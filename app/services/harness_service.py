from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.exceptions import HarnessNotFoundException, InvalidHarnessDataException


class HarnessService:
    def create_harness(
        self, db: Session, harness_in: schemas.HarnessCreate
    ) -> models.Harness:
        # Create Harness
        db_harness = models.Harness(name=harness_in.name)
        db.add(db_harness)
        db.flush()

        # Create Connectors and Pins
        connector_map = {}
        pin_map = {}
        for conn_in in harness_in.connectors:
            db_conn = models.Connector(
                logical_id=conn_in.id,
                manufacturer=conn_in.manufacturer,
                part_number=conn_in.part_number,
                harness_id=db_harness.id,
            )
            db.add(db_conn)
            db.flush()
            connector_map[conn_in.id] = db_conn
            for pin_in in conn_in.pins:
                db_pin = models.Pin(logical_id=pin_in.id, connector_id=db_conn.id)
                db.add(db_pin)
                db.flush()
                pin_map[f"{conn_in.id}-{pin_in.id}"] = db_pin

        # Create Wires
        wire_map = {}
        for wire_in in harness_in.wires:
            db_wire = models.Wire(
                logical_id=wire_in.id,
                manufacturer=wire_in.manufacturer,
                part_number=wire_in.part_number,
                color=wire_in.color,
                gauge=wire_in.gauge,
                length=wire_in.length,
                harness_id=db_harness.id,
            )
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

            db_connection = models.Connection(
                harness_id=db_harness.id,
                wire_id=wire_map[conn_data.wire_id].id,
                from_pin_id=pin_map[from_pin_key].id,
                to_pin_id=pin_map[to_pin_key].id,
            )
            db.add(db_connection)

        db.commit()
        db.refresh(db_harness)
        return db_harness

    def get_harness(self, db: Session, harness_id: UUID) -> models.Harness:
        db_harness = (
            db.query(models.Harness)
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
            .filter(models.Harness.id == harness_id)
            .first()
        )

        if not db_harness:
            raise HarnessNotFoundException()
        return db_harness

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


harness_service = HarnessService()
