from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models.due_diligence_step import DueDiligenceStep


def complete_step(
    db: Session,
    vehicle_id: int,
    step_type: str,
    source: str | None = None,
    cost: float | None = None,
    notes: str | None = None,
) -> DueDiligenceStep:
    existing_step = (
        db.query(DueDiligenceStep)
        .filter(
            DueDiligenceStep.vehicle_id == vehicle_id,
            DueDiligenceStep.step_type == step_type,
        )
        .first()
    )

    if existing_step is not None:
        return existing_step

    now = datetime.now(UTC)

    step = DueDiligenceStep(
        vehicle_id=vehicle_id,
        step_type=step_type,
        status="completed",
        source=source,
        cost=cost,
        notes=notes,
        started_at=now,
        completed_at=now,
    )

    db.add(step)
    db.commit()
    db.refresh(step)

    return step


def record_unavailable_step(
    db: Session,
    vehicle_id: int,
    step_type: str,
    source: str | None = None,
    notes: str | None = None,
) -> DueDiligenceStep:
    existing_step = (
        db.query(DueDiligenceStep)
        .filter(
            DueDiligenceStep.vehicle_id == vehicle_id,
            DueDiligenceStep.step_type == step_type,
        )
        .first()
    )

    if existing_step is not None:
        return existing_step

    now = datetime.now(UTC)

    step = DueDiligenceStep(
        vehicle_id=vehicle_id,
        step_type=step_type,
        status="unavailable",
        source=source,
        notes=notes,
        started_at=now,
        completed_at=now,
    )

    db.add(step)
    db.commit()
    db.refresh(step)

    return step


def get_vehicle_steps(
    db: Session,
    vehicle_id: int,
) -> list[DueDiligenceStep]:
    return (
        db.query(DueDiligenceStep)
        .filter(DueDiligenceStep.vehicle_id == vehicle_id)
        .order_by(DueDiligenceStep.created_at.asc())
        .all()
)
