import frappe
from frappe.model.document import Document
import json

class LiveStatus(Document):
    def db_insert(self, *args, **kwargs):
        pass # Virtual DocTypes don't insert to DB

    def db_update(self, *args, **kwargs):
        pass # Virtual DocTypes don't update DB

    @staticmethod
    def get_list(args):
        """
        This is called when you open the List View.
        It pulls all active inverter data from Redis.
        """
        result = []
        # Find all keys in Redis cache that start with our prefix
        keys = frappe.cache().get_keys("live_data::")
        
        for key in keys:
            # Redis returns keys with the site prefix, we need the raw data
            raw_data = frappe.cache().get_value(key)
            if raw_data:
                # If data is stored as a string/json, parse it
                if isinstance(raw_data, str):
                    data = json.loads(raw_data)
                else:
                    data = raw_data
                
                result.append(frappe._dict(data))
        
        return result

    @staticmethod
    def get_count(args):
        return len(frappe.cache().get_keys("live_data::"))

    @staticmethod
    def get_stats(args):
        return {}