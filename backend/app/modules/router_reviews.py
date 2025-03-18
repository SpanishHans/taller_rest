from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from modules.db_engine import get_db
from modules.models import Review
from modules.schemas import ReviewCreate, ReviewResponse

router_reviews = APIRouter(tags=["Reviews"])

# Create Review
@router_reviews.post("/review", response_model=ReviewResponse)
async def create_review(review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    new_review = Review(**review.dict())
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review

# Read Review by ID
@router_reviews.get("/reviews/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=404, detail="Review no encontrado")
    return review

# Update Review
@router_reviews.put("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(review_id: int, review_update: ReviewCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=404, detail="Review no encontrado")

    for key, value in review_update.dict().items():
        setattr(review, key, value)

    await db.commit()
    await db.refresh(review)
    return review

# Delete Review
@router_reviews.delete("/reviews/{review_id}")
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if review is None:
        raise HTTPException(status_code=404, detail="Review no encontrado")

    await db.delete(review)
    await db.commit()
    return {"message": f"Review {review_id} eliminado correctamente"}
