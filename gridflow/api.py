import frappe

@frappe.whitelist(allow_guest=True)
def handle_device_telemetry(device_id, kwh, v, i):
    # 1. Verify the device exists
    if not frappe.db.exists("GridFlow Device", device_id):
        return {"status": "error", "message": "Device not found"}

    # 2. Create the Energy Log
    log = frappe.get_doc({
        "doctype": "Energy Log",
        "device_id": device_id,
        "yieldkwh": kwh,
        "voltage": v,
        "current": i,
        "reading_time": frappe.utils.now_datetime(),
        "mint_status": "Pending"
    })
    log.insert(ignore_permissions=True)

    # 3. Check Balance for School/Hospital
    balance = frappe.db.get_value("GridFlow Device", device_id, "wallet_balance")
    
    # Send command back to ESP32: 1 = ON, 0 = OFF
    command = 1 if balance > 0 else 0
    
    frappe.db.commit()
    return {"status": "success", "relay_command": command}