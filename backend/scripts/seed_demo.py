from datetime import date

from app.core.database import SessionLocal
from app.models.incident import Incident
from app.models.ownership import Ownership
from app.models.service_record import ServiceRecord
from app.models.vehicle import Vehicle
from app.models.vehicle_details import VehicleDetails


def create_vehicle(
    db,
    registration_number,
    make,
    model,
    variant,
    manufacturing_year,
    fuel_type,
    owners,
    services,
    incidents,
):
    vehicle = Vehicle(registration_number=registration_number)
    db.add(vehicle)
    db.flush()

    db.add(
        VehicleDetails(
            vehicle_id=vehicle.id,
            make=make,
            model=model,
            variant=variant,
            manufacturing_year=manufacturing_year,
            fuel_type=fuel_type,
        )
    )

    for owner in owners:
        db.add(
            Ownership(
                vehicle_id=vehicle.id,
                owner_sequence=owner["sequence"],
                owner_name=owner["name"],
                purchase_date=owner.get("purchase_date"),
                transfer_date=owner.get("transfer_date"),
            )
        )

    for service in services:
        db.add(
            ServiceRecord(
                vehicle_id=vehicle.id,
                service_date=service["date"],
                service_type=service["type"],
                odometer_reading=service.get("odometer"),
                description=service.get("description"),
                service_center=service.get("center"),
                cost=service.get("cost"),
            )
        )

    for incident in incidents:
        db.add(
            Incident(
                vehicle_id=vehicle.id,
                incident_type=incident["type"],
                incident_date=incident["date"],
                severity=incident["severity"],
                description=incident.get("description"),
                reported_by=incident.get("reported_by"),
                repair_cost=incident.get("repair_cost"),
            )
        )

    return vehicle


def main():
    db = SessionLocal()

    try:
        # Clean up previous demo vehicles so the script is safe to rerun.
        demo_registrations = [
            "DL01VERO01",
            "DL01VERO02",
            "DL01VERO03",
        ]

        existing = (
            db.query(Vehicle)
            .filter(Vehicle.registration_number.in_(demo_registrations))
            .all()
        )

        for vehicle in existing:
            db.delete(vehicle)

        db.flush()

        # 🟢 GOOD VEHICLE
        good = create_vehicle(
            db=db,
            registration_number="DL01VERO01",
            make="Toyota",
            model="Camry",
            variant="2.5 Hybrid",
            manufacturing_year=2023,
            fuel_type="Hybrid",
            owners=[
                {
                    "sequence": 1,
                    "name": "First Owner",
                    "purchase_date": date(2023, 3, 15),
                }
            ],
            services=[
                {
                    "date": date(2023, 9, 10),
                    "type": "Routine Service",
                    "odometer": 8500,
                    "description": "Scheduled maintenance",
                    "center": "Toyota Authorized Service",
                    "cost": 8500,
                },
                {
                    "date": date(2024, 9, 18),
                    "type": "Routine Service",
                    "odometer": 17200,
                    "description": "Scheduled maintenance",
                    "center": "Toyota Authorized Service",
                    "cost": 9200,
                },
                {
                    "date": date(2025, 9, 22),
                    "type": "Routine Service",
                    "odometer": 26100,
                    "description": "Scheduled maintenance",
                    "center": "Toyota Authorized Service",
                    "cost": 10800,
                },
            ],
            incidents=[],
        )

        # 🟡 QUESTIONABLE VEHICLE
        questionable = create_vehicle(
            db=db,
            registration_number="DL01VERO02",
            make="Honda",
            model="City",
            variant="ZX",
            manufacturing_year=2018,
            fuel_type="Petrol",
            owners=[
                {
                    "sequence": 1,
                    "name": "First Owner",
                    "purchase_date": date(2018, 5, 12),
                    "transfer_date": date(2020, 8, 20),
                },
                {
                    "sequence": 2,
                    "name": "Second Owner",
                    "purchase_date": date(2020, 8, 20),
                    "transfer_date": date(2023, 2, 10),
                },
                {
                    "sequence": 3,
                    "name": "Current Owner",
                    "purchase_date": date(2023, 2, 10),
                },
            ],
            services=[
                {
                    "date": date(2022, 7, 15),
                    "type": "Routine Service",
                    "odometer": 42000,
                    "description": "Regular maintenance",
                    "center": "Honda Service Center",
                    "cost": 11500,
                },
                {
                    "date": date(2024, 1, 20),
                    "type": "Repair",
                    "odometer": 61000,
                    "description": "Brake and suspension repair",
                    "center": "Independent Service Center",
                    "cost": 28500,
                },
            ],
            incidents=[
                {
                    "type": "Road Accident",
                    "date": date(2022, 11, 4),
                    "severity": "moderate",
                    "description": "Front-end collision reported.",
                    "reported_by": "Insurance Provider",
                    "repair_cost": 65000,
                }
            ],
        )

        # 🔴 HIGH-RISK VEHICLE
        risky = create_vehicle(
            db=db,
            registration_number="DL01VERO03",
            make="Ford",
            model="EcoSport",
            variant="Titanium",
            manufacturing_year=2015,
            fuel_type="Diesel",
            owners=[
                {
                    "sequence": 1,
                    "name": "First Owner",
                    "purchase_date": date(2015, 4, 10),
                    "transfer_date": date(2017, 6, 12),
                },
                {
                    "sequence": 2,
                    "name": "Second Owner",
                    "purchase_date": date(2017, 6, 12),
                    "transfer_date": date(2019, 9, 5),
                },
                {
                    "sequence": 3,
                    "name": "Third Owner",
                    "purchase_date": date(2019, 9, 5),
                    "transfer_date": date(2022, 1, 18),
                },
                {
                    "sequence": 4,
                    "name": "Current Owner",
                    "purchase_date": date(2022, 1, 18),
                },
            ],
            services=[
                {
                    "date": date(2023, 3, 11),
                    "type": "Major Repair",
                    "odometer": 98000,
                    "description": "Major mechanical repair",
                    "center": "Independent Garage",
                    "cost": 78000,
                }
            ],
            incidents=[
                {
                    "type": "Major Accident",
                    "date": date(2021, 8, 27),
                    "severity": "severe",
                    "description": "Major collision with extensive front-end damage.",
                    "reported_by": "Insurance Provider",
                    "repair_cost": 185000,
                }
            ],
        )

        db.commit()

        print("Demo vehicles created successfully:")
        print(f"  GOOD:         {good.id} - {good.registration_number}")
        print(
            f"  QUESTIONABLE: {questionable.id} - "
            f"{questionable.registration_number}"
        )
        print(f"  HIGH RISK:    {risky.id} - {risky.registration_number}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
