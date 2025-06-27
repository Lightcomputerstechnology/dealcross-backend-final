# File: utils/deal_status.py

from models.deal import DealStatus

VALID_TRANSITIONS = {
    DealStatus.pending: [DealStatus.active, DealStatus.cancelled],
    DealStatus.active: [DealStatus.completed, DealStatus.disputed],
    DealStatus.disputed: [DealStatus.completed, DealStatus.cancelled],
    DealStatus.completed: [],
    DealStatus.cancelled: []
}

def is_valid_transition(current_status, new_status):
    return new_status in VALID_TRANSITIONS.get(current_status, [])
