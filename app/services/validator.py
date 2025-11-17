# app/services/validator.py
from typing import List

from sqlalchemy.orm import Session

from app import models
from app.schemas.validation import ValidationError


class ValidationService:
    def validate_harness(
        self, db: Session, harness: models.Harness, settings: models.ProjectSettings
    ) -> List[ValidationError]:
        errors: List[ValidationError] = []

        # Rule 1: Data Quality - Check for missing specifications
        for connector in harness.connectors:
            if any(
                spec is None
                for spec in [
                    connector.voltage_rating,
                    connector.applicable_wire_max_diameter,
                    connector.is_rohs,
                    connector.is_ul,
                ]
            ):
                errors.append(
                    ValidationError(
                        component_id=str(connector.id),
                        component_type="Connector",
                        message=f"Connector {connector.logical_id} ({connector.part_number}) has missing technical specifications.",
                        error_type="DataQualityError",
                    )
                )

        for wire in harness.wires:
            if any(
                spec is None
                for spec in [
                    wire.voltage_rating,
                    wire.outer_diameter,
                    wire.is_rohs,
                    wire.is_ul,
                ]
            ):
                errors.append(
                    ValidationError(
                        component_id=str(wire.id),
                        component_type="Wire",
                        message=f"Wire {wire.logical_id} ({wire.part_number}) has missing technical specifications.",
                        error_type="DataQualityError",
                    )
                )

        # Rule 2: Electrical - Check voltage ratings
        if settings.system_voltage:
            for connector in harness.connectors:
                if (
                    connector.voltage_rating is not None
                    and connector.voltage_rating < settings.system_voltage
                ):
                    errors.append(
                        ValidationError(
                            component_id=str(connector.id),
                            component_type="Connector",
                            message=f"Connector {connector.logical_id} voltage rating ({connector.voltage_rating}V) is less than system voltage ({settings.system_voltage}V).",
                            error_type="ElectricalError",
                        )
                    )
            for wire in harness.wires:
                if (
                    wire.voltage_rating is not None
                    and wire.voltage_rating < settings.system_voltage
                ):
                    errors.append(
                        ValidationError(
                            component_id=str(wire.id),
                            component_type="Wire",
                            message=f"Wire {wire.logical_id} voltage rating ({wire.voltage_rating}V) is less than system voltage ({settings.system_voltage}V).",
                            error_type="ElectricalError",
                        )
                    )

        # Rule 3: Compliance - Check RoHS and UL standards
        if settings.require_rohs:
            for component in harness.connectors + harness.wires:
                if not component.is_rohs:
                    errors.append(
                        ValidationError(
                            component_id=str(component.id),
                            component_type=type(component).__name__,
                            message=f"Component {component.logical_id} ({component.part_number}) is not RoHS compliant.",
                            error_type="ComplianceError",
                        )
                    )

        # Rule 4: Physical - Check wire diameter vs. connector capacity
        for connection in harness.connections:
            wire = connection.wire
            from_connector = connection.from_pin.connector

            if (
                wire.outer_diameter is not None
                and from_connector.applicable_wire_max_diameter is not None
                and wire.outer_diameter
                > from_connector.applicable_wire_max_diameter
            ):
                errors.append(
                    ValidationError(
                        component_id=str(connection.id),
                        component_type="Connection",
                        message=f"Wire {wire.logical_id} ({wire.outer_diameter}mm) exceeds max diameter for connector {from_connector.logical_id} ({from_connector.applicable_wire_max_diameter}mm).",
                        error_type="PhysicalError",
                    )
                )

        return errors


validation_service = ValidationService()
