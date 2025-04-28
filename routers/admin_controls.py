Admin Controls - Block Users & Deal Approval (Tortoise ORM Version)

from fastapi import APIRouter, Depends, HTTPException from models.user import User from models.deal import Deal from schemas.admin_controls import BlockAction, DealApproval

router = APIRouter()

GET all users

@router.get("/users") async def get_users(): return await User.all()

Block a user

@router.post("/users/block") async def block_user(data: BlockAction): user = await User.get_or_none(id=data.user_id) if not user: raise HTTPException(status_code=404, detail="User not found") user.is_blocked = True user.block_reason = data.reason await user.save() return {"message": "User blocked successfully."}

Unblock a user

@router.post("/users/unblock") async def unblock_user(data: BlockAction): user = await User.get_or_none(id=data.user_id) if not user: raise HTTPException(status_code=404, detail="User not found") user.is_blocked = False user.block_reason = None await user.save() return {"message": "User unblocked successfully."}

Approve a deal

@router.post("/deals/approve") async def approve_deal(data: DealApproval): deal = await Deal.get_or_none(id=data.deal_id) if not deal: raise HTTPException(status_code=404, detail="Deal not found") deal.status = "approved" deal.approval_note = data.note await deal.save() return {"message": "Deal approved."}

Reject a deal

@router.post("/deals/reject") async def reject_deal(data: DealApproval): deal = await Deal.get_or_none(id=data.deal_id) if not deal: raise HTTPException(status_code=404, detail="Deal not found") deal.status = "rejected" deal.approval_note = data.note await deal.save() return {"message": "Deal rejected."}

