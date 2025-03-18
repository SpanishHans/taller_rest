from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from modules.base import Base

# https://www.kaggle.com/datasets/saurabhbagchi/books-dataset

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ubicacion: Mapped[str] = mapped_column(nullable=True)
    edad: Mapped[int] = mapped_column(nullable=True)

    # Relación con reviews
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="usuario")


class Libro(Base):
    __tablename__ = "libros"

    isbn: Mapped[str] = mapped_column(primary_key=True, unique=True, index=True)
    titulo: Mapped[str] = mapped_column(nullable=True)
    autor: Mapped[str] = mapped_column(nullable=True)
    publicado_en: Mapped[int] = mapped_column(nullable=True)
    publicado_por: Mapped[str] = mapped_column(nullable=True)
    url_s: Mapped[str] = mapped_column(nullable=True)
    url_m: Mapped[str] = mapped_column(nullable=True)
    url_l: Mapped[str] = mapped_column(nullable=True)

    # Relación con reviews
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="libro")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    isbn: Mapped[str] = mapped_column(ForeignKey("libros.isbn"), nullable=False)
    nota: Mapped[int] = mapped_column(nullable=True)

    # Relaciones inversas
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="reviews")
    libro: Mapped["Libro"] = relationship("Libro", back_populates="reviews")
