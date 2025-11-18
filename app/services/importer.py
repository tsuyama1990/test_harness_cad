# app/services/importer.py

import io
from typing import IO, cast

import ezdxf
from ezdxf.document import Drawing
from ezdxf.entities import Insert
from sqlalchemy.orm import Session

from app import models
from app.services.catalog import CatalogService, catalog_service


class ImporterService:
    def __init__(self, catalog_service: CatalogService):
        self.catalog_service = catalog_service

    def import_dxf(
        self, db: Session, dxf_file: IO[bytes], project_id: int
    ) -> models.Harness:
        """
        Parses a DXF file to import connectors and create a new harness.
        """
        doc: Drawing
        try:
            # Attempt to read the DXF file with UTF-8 encoding
            doc = ezdxf.read(io.TextIOWrapper(dxf_file, encoding="utf-8"))
        except UnicodeDecodeError:
            # If UTF-8 fails, reset stream and try with a common legacy encoding
            dxf_file.seek(0)
            doc = ezdxf.read(io.TextIOWrapper(dxf_file, encoding="cp1252"))
        msp = doc.modelspace()

        # Create a new Harness to host the imported components
        db_harness = models.Harness(name="Imported Harness")
        db.add(db_harness)
        db.flush()

        imported_connectors = []
        # Find all block references (INSERT entities) in the modelspace
        for block_ref in msp.query("INSERT"):
            if not isinstance(block_ref, Insert):
                continue
            insert_entity = cast(Insert, block_ref)
            part_number = insert_entity.get_attrib_text("PART_NUMBER")
            ref_des = insert_entity.get_attrib_text("REF_DES")

            if not part_number or not ref_des:
                continue  # Skip blocks that don't have the required attributes

            db_connector = models.Connector(
                logical_id=ref_des,
                manufacturer="Unknown",  # Manufacturer is not in the DXF
                part_number=part_number,
                harness_id=db_harness.id,
            )
            db.add(db_connector)
            db.flush()

            # Enrich with catalog data
            spec = self.catalog_service.get_specification(part_number)
            if spec:
                db_connector.voltage_rating = spec.get("voltage_rating")
                db_connector.applicable_wire_max_diameter = spec.get(
                    "applicable_wire_max_diameter"
                )
                db_connector.is_rohs = spec.get("is_rohs")
                db_connector.is_ul = spec.get("is_ul")

                # Create pins based on catalog data
                pin_data = spec.get("pins")
                if pin_data:
                    for i in range(pin_data["pin_count"]):
                        db_pin = models.Pin(
                            logical_id=str(i + 1),
                            connector_id=db_connector.id,
                        )
                        db.add(db_pin)

            imported_connectors.append(db_connector)

        db.commit()
        db.refresh(db_harness)

        # Associate the new harness with the project via HarnessDesign
        harness_design = models.HarnessDesign(
            project_id=project_id, harness_id=db_harness.id
        )
        db.add(harness_design)
        db.commit()

        return db_harness


importer_service = ImporterService(catalog_service=catalog_service)
