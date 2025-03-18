from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends, Query

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from modules.db_engine import get_db
from modules.models import Libro
from modules.schemas import LibroCreate,LibroResponse

router_libros = APIRouter(tags=["Libros"])

# Create Libro
@router_libros.post("/nuevo_libro", response_model=LibroResponse)
async def create_libro(libro: LibroCreate, db: AsyncSession = Depends(get_db)):
    new_libro = Libro(**libro.dict())
    db.add(new_libro)
    await db.commit()
    await db.refresh(new_libro)
    return new_libro

# Read Libro by ID
@router_libros.get("/isbn/{libro_id}", response_model=LibroResponse)
async def get_libro(libro_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Libro).where(Libro.isbn == libro_id))
    libro = result.scalar_one_or_none()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro
    
@router_libros.get("/libros", response_model=List[LibroResponse])
async def get_libros(
    start_date: Optional[int] = Query(None),
    end_date: Optional[int] = Query(None),
    publisher: Optional[str] = Query(None),
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    query = select(Libro)

    if start_date:
        query = query.where(Libro.publicado_en >= start_date)
    if end_date:
        query = query.where(Libro.publicado_en <= end_date)
    if publisher:
        query = query.where(Libro.publicado_por == publisher)

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    libros = result.scalars().all()
    return libros

# Update Libro
@router_libros.put("/isbn/{libro_id}", response_model=LibroResponse)
async def update_libro(libro_id: str, libro_update: LibroCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Libro).where(Libro.isbn == libro_id))
    libro = result.scalar_one_or_none()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    for key, value in libro_update.dict().items():
        setattr(libro, key, value)

    await db.commit()
    await db.refresh(libro)
    return libro

# Delete Libro
@router_libros.delete("/isbn/{libro_id}")
async def delete_libro(libro_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Libro).where(Libro.isbn == libro_id))
    libro = result.scalar_one_or_none()
    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    await db.delete(libro)
    await db.commit()
    return {"message": f"Libro {libro_id} eliminado correctamente"}
