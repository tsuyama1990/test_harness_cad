# app/services/validator.py
from typing import List

from sqlalchemy.orm import Session

from app import models
from app.schemas.validation import ValidationError
from app.services.catalog import catalog_service


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
                        message=(
                            f"Connector {connector.logical_id} "
                            f"({connector.part_number}) has missing "
                            "technical specifications."
                        ),
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
                        message=(
                            f"Wire {wire.logical_id} ({wire.part_number}) has "
                            "missing technical specifications."
                        ),
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
                            message=(
                                f"Connector {connector.logical_id} voltage rating "
                                f"({connector.voltage_rating}V) is less than "
                                f"system voltage ({settings.system_voltage}V)."
                            ),
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
                            message=(
                                f"Wire {wire.logical_id} voltage rating "
                                f"({wire.voltage_rating}V) is less than system "
                                f"voltage ({settings.system_voltage}V)."
                            ),
                            error_type="ElectricalError",
                        )
                    )

        # Rule 3: Compliance - Check RoHS and UL standards
        if settings.require_rohs:
            for component in harness.connectors + harness.wires:
                if component.is_rohs is False:
                    errors.append(
                        ValidationError(
                            component_id=str(component.id),
                            component_type=type(component).__name__,
                            message=(
                                f"Component {component.logical_id} "
                                f"({component.part_number}) is not RoHS "
                                "compliant."
                            ),
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
                and wire.outer_diameter > from_connector.applicable_wire_max_diameter
            ):
                errors.append(
                    ValidationError(
                        component_id=str(connection.id),
                        component_type="Connection",
                        message=(
                            f"Wire {wire.logical_id} diameter "
                            f"({wire.outer_diameter}mm) exceeds max "
                            f"diameter for connector "
                            f"{from_connector.logical_id} "
                            f"({from_connector.applicable_wire_max_diameter}mm)."
                        ),
                        error_type="PhysicalError",
                    )
                )

        # Rule 5: Terminal Compatibility
        for conn in harness.connections:
            wire_gauge = conn.wire.gauge

            # Check terminal on side A
            if conn.terminal_part_number_a:
                terminal_a_spec = catalog_service.get_specification(conn.terminal_part_number_a)
                if not terminal_a_spec:
                    errors.append(ValidationError(
                        component_id=str(conn.id), component_type="Connection",
                        message=f"Terminal {conn.terminal_part_number_a} not found in catalog.",
                        error_type="DataQualityError"
                    ))
                else:
                    # 1. Wire gauge check
                    min_gauge = terminal_a_spec.get("applicable_wire_gauge_min")
                    max_gauge = terminal_a_spec.get("applicable_wire_gauge_max")
                    if not (min_gauge is not None and max_gauge is not None and min_gauge <= wire_gauge <= max_gauge):
                        errors.append(ValidationError(
                            component_id=str(conn.id), component_type="Connection",
                            message=f"Wire gauge AWG{wire_gauge} is not compatible with terminal {conn.terminal_part_number_a} (supports AWG{min_gauge}-{max_gauge}).",
                            error_type="CompatibilityError"
                        ))

                    # 2. Connector series check
                    connector_a_series = conn.from_pin.connector.part_number.split('-')[0]
                    compatible_series = terminal_a_spec.get("compatible_connector_series")
                    if compatible_series and connector_a_series not in compatible_series:
                        errors.append(ValidationError(
                            component_id=str(conn.id), component_type="Connection",
                            message=f"Terminal {conn.terminal_part_number_a} is not compatible with connector series {connector_a_series}.",
                            error_type="CompatibilityError"
                        ))

            # Check terminal on side B
            if conn.terminal_part_number_b:
                terminal_b_spec = catalog_service.get_specification(conn.terminal_part_number_b)
                if not terminal_b_spec:
                    errors.append(ValidationError(
                        component_id=str(conn.id), component_type="Connection",
                        message=f"Terminal {conn.terminal_part_number_b} not found in catalog.",
                        error_type="DataQualityError"
                    ))
                else:
                    # 1. Wire gauge check
                    min_gauge = terminal_b_spec.get("applicable_wire_gauge_min")
                    max_gauge = terminal_b_spec.get("applicable_wire_gauge_max")
                    if not (min_gauge is not None and max_gauge is not None and min_gauge <= wire_gauge <= max_gauge):
                        errors.append(ValidationError(
                            component_id=str(conn.id), component_type="Connection",
                            message=f"Wire gauge AWG{wire_gauge} is not compatible with terminal {conn.terminal_part_number_b} (supports AWG{min_gauge}-{max_gauge}).",
                            error_type="CompatibilityError"
                        ))

                    # 2. Connector series check
                    connector_b_series = conn.to_pin.connector.part_number.split('-')[0]
                    compatible_series = terminal_b_spec.get("compatible_connector_series")
                    if compatible_series and connector_b_series not in compatible_series:
                        errors.append(ValidationError(
                            component_id=str(conn.id), component_type="Connection",
                            message=f"Terminal {conn.terminal_part_number_b} is not compatible with connector series {connector_b_series}.",
                            error_type="CompatibilityError"
                        ))

        return errors


validation_service = ValidationService()
