import io
from uuid import UUID

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.exceptions import HarnessNotFoundException, InvalidHarnessDataException


class HarnessService:
    def create_harness(
        self, db: Session, harness_in: schemas.HarnessCreate
    ) -> models.Harness:
        # Create Harness
        db_harness = models.Harness()
        db_harness.name = harness_in.name
        db.add(db_harness)
        db.flush()

        # Create Connectors and Pins
        connector_map = {}
        pin_map = {}
        for conn_in in harness_in.connectors:
            db_conn = models.Connector()
            db_conn.logical_id = conn_in.id
            db_conn.manufacturer = conn_in.manufacturer
            db_conn.part_number = conn_in.part_number
            db_conn.harness_id = db_harness.id
            db.add(db_conn)
            db.flush()
            connector_map[conn_in.id] = db_conn
            for pin_in in conn_in.pins:
                db_pin = models.Pin()
                db_pin.logical_id = pin_in.id
                db_pin.connector_id = db_conn.id
                db.add(db_pin)
                db.flush()
                pin_map[f"{conn_in.id}-{pin_in.id}"] = db_pin

        # Create Wires
        wire_map = {}
        for wire_in in harness_in.wires:
            db_wire = models.Wire()
            db_wire.logical_id = wire_in.id
            db_wire.manufacturer = wire_in.manufacturer
            db_wire.part_number = wire_in.part_number
            db_wire.color = wire_in.color
            db_wire.gauge = wire_in.gauge
            db_wire.length = wire_in.length
            db_wire.harness_id = db_harness.id
            db.add(db_wire)
            db.flush()
            wire_map[wire_in.id] = db_wire

        # Create Connections
        for conn_data in harness_in.connections:
            from_pin_key = f"{conn_data.from_connector_id}-{conn_data.from_pin_id}"
            to_pin_key = f"{conn_data.to_connector_id}-{conn_data.to_pin_id}"

            if from_pin_key not in pin_map or to_pin_key not in pin_map:
                raise InvalidHarnessDataException("Pin not found for connection.")
            if conn_data.wire_id not in wire_map:
                raise InvalidHarnessDataException("Wire not found for connection.")

            db_connection = models.Connection()
            db_connection.harness_id = db_harness.id
            db_connection.wire_id = wire_map[conn_data.wire_id].id
            db_connection.from_pin_id = pin_map[from_pin_key].id
            db_connection.to_pin_id = pin_map[to_pin_key].id

            # Add assembly instructions
            db_connection.strip_length_a = conn_data.strip_length_a
            db_connection.strip_length_b = conn_data.strip_length_b
            db_connection.terminal_part_number_a = conn_data.terminal_part_number_a
            db_connection.terminal_part_number_b = conn_data.terminal_part_number_b
            db_connection.marking_text_a = conn_data.marking_text_a
            db_connection.marking_text_b = conn_data.marking_text_b
            db.add(db_connection)

        db.commit()
        db.refresh(db_harness)
        return db_harness

    def update_harness(
        self, db: Session, harness_id: UUID, harness_in: schemas.HarnessCreate
    ) -> models.Harness:
        db_harness = self.get_harness(db=db, harness_id=harness_id)

        # Clear existing data
        for connection in db_harness.connections:
            db.delete(connection)
        for wire in db_harness.wires:
            db.delete(wire)
        for connector in db_harness.connectors:
            db.delete(connector)  # Pins will be cascade-deleted
        db.flush()

        # Update harness name
        db_harness.name = harness_in.name

        # Re-create components from the input schema
        connector_map = {}
        pin_map = {}
        for conn_in in harness_in.connectors:
            db_conn = models.Connector()
            db_conn.logical_id = conn_in.id
            db_conn.manufacturer = conn_in.manufacturer
            db_conn.part_number = conn_in.part_number
            db_conn.harness_id = db_harness.id
            db.add(db_conn)
            db.flush()
            connector_map[conn_in.id] = db_conn
            for pin_in in conn_in.pins:
                db_pin = models.Pin()
                db_pin.logical_id = pin_in.id
                db_pin.connector_id = db_conn.id
                db.add(db_pin)
                db.flush()
                pin_map[f"{conn_in.id}-{pin_in.id}"] = db_pin

        wire_map = {}
        for wire_in in harness_in.wires:
            db_wire = models.Wire()
            db_wire.logical_id = wire_in.id
            db_wire.manufacturer = wire_in.manufacturer
            db_wire.part_number = wire_in.part_number
            db_wire.color = wire_in.color
            db_wire.gauge = wire_in.gauge
            db_wire.length = wire_in.length
            db_wire.harness_id = db_harness.id
            db.add(db_wire)
            db.flush()
            wire_map[wire_in.id] = db_wire

        for conn_data in harness_in.connections:
            from_pin_key = f"{conn_data.from_connector_id}-{conn_data.from_pin_id}"
            to_pin_key = f"{conn_data.to_connector_id}-{conn_data.to_pin_id}"

            if from_pin_key not in pin_map or to_pin_key not in pin_map:
                raise InvalidHarnessDataException("Pin not found for connection.")
            if conn_data.wire_id not in wire_map:
                raise InvalidHarnessDataException("Wire not found for connection.")

            db_connection = models.Connection()
            db_connection.harness_id = db_harness.id
            db_connection.wire_id = wire_map[conn_data.wire_id].id
            db_connection.from_pin_id = pin_map[from_pin_key].id
            db_connection.to_pin_id = pin_map[to_pin_key].id

            # Add assembly instructions
            db_connection.strip_length_a = conn_data.strip_length_a
            db_connection.strip_length_b = conn_data.strip_length_b
            db_connection.terminal_part_number_a = conn_data.terminal_part_number_a
            db_connection.terminal_part_number_b = conn_data.terminal_part_number_b
            db_connection.marking_text_a = conn_data.marking_text_a
            db_connection.marking_text_b = conn_data.marking_text_b
            db.add(db_connection)

        db.commit()
        db.refresh(db_harness)
        return db_harness
    
    def get_harness(self, db: Session, harness_id: UUID) -> models.Harness:
        db_harness = (
            db.query(models.Harness)
            .filter(models.Harness.id == harness_id)
            .options(
                joinedload(models.Harness.connectors).joinedload(models.Connector.pins),
                joinedload(models.Harness.wires),
                joinedload(models.Harness.connections).joinedload(
                    models.Connection.wire
                ),
                joinedload(models.Harness.connections)
                .joinedload(models.Connection.from_pin)
                .joinedload(models.Pin.connector),
                joinedload(models.Harness.connections)
                .joinedload(models.Connection.to_pin)
                .joinedload(models.Pin.connector),
            )
            .first()
        )

        if not db_harness:
            raise HarnessNotFoundException()
        return db_harness  # type: ignore

    def get_wire(self, db: Session, harness_id: UUID, wire_id: UUID) -> models.Wire:
        """Retrieves a single wire from a specific harness."""
        wire: models.Wire | None = (
            db.query(models.Wire)
            .filter(models.Wire.harness_id == harness_id, models.Wire.id == wire_id)
            .first()
        )
        if not wire:
            raise HarnessNotFoundException("Wire not found in this harness")
        return wire

    def generate_bom(self, db_harness: models.Harness) -> schemas.BomResponse:
        connector_bom = {}
        for conn in db_harness.connectors:
            if conn.part_number not in connector_bom:
                connector_bom[conn.part_number] = schemas.BomItem(
                    part_number=conn.part_number,
                    manufacturer=conn.manufacturer,
                    quantity=0,
                )
            connector_bom[conn.part_number].quantity += 1

        wire_bom = {}
        for wire in db_harness.wires:
            if wire.part_number not in wire_bom:
                wire_bom[wire.part_number] = schemas.BomItem(
                    part_number=wire.part_number,
                    manufacturer=wire.manufacturer,
                    quantity=0,
                )
            wire_bom[wire.part_number].quantity += 1

        return schemas.BomResponse(
            connectors=list(connector_bom.values()),
            wires=list(wire_bom.values()),
        )

    def generate_cutlist(self, db_harness: models.Harness) -> schemas.CutlistResponse:
        items = [
            schemas.CutlistItem(
                wire_id=wire.logical_id,
                part_number=wire.part_number,
                color=wire.color,
                length=wire.length,
            )
            for wire in db_harness.wires
        ]
        return schemas.CutlistResponse(items=items)

    def generate_fromto(self, db_harness: models.Harness) -> schemas.FromToResponse:
        items = []
        for conn in db_harness.connections:
            from_location = (
                f"{conn.from_pin.connector.logical_id}-{conn.from_pin.logical_id}"
            )
            to_location = f"{conn.to_pin.connector.logical_id}-{conn.to_pin.logical_id}"
            items.append(
                schemas.FromToItem(
                    wire_id=conn.wire.logical_id,
                    from_location=from_location,
                    to_location=to_location,
                )
            )
        return schemas.FromToResponse(items=items)

    def generate_formboard_pdf(self, db_harness: models.Harness) -> bytes:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # This is a placeholder for the actual drawing logic.
        # In a real implementation, you would iterate through the harness data
        # and draw the connectors and wires to scale.
        p.drawString(100, height - 100, f"Formboard for Harness: {db_harness.name}")

        # Draw a simple representation of connectors
        for i, connector in enumerate(db_harness.connectors):
            p.drawString(
                100, height - 150 - (i * 50), f"Connector: {connector.logical_id}"
            )

        # Draw a simple representation of wires
        for i, wire in enumerate(db_harness.wires):
            p.drawString(300, height - 150 - (i * 50), f"Wire: {wire.logical_id}")

        p.showPage()
        p.save()

        buffer.seek(0)
        return buffer.getvalue()


harness_service = HarnessService()