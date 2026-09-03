from app.integrations.api_sathi import api_sathi_client


def normalize_registration_number(registration_number: str) -> str:
    return registration_number.strip().upper()


def get_external_vehicle_data(registration_number: str) -> dict:
    rc_number = normalize_registration_number(registration_number)

    rc = api_sathi_client.verify_rc(rc_number)
    challans = api_sathi_client.get_challans(rc_number)

    return {
        "registration_number": rc.rc_number,
        "source": "api_sathi",
        "registration": {
            "verified": rc.verified,
            "registration_date": rc.registration_date,
            "vehicle_class": rc.vehicle_class,
            "fitness_upto": rc.fitness_upto,
        },
        "vehicle": {
            "owner_name": rc.owner_name,
            "maker_model": rc.maker_model,
            "fuel_type": rc.fuel_type,
        },
        "insurance": {
            "insurance_upto": rc.insurance_upto,
        },
        "compliance": {
            "challans": [
                {
                    "challan_no": challan.challan_no,
                    "amount": challan.amount,
                    "status": challan.status,
                }
                for challan in challans
            ]
        },
        "data_limitations": [
            "Ownership history is not available from this source.",
            "Insurance claim history is not available from this source.",
            "Accident history is not available from this source.",
            "Service and maintenance history is not available from this source.",
        ],
    }
