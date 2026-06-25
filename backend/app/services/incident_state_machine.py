from app.models.incident import IncidentStatus

ALLOWED_TRANSITIONS: dict[IncidentStatus, set[IncidentStatus]] = {
    IncidentStatus.open: {IncidentStatus.acknowledged, IncidentStatus.investigating},
    IncidentStatus.acknowledged: {IncidentStatus.investigating},
    IncidentStatus.investigating: {IncidentStatus.mitigated, IncidentStatus.resolved},
    IncidentStatus.mitigated: {IncidentStatus.resolved, IncidentStatus.investigating},
    IncidentStatus.resolved: set(),
}


def is_valid_transition(
    current_status: IncidentStatus, next_status: IncidentStatus
) -> bool:
    return next_status in ALLOWED_TRANSITIONS[current_status]
