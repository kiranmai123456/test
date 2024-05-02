# Import necessary libraries
import os
import json
import frappe
from frappe.model.document import Document

class VirtualDoctype(Document):
    DATA_FILE = "data_file.json"

    @staticmethod
    def get_current_data():
        if not os.path.exists(VirtualDoctype.DATA_FILE):
            return {}

        try:
            with open(VirtualDoctype.DATA_FILE) as f:
                data = f.read()
                return json.loads(data) if data else {}
        except json.JSONDecodeError as e:
            frappe.throw(f"Error decoding JSON data: {str(e)}")

    @staticmethod
    def update_data(data):
        with open(VirtualDoctype.DATA_FILE, "w+") as data_file:
            json.dump(data, data_file)

    def db_insert(self, *args, **kwargs):
        d = self.get_valid_dict(convert_dates_to_str=True)

        data = self.get_current_data()
        data[d.name] = d

        self.update_data(data)

    def load_from_db(self):
        data = self.get_current_data()
        d = data.get(self.name)
        super(Document, self).__init__(d)

    def db_update(self, *args, **kwargs):
        # For this example, insert and update are the same operation
        self.db_insert(*args, **kwargs)

    def delete(self):
        data = self.get_current_data()
        data.pop(self.name, None)
        self.update_data(data)

    @staticmethod
    def get_list(args):
        data = VirtualDoctype.get_current_data()
        return [frappe._dict(doc) for name, doc in data.items()]

    @staticmethod
    def get_count(args):
        data = VirtualDoctype.get_current_data()
        return len(data)

    @staticmethod
    def get_stats(args):
        return {}
