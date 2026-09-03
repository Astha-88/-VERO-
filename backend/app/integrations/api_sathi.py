from dataclasses import dataclass

import httpx

from app.core.config import settings

API_BASE_URL = "https://apisathi.in/gw/v1"


@dataclass
class RCVerification:
    verified: bool
    rc_number: str
    owner_name: str | None
    maker_model: str | None
    fuel_type: str | None
    registration_date: str | None
    insurance_upto: str | None
    fitness_upto: str | None
    vehicle_class: str | None


@dataclass
class Challan:
    amount: int
    status: str
    challan_no: str


class APISathiClient:
    def __init__(self) -> None:
        self.base_url = API_BASE_URL
        self.headers = {
            "X-API-Key": settings.api_sathi_api_key,
            "Content-Type": "application/json",
        }

    def verify_rc(self, rc_number: str) -> RCVerification:
        response = httpx.post(
            f"{self.base_url}/vehicle-rc-v1/",
            headers=self.headers,
            json={"rc_number": rc_number},
            timeout=15.0,
        )

        response.raise_for_status()
        data = response.json()

        return RCVerification(
            verified=data["verified"],
            rc_number=data["rc_number"],
            owner_name=data.get("owner_name"),
            maker_model=data.get("maker_model"),
            fuel_type=data.get("fuel_type"),
            registration_date=data.get("registration_date"),
            insurance_upto=data.get("insurance_upto"),
            fitness_upto=data.get("fitness_upto"),
            vehicle_class=data.get("vehicle_class"),
        )

    def get_challans(self, rc_number: str) -> list[Challan]:
        response = httpx.post(
            f"{self.base_url}/rc-challan/",
            headers=self.headers,
            json={"rc_number": rc_number},
            timeout=15.0,
        )

        response.raise_for_status()
        data = response.json()

        return [
            Challan(
                amount=challan["amount"],
                status=challan["status"],
                challan_no=challan["challan_no"],
            )
            for challan in data.get("challans", [])
        ]


api_sathi_client = APISathiClient()
