# Frappe Pincode Serviceability & Logistics Matrix 📦📍

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Frappe](https://img.shields.io/badge/Frappe-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An enterprise 6-digit Indian postal code serviceability, Cash on Delivery (COD) restriction engine, and multi-courier partner rate shopping system for **Frappe Framework & E-Commerce Checkouts**.

---

## 🚀 Key Features

- **Pincode Format & Zone Mapping**: Validates Indian PIN codes against regional tier classifications (Metro, Non-Metro, Remote North-East).
- **COD Risk Threshold Enforcement**: Blocks high-value Cash on Delivery orders above risk thresholds to protect against fraudulent RTO returns.
- **Dynamic Courier Rate Shopping**: Compares air and surface freight across Delhivery, Bluedart, Shadowfax, and Ekart.
- **Accurate SLA Delivery Estimates**: Predicts guaranteed arrival business days for transparent checkout experiences.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/frappe-pincode-serviceability-matrix.git
cd frappe-pincode-serviceability-matrix
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from serviceability.engine import PincodeServiceabilityEngine, PincodeCoverage, CourierCapability

engine = PincodeServiceabilityEngine()

engine.add_pincode_rule(PincodeCoverage(
    pincode="110001",
    city="New Delhi",
    state="Delhi",
    zone="METRO",
    is_prepaid_available=True,
    is_cod_available=True,
    max_cod_amount=7500.0,
    supported_couriers=[
        CourierCapability(courier_code="BLUEDART_AIR", base_rate_500g=65.0, additional_500g_rate=35.0, cod_charge=30.0, sla_days=1)
    ]
))

result = engine.evaluate_serviceability("110001", package_weight_grams=450.0, cart_value=1500.0, preferred_payment="COD")
print(f"Serviceable: {result.is_serviceable} | Courier: {result.recommended_courier} | Delivery: {result.estimated_delivery_days} days")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
