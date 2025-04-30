# File: routers/chat.py

from fastapi import APIRouter, Depends, HTTPException
from tortoise.expressions import Q
from core.security import get_current_user
from models.chat import ChatMessage
from models.user import User
from schemas.chat import ChatMessageCreate, ChatMessageOut

router = APIRouter(prefix="/chat", tags=["Chat"])

# ─────────── SEND MESSAGE ───────────
@router.post("/send", response_model=ChatMessageOut)
async def send_message(data: ChatMessageCreate, current_user: User = Depends(get_current_user)):
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
@router.get("/messages/{user_id}", response_model=list[ChatMessageOut])
async def get_conversation(user_id: int, current_user: User = Depends(get_current_user)):
    messages = await ChatMessage.filter(
        Q(sender=current_user, receiver_id=user_id) | Q(sender_id=user_id, receiver=current_user)
    ).order_by("timestamp")
    return [await ChatMessageOut.from_tortoise_orm(msg) for msg in messages]

# ─────────── UNREAD COUNT ───────────
@router.get("/unread", summary="Get count of unread messages")
async def get_unread_count(current_user: User = Depends(get_current_user)):
    count = await ChatMessage.filter(receiver=current_user, is_read=False).count()
    return {"unread": count}

# ─────────── MARK AS READ ───────────
@router.post("/mark-read/{user_id}")
async def mark_as_read(user_id: int, current_user: User = Depends(get_current_user)):
    await ChatMessage.filter(
        sender_id=user_id, receiver=current_user, is_read=False
    ).update(is_read=True)
    return {"message": "Messages marked as read."}