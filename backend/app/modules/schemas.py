from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# --- Usuario ---
class UsuarioBase(BaseModel):
    ubicacion: Optional[str] = Field(
        None, json_schema_extra={'examples': ['Bogotá, Colombia']}
    )
    edad: Optional[int] = Field(
        None, json_schema_extra={'examples': [25]}
    )

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int = Field(
        json_schema_extra={'examples': [1]}
    )
    class Config:
        from_attributes = True


# --- Libro ---
class LibroBase(BaseModel):
    titulo: Optional[str] = Field(
        None, json_schema_extra={'examples': ['Jane Doe']}
    )
    autor: Optional[str] = Field(
        None, json_schema_extra={'examples': ['R. J. Kaiser']}
    )
    publicado_en: Optional[int] = Field(
        None, json_schema_extra={'examples': [1999]}
    )
    publicado_por: Optional[str] = Field(
        None, json_schema_extra={'examples': ['Mira Books']}
    )
    url_s: Optional[str] = Field(
        None, json_schema_extra={'examples': ['http://images.amazon.com/images/P/1552041778.01.THUMBZZZ.jpg']}
    )
    url_m: Optional[str] = Field(
        None, json_schema_extra={'examples': ['http://images.amazon.com/images/P/1552041778.01.MZZZZZZZ.jpg']}
    )
    url_l: Optional[str] = Field(
        None, json_schema_extra={'examples': ['http://images.amazon.com/images/P/1552041778.01.LZZZZZZZ.jpg']}
    )

class LibroCreate(LibroBase):
    isbn: str = Field(
        json_schema_extra={'examples': ['978-3-16-148410-0']}
    )

class LibroResponse(LibroBase):
    isbn: str = Field(
        json_schema_extra={'examples': ['978-3-16-148410-0']}
    )
    class Config:
        from_attributes = True


# --- Review ---
class ReviewBase(BaseModel):
    nota: Optional[int] = Field(
        None, json_schema_extra={'examples': [4]}
    )

class ReviewCreate(ReviewBase):
    user_id: int = Field(
        json_schema_extra={'examples': [1]}
    )
    isbn: str = Field(
        json_schema_extra={'examples': ['978-3-16-148410-0']}
    )

class ReviewResponse(ReviewBase):
    id: int = Field(
        json_schema_extra={'examples': [10]}
    )
    user_id: int = Field(
        json_schema_extra={'examples': [1]}
    )
    isbn: str = Field(
        json_schema_extra={'examples': ['978-3-16-148410-0']}
    )
    class Config:
        from_attributes = True
