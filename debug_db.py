import uuid
from app.db.session import SessionLocal
from app.models.harness import Harness


def main():
    db = SessionLocal()
    harnesses = db.query(Harness).all()
    print("Harnesses in DB:")
    for h in harnesses:
        print(h.id, h.name)

    harness_id = uuid.UUID("0a9eb930-c504-4835-a281-3e5c1800e1d1")
    harness = db.query(Harness).filter(Harness.id == harness_id).first()
    print(f"Harness found: {harness}")


if __name__ == "__main__":
    main()
