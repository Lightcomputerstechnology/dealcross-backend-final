from pydantic import BaseModel

class EscrowStatusUpdate(BaseModel):
    deal_id: int
    status: str  # e.g., 'funded', 'delivered', 'released', 'disputed'

    model_config = {"from_attributes": True}


class EscrowTrackerOut(BaseModel):
    id: int
    deal_id: int
    status: str
    updated_at: str  # ISO format

    model_config = {"from_attributes": True}
