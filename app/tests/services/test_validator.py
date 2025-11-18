# app/tests/services/test_validator.py

import pytest
from sqlalchemy.orm import Session

from app import models
from app.services.validator import ValidationService


# A reusable mock project settings object for tests
@pytest.fixture
def mock_project_settings() -> models.ProjectSettings:
    return models.ProjectSettings(
        system_voltage=24.0,
        require_rohs=True,
        require_ul=False,
    )


# A reusable mock harness object for tests
@pytest.fixture
def mock_harness(db: Session) -> models.Harness:
    harness = models.Harness(name="Test Harness")
    db.add(harness)
    db.commit()
    return harness


def test_validation_success(
    db: Session,
    mock_harness: models.Harness,
    mock_project_settings: models.ProjectSettings,
):
    """
    Test a harness that should pass all validation rules.
    """
    # Create valid components
    connector = models.Connector(
        logical_id="C1",
        manufacturer="Test",
        part_number="VALID-CONN",
        harness_id=mock_harness.id,
        voltage_rating=50.0,
        applicable_wire_max_diameter=2.0,
        is_rohs=True,
        is_ul=True,
    )
    wire = models.Wire(
        logical_id="W1",
        manufacturer="Test",
        part_number="VALID-WIRE",
        harness_id=mock_harness.id,
        color="RD",
        gauge=22,
        length=100,
        voltage_rating=100.0,
        outer_diameter=1.5,
        is_rohs=True,
        is_ul=True,
    )
    db.add_all([connector, wire])
    db.commit()

    validator = ValidationService()
    errors = validator.validate_harness(
        db=db, harness=mock_harness, settings=mock_project_settings
    )
    assert len(errors) == 0


def test_data_quality_error(
    db: Session,
    mock_harness: models.Harness,
    mock_project_settings: models.ProjectSettings,
):
    """
    Test that a component with missing specs raises a DataQualityError.
    """
    connector = models.Connector(
        logical_id="C1",
        manufacturer="Test",
        part_number="INCOMPLETE-CONN",
        harness_id=mock_harness.id,
        voltage_rating=None,  # Missing spec
    )
    db.add(connector)
    db.commit()

    validator = ValidationService()
    errors = validator.validate_harness(
        db=db, harness=mock_harness, settings=mock_project_settings
    )
    assert len(errors) == 1
    assert errors[0].error_type == "DataQualityError"


def test_electrical_error(
    db: Session,
    mock_harness: models.Harness,
    mock_project_settings: models.ProjectSettings,
):
    """
    Test that a component with a voltage rating below the system requirement
    raises an ElectricalError.
    """
    connector = models.Connector(
        logical_id="C1",
        manufacturer="Test",
        part_number="LOW-VOLTAGE-CONN",
        harness_id=mock_harness.id,
        voltage_rating=12.0,  # Below system voltage of 24V
        applicable_wire_max_diameter=2.0,
        is_rohs=True,
        is_ul=True,
    )
    db.add(connector)
    db.commit()

    validator = ValidationService()
    errors = validator.validate_harness(
        db=db, harness=mock_harness, settings=mock_project_settings
    )
    assert len(errors) == 1
    assert errors[0].error_type == "ElectricalError"


def test_compliance_error(
    db: Session,
    mock_harness: models.Harness,
    mock_project_settings: models.ProjectSettings,
):
    """
    Test that a non-RoHS component in a project requiring RoHS
    raises a ComplianceError.
    """
    connector = models.Connector(
        logical_id="C1",
        manufacturer="Test",
        part_number="NON-ROHS-CONN",
        harness_id=mock_harness.id,
        voltage_rating=50.0,
        applicable_wire_max_diameter=2.0,
        is_rohs=False,  # Not compliant
        is_ul=True,
    )
    db.add(connector)
    db.commit()

    validator = ValidationService()
    errors = validator.validate_harness(
        db=db, harness=mock_harness, settings=mock_project_settings
    )
    assert len(errors) == 1
    assert errors[0].error_type == "ComplianceError"


def test_physical_error(
    db: Session,
    mock_harness: models.Harness,
    mock_project_settings: models.ProjectSettings,
):
    """
    Test that a wire with a diameter larger than the connector's max
    raises a PhysicalError.
    """
    connector = models.Connector(
        logical_id="C1",
        manufacturer="Test",
        part_number="SMALL-CONN",
        harness_id=mock_harness.id,
        voltage_rating=50.0,
        applicable_wire_max_diameter=1.5,  # Max 1.5mm
        is_rohs=True,
        is_ul=True,
    )
    wire = models.Wire(
        logical_id="W1",
        manufacturer="Test",
        part_number="THICK-WIRE",
        harness_id=mock_harness.id,
        color="BL",
        gauge=20,
        length=100,
        voltage_rating=100.0,
        outer_diameter=2.0,  # 2.0mm wire
        is_rohs=True,
        is_ul=True,
    )
    pin1 = models.Pin(logical_id="1", connector=connector)
    # Fake second pin for connection
    pin2 = models.Pin(logical_id="2", connector=connector)
    db.add_all([connector, wire, pin1, pin2])
    db.commit()

    connection = models.Connection(
        harness_id=mock_harness.id,
        wire_id=wire.id,
        from_pin_id=pin1.id,
        to_pin_id=pin2.id,
    )
    db.add(connection)
    db.commit()

    validator = ValidationService()
    errors = validator.validate_harness(
        db=db, harness=mock_harness, settings=mock_project_settings
    )
    assert len(errors) == 1
    assert errors[0].error_type == "PhysicalError"
