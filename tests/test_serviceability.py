import unittest
from serviceability.engine import PincodeServiceabilityEngine, PincodeCoverage, CourierCapability


class TestPincodeServiceability(unittest.TestCase):
    def setUp(self):
        self.engine = PincodeServiceabilityEngine()
        # Add Mumbai pincode
        self.engine.add_pincode_rule(PincodeCoverage(
            pincode="400001",
            city="Mumbai",
            state="Maharashtra",
            zone="METRO",
            is_prepaid_available=True,
            is_cod_available=True,
            max_cod_amount=5000.0,
            supported_couriers=[
                CourierCapability(courier_code="DELHIVERY_SURFACE", base_rate_500g=40.0, additional_500g_rate=30.0, cod_charge=25.0, sla_days=2),
                CourierCapability(courier_code="BLUEDART_AIR", base_rate_500g=75.0, additional_500g_rate=45.0, cod_charge=40.0, sla_days=1)
            ]
        ))

    def test_prepaid_serviceability(self):
        decision = self.engine.evaluate_serviceability(
            dest_pincode="400001",
            package_weight_grams=800.0,
            cart_value=1200.0,
            preferred_payment="PREPAID"
        )
        self.assertTrue(decision.is_serviceable)
        self.assertEqual(decision.city, "Mumbai")
        self.assertEqual(decision.recommended_courier, "DELHIVERY_SURFACE")
        self.assertEqual(decision.estimated_delivery_days, 2)

    def test_cod_limit_exceeded(self):
        # Cart value 7000 exceeds max COD 5000
        decision = self.engine.evaluate_serviceability(
            dest_pincode="400001",
            package_weight_grams=500.0,
            cart_value=7000.0,
            preferred_payment="COD"
        )
        self.assertFalse(decision.is_serviceable)
        self.assertIn("not permitted", decision.rejection_reason)


if __name__ == "__main__":
    unittest.main()
