# app/services/catalog.py

"""
Mock Catalog Service

This service simulates an external catalog API (like MISUMI) to fetch technical
specifications for components based on their part number.
"""

from typing import Any, Dict, TypedDict


class PinData(TypedDict):
    pin_count: int
    pin_positions: list[dict[str, float]]  # e.g., [{"x": 0, "y": 0}, ...]


class ComponentSpec(TypedDict):
    voltage_rating: float | None
    applicable_wire_max_diameter: float | None
    outer_diameter: float | None
    is_rohs: bool | None
    is_ul: bool | None
    pins: PinData | None


# Mock database for component specifications.
# In a real-world scenario, this would be fetched from an external API or a dedicated database.
MOCK_CATALOG_DB: Dict[str, ComponentSpec] = {
    # Connectors
    "DF13-3S-1.25C": {
        "voltage_rating": 150.0,  # Volts
        "applicable_wire_max_diameter": 0.9,  # mm
        "is_rohs": True,
        "is_ul": True,
        "pins": {"pin_count": 3, "pin_positions": []},
        "outer_diameter": None,
    },
    "PHR-3": {
        "voltage_rating": 100.0,
        "applicable_wire_max_diameter": 1.5,
        "is_rohs": True,
        "is_ul": True,
        "pins": {"pin_count": 3, "pin_positions": []},
        "outer_diameter": None,
    },
    # Connector that is not RoHS compliant
    "OLD-CONN-01": {
        "voltage_rating": 50.0,
        "applicable_wire_max_diameter": 2.0,
        "is_rohs": False,
        "is_ul": True,
        "pins": {"pin_count": 4, "pin_positions": []},
        "outer_diameter": None,
    },
    # Wires
    "UL1007-26-RD": {
        "voltage_rating": 300.0,
        "outer_diameter": 1.2,  # mm
        "is_rohs": True,
        "is_ul": True,
        "pins": None,
        "applicable_wire_max_diameter": None,
    },
    "UL1007-22-BK": {
        "voltage_rating": 300.0,
        "outer_diameter": 1.6,
        "is_rohs": True,
        "is_ul": True,
        "pins": None,
        "applicable_wire_max_diameter": None,
    },
    # Wire with a large diameter
    "THICK-WIRE-01": {
        "voltage_rating": 600.0,
        "outer_diameter": 3.0,
        "is_rohs": True,
        "is_ul": True,
        "pins": None,
        "applicable_wire_max_diameter": None,
    },
}


class CatalogService:
    def get_specification(self, part_number: str) -> ComponentSpec | None:
        """
        Retrieves the technical specifications for a given part number.
        Returns None if the part number is not found in the catalog.
        """
        return MOCK_CATALOG_DB.get(part_number)


catalog_service = CatalogService()
