# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "serviceability"
app_title = "Frappe Pincode Serviceability Matrix"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Pincode Serviceability Matrix - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/serviceability/css/serviceability.bundle.css"
app_include_js = "/assets/serviceability/js/serviceability.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Pincode Serviceability Matrix Entry": {
        "validate": "serviceability.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "serviceability.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "serviceability.tasks.hourly_sync"
    ],
    "daily": [
        "serviceability.tasks.daily_reconciliation"
    ],
    "weekly": [
        "serviceability.tasks.weekly_digest"
    ]
}
