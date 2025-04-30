# File: routers/chat.py

from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist
from models.chat import ChatMessage
from models.user import User
from schemas.chat import ChatMessageCreate, ChatMessageOut
from core.security import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

# Send message
@router.post("/send", response_model=ChatMessageOut)
async def send_message(
    msg: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
):
    message = await ChatMessage.create(
        sender=current_user,
        receiver_id=msg.receiver_id,
        content=msg.content,
        deal_id=msg.deal_id
    )
    return await ChatMessageOut.model_validate(message)

# Get chat messages between two users
@router.get("/messages/{user_id}", response_model=list[ChatMessageOut])
async def get_conversation(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    messages = await ChatMessage.filter(
        (fields.Q(sender_id=current_user.id) & fields.Q(receiver_id=user_id)) |
        (fields.Q(sender_id=user_id) & fields.Q(receiver_id=current_user.id))
    ).order_by("timestamp")
    return await ChatMessageOut.model_validate(messages, many=True)

# Mark all as read
@router.post("/mark-read/{user_id}")
async def mark_read(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    await ChatMessage.filter(sender_id=user_id, receiver_id=current_user.id, is_read=False).update(is_read=True)
    return {"message": "Messages marked as read."}

# Count unread
@router.get("/unread/{user_id}")
async def count_unread(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    count = await ChatMessage.filter(sender_id=user_id, receiver_id=current_user.id, is_read=False).count()
    return {"unread_count": count}