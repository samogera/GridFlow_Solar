
import frappe
import time
import json
from ecobright.driver import get_connection, read_inverter_data

def process_telemetry(inverter_id, modbus, last_log_time):
    """
    Single step of telemetry processing.
    Returns the new last_log_time.
    """
    # 3. Fetch Data
    data = read_inverter_data(modbus)
    
    if data:
        # Add Timestamp
        data['timestamp'] = frappe.utils.now()
        data['inverter'] = inverter_id

        # A. Update Redis (For Virtual DocType)
        frappe.cache().set_value(f"live_data::{inverter_id}", data)

        # B. Push to Frontend (Socket.io)
        frappe.publish_realtime(
            event="inverter_update",
            message=data,
            room=f"inverter_room_{inverter_id}"
        )

        # C. Historical Log (Every 5 Minutes)
        if time.time() - last_log_time > 300: # 300 seconds
            log_entry = frappe.get_doc({
                "doctype": "Telemetry Log",
                "inverter": inverter_id,
                "power_w": data['power_w'],
                "soc_percent": data['soc'],
                "timestamp": frappe.utils.now()
            })
            log_entry.insert(ignore_permissions=True)
            frappe.db.commit()
            last_log_time = time.time()

    return last_log_time

def start_worker(inverter_id):
    """
    Main Loop: Polls LSW-3 -> Updates Redis -> Pushes to Socket.io
    """
    # 1. Setup
    doc = frappe.get_doc("Grid Inverter", inverter_id)
    print(f"Starting Telemetry for {doc.inverter_id}...")
    
    # 2. Connect
    modbus = get_connection(doc.ip_address, doc.uid)
    
    # Track time for historical logging
    last_log_time = time.time()
    
    while True:
        try:
            if not modbus:
                 # Retry logic if connection dropped
                print("Reconnecting...")
                modbus = get_connection(doc.ip_address, doc.uid)
                time.sleep(5)
                continue

            last_log_time = process_telemetry(inverter_id, modbus, last_log_time)

            # 4. Pace the loop (Don't flood the LSW-3, it's weak)
            time.sleep(2) 

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5) # Backoff on error