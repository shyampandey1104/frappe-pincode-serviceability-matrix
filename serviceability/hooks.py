# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "serviceability"
app_title = "Frappe Pincode Serviceability Matrix"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Pincode Serviceability Matrix for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/serviceability/css/serviceability.bundle.css"
app_include_js = "/assets/serviceability/js/serviceability.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "serviceability.engine.on_document_submit",
        "on_cancel": "serviceability.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "serviceability.engine.daily_scheduled_sync"
    ]
}
