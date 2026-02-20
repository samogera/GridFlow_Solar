import click
import frappe
from ecobright.telemetry_worker import start_worker

@click.command("start-telemetry")
@click.argument("inverter_id")
def start_telemetry(inverter_id):
    """Starts the live telemetry stream for a given inverter."""
    
    # We know the exact name now, so we hardcode it!
    site_name = "ecobright.docker"
            
    click.echo(f"Connecting to database for site: {site_name}...")
    
    # Initialize and connect
    frappe.init(site=site_name)
    frappe.connect()
    
    try:
        click.echo(f"Starting Telemetry Worker for Inverter: {inverter_id}")
        start_worker(inverter_id)
    finally:
        frappe.destroy()

commands = [
    start_telemetry
]