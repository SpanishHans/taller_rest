from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from modules.db_engine import get_db
from modules.models import Usuario
from modules.schemas import UsuarioCreate,UsuarioResponse

router_users = APIRouter(tags=["Usuarios"])

# Create Usuario
@router_users.post("/registro", response_model=UsuarioResponse)
async def create_usuario(usuario: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    new_usuario = Usuario(**usuario.dict())
    db.add(new_usuario)
    await db.commit()
    await db.refresh(new_usuario)
    return new_usuario

# Read Usuario by ID
@router_users.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Update Usuario
@router_users.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(usuario_id: int, usuario_update: UsuarioCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    for key, value in usuario_update.dict().items():
        setattr(usuario, key, value)

    await db.commit()
    await db.refresh(usuario)
    return usuario

# Delete Usuario
@router_users.delete("/usuarios/{usuario_id}")
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    await db.delete(usuario)
    await db.commit()
    return {"message": f"Usuario {usuario_id} eliminado correctamente"}
