import frappe
from frappe.model.document import Document
from frappe.permissions import add_permission
from frappe import _
from frappe.utils import now_datetime, cstr

@frappe.whitelist()
def create_custom_doctype():
    # Define your custom DocType details
    doctype_name = 'Jhansi3'
    module = 'lenovo'
    
    # Create a new DocType
    doc = frappe.get_doc({
        'doctype': 'DocType',
        'module': module,
        'custom': 1,
        'name': doctype_name,
        'fields': [
            {
                'fieldname': 'fname',
                'label': 'FName',
                'fieldtype': 'Data',
                'reqd': 1,
                # Add more field properties as needed
            },
            # Add more fields as needed
        ],
        # Add more DocType properties as needed
    })

    # Save the DocType
    doc.insert()


    print(f"DocType '{doctype_name}' created successfully!")



@frappe.whitelist(allow_guest=True)
def get_recent_records(doctype, username, limit=10):
    # Get user's recent records
    recent_records = frappe.get_list(
        doctype,
        fields=["name", "creation", "modified"],
        filters={"owner": username},
        order_by="creation desc",
        limit=limit
    )

    # Prepare response
    response = {
        "success": True,
        "message": _("Recent records fetched successfully"),
        "data": recent_records
    }

    return response




@frappe.whitelist()
def get_recent_record(doctype, username):
    # Get user's most recent record
    recent_record = frappe.get_list(
        doctype,
        fields=["name", "creation", "modified"],
        filters={"owner": username},
        order_by="creation desc",
        limit=1
    )

    # Prepare response
    if recent_record:
        response = {
            "success": True,
            "message": _("Most recent record fetched successfully"),
            "data": recent_record[0]
        }
    else:
        response = {
            "success": False,
            "message": _("No recent record found"),
            "data": None
        }

    return response
