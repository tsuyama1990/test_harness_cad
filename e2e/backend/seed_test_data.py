import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.db.session import SessionLocal
from app.schemas.harness import (
    ConnectorCreate,
    HarnessCreate,
    PinCreate,
    WireCreate,
)
from app.services.harness_service import harness_service


def seed_harness_data():
    db = SessionLocal()
    try:
        # Define sample data for a harness
        sample_harness_data = HarnessCreate(
            name="Test Harness 1",
            connectors=[
                ConnectorCreate(
                    id="CONN1",
                    manufacturer="TE",
                    part_number="1-1234567-1",
                    pins=[PinCreate(id="1"), PinCreate(id="2")],
                ),
                ConnectorCreate(
                    id="CONN2",
                    manufacturer="Molex",
                    part_number="2-9876543-2",
                    pins=[PinCreate(id="A"), PinCreate(id="B")],
                ),
            ],
            wires=[
                WireCreate(
                    id="WIRE1",
                    manufacturer="Sumitomo",
                    part_number="S-100",
                    color="RED",
                    gauge=0.5,
                    length=100.0,
                ),
                WireCreate(
                    id="WIRE2",
                    manufacturer="Sumitomo",
                    part_number="S-100",
                    color="BLUE",
                    gauge=0.5,
                    length=150.0,
                ),
            ],
            connections=[],  # Start with no connections
        )

        harness = harness_service.create_harness(db=db, harness_in=sample_harness_data)
        print(f"Successfully created harness with ID: {harness.id}")
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_harness_data()
