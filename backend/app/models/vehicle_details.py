from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class VehicleDetails(Base):
    __tablename__ = "vehicle_details"

    id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        unique=True,
        nullable=False,
        index=True,
    )

    make: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    variant: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    manufacturing_year: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    fuel_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
