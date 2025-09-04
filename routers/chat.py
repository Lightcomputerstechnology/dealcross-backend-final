# File: routers/chat.py

from typing import Dict, Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException
from tortoise.expressions import Q

from core.security import get_current_user
from models.chat import ChatMessage
from models.user import User
from schemas.chat import ChatMessageCreate, ChatMessageOut

router = APIRouter(prefix="/chat", tags=["Chat"])


# ─────────── MAP AUTH → DB USER ───────────
async def resolve_db_user(claims: Dict[str, Any] = Depends(get_current_user)) -> User:
    email: Optional[str] = claims.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Authenticated token missing email claim")
    user = await User.get_or_none(email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User record not found for this account")
    return user


# ─────────── SEND MESSAGE ───────────
@router.post("/send", response_model=ChatMessageOut)
async def send_message(
    data: ChatMessageCreate,
    current_user: User = Depends(resolve_db_user)
):
    if data.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot message yourself.")

    message = await ChatMessage.create(
        sender=current_user,
        receiver_id=data.receiver_id,
        content=data.content,
        deal_id=data.deal_id,
    )
    return await ChatMessageOut.from_tortoise_orm(message)


# ─────────── GET CONVERSATION ───────────
@router.get("/messages/{user_id}", response_model=List[ChatMessageOut])
async def get_conversation(
    user_id: int,
    current_user: User = Depends(resolve_db_user)
):
    messages = await ChatMessage.filter(
        Q(sender_id=current_user.id, receiver_id=user_id) |
        Q(sender_id=user_id, receiver_id=current_user.id)
    ).order_by("timestamp")

    return [await ChatMessageOut.from_tortoise_orm(msg) for msg in messages]


# ─────────── UNREAD COUNT ───────────
@router.get("/unread", summary="Get count of unread messages")
async def get_unread_count(
    current_user: User = Depends(resolve_db_user)
):
    count = await ChatMessage.filter(
        receiver_id=current_user.id,
        is_read=False
    ).count()
    return {"unread": count}


# ─────────── MARK AS READ ───────────
@router.post("/mark-read/{user_id}")
async def mark_as_read(
    user_id: int,
    current_user: User = Depends(resolve_db_user)
):
    await ChatMessage.filter(
        sender_id=user_id,
        receiver_id=current_user.id,
        is_read=False
    ).update(is_read=True)
    return {"message": "Messages marked as read."}
