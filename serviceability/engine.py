"""Postal Pincode Serviceability, Courier Partner Routing & COD Restriction Engine."""

import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class CourierCapability(BaseModel):
    courier_code: str  # BLUEDART_AIR, DELHIVERY_SURFACE, SHADOWFAX_HYPERLOCAL, EKART
    base_rate_500g: float
    additional_500g_rate: float
    cod_charge: float
    max_weight_kg: float = 20.0
    sla_days: int = 3


class PincodeCoverage(BaseModel):
    pincode: str
    city: str
    state: str
    zone: str  # METRO, REGIONAL, REMOTE_NORTH_EAST, SPECIAL_DESTINATION
    is_prepaid_available: bool = True
    is_cod_available: bool = True
    max_cod_amount: float = 10000.0  # Max cash on delivery limit
    supported_couriers: List[CourierCapability] = Field(default_factory=list)


class ServiceabilityDecision(BaseModel):
    pincode: str
    city: str
    state: str
    is_serviceable: bool
    payment_mode_allowed: List[str]  # PREPAID, COD
    recommended_courier: Optional[str] = None
    estimated_shipping_fee: float = 0.0
    estimated_delivery_days: int = 0
    rejection_reason: Optional[str] = None


class PincodeServiceabilityEngine:
    """Manages Indian 6-digit postal code courier serviceability, COD eligibility, and rate shopping."""

    PINCODE_REGEX = re.compile(r"^[1-9][0-9]{5}$")

    def __init__(self):
        self.coverage_db: Dict[str, PincodeCoverage] = {}

    def add_pincode_rule(self, coverage: PincodeCoverage) -> PincodeCoverage:
        if not self.PINCODE_REGEX.match(coverage.pincode):
            raise ValueError(f"Invalid Indian postal pincode: {coverage.pincode}")
        self.coverage_db[coverage.pincode] = coverage
        return coverage

    def evaluate_serviceability(
        self,
        dest_pincode: str,
        package_weight_grams: float,
        cart_value: float,
        preferred_payment: str = "PREPAID"  # PREPAID or COD
    ) -> ServiceabilityDecision:
        cleaned_pin = dest_pincode.strip()
        if not self.PINCODE_REGEX.match(cleaned_pin):
            return ServiceabilityDecision(
                pincode=cleaned_pin,
                city="Unknown",
                state="Unknown",
                is_serviceable=False,
                payment_mode_allowed=[],
                rejection_reason="Invalid 6-digit postal code format."
            )

        cov = self.coverage_db.get(cleaned_pin)
        if not cov:
            return ServiceabilityDecision(
                pincode=cleaned_pin,
                city="Unknown",
                state="Unknown",
                is_serviceable=False,
                payment_mode_allowed=[],
                rejection_reason=f"Pincode {cleaned_pin} is currently not serviceable by any logistics partner."
            )

        allowed_payments = []
        if cov.is_prepaid_available:
            allowed_payments.append("PREPAID")
        if cov.is_cod_available and cart_value <= cov.max_cod_amount:
            allowed_payments.append("COD")

        payment_mode = preferred_payment.upper()
        if payment_mode not in allowed_payments:
            return ServiceabilityDecision(
                pincode=cleaned_pin,
                city=cov.city,
                state=cov.state,
                is_serviceable=False,
                payment_mode_allowed=allowed_payments,
                rejection_reason=f"Payment method '{payment_mode}' not permitted for pincode {cleaned_pin} (Limit ₹{cov.max_cod_amount})."
            )

        # Rate shopping across active couriers supporting the weight
        package_weight_kg = package_weight_grams / 1000.0
        eligible_couriers = [c for c in cov.supported_couriers if package_weight_kg <= c.max_weight_kg]

        if not eligible_couriers:
            return ServiceabilityDecision(
                pincode=cleaned_pin,
                city=cov.city,
                state=cov.state,
                is_serviceable=False,
                payment_mode_allowed=allowed_payments,
                rejection_reason=f"Package weight {package_weight_kg}kg exceeds max carrier weight limit."
            )

        # Pick lowest-cost courier
        best_courier = None
        lowest_freight = float("inf")
        best_sla = 5

        for courier in eligible_couriers:
            # First 500g
            freight = courier.base_rate_500g
            if package_weight_grams > 500.0:
                extra_units = (package_weight_grams - 500.0) / 500.0
                freight += extra_units * courier.additional_500g_rate
            if payment_mode == "COD":
                freight += courier.cod_charge

            if freight < lowest_freight:
                lowest_freight = freight
                best_courier = courier.courier_code
                best_sla = courier.sla_days

        return ServiceabilityDecision(
            pincode=cleaned_pin,
            city=cov.city,
            state=cov.state,
            is_serviceable=True,
            payment_mode_allowed=allowed_payments,
            recommended_courier=best_courier,
            estimated_shipping_fee=round(lowest_freight, 2),
            estimated_delivery_days=best_sla
        )
