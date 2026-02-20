
import frappe
from frappe.model.document import Document

class GridInverter(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_telemetry(inverter_id):
    """Safely retrieves live cache data for Polling frontend avoiding WebSocket complexities."""
    data = frappe.cache().get_value(f"live_data::{inverter_id}")
    import json
    return json.loads(data) if isinstance(data, str) else dict(data or {})
