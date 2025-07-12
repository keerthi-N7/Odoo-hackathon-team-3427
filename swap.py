# app/swap.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api/swap", tags=["Swap Requests"])
from app.websocket import notify_user


# Send a swap request
@router.post("/")
async def send_swap_request(
    request: schemas.SwapRequestCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(get_current_user)
):
    new_request = models.SwapRequest(
        requester_id=current_user.id,
        target_id=request.target_id,
        skill_offered=request.skill_offered,
        skill_wanted=request.skill_wanted,
        message=request.message
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)


    await notify_user(request.target_id, f"You received a new swap request from {current_user.name}")

    return new_request



# Get all swap requests for the current user
@router.get("/")
def get_swap_requests(db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(get_current_user)):
    return db.query(models.SwapRequest).filter(
        (models.SwapRequest.requester_id == current_user.id) |
        (models.SwapRequest.target_id == current_user.id)
    ).all()

# Accept or reject a swap request
@router.put("/{request_id}")
def update_swap_request(request_id: int, status: str, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(get_current_user)):
    request = db.query(models.SwapRequest).filter(models.SwapRequest.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    if request.target_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    request.status = status
    request.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(request)
    return request
