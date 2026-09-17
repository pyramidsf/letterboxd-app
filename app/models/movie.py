from sqlalchemy import Column, Integer, String, Float, Date
from app.database.connection import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True) # Para saber de quem é o filme
    
    # letterboxd data 
    title = Column(String, index=True)
    year = Column(Integer)
    user_rating = Column(Float, nullable=True)
    watch_date = Column(Date, nullable=True)
    
    # tmdb data
    director = Column(String, nullable=True)
    genres = Column(String, nullable=True) # Podemos salvar como string separada por vírgula para simplificar a v1
    country = Column(String, nullable=True)
    runtime_minutes = Column(Integer, nullable=True)
    main_cast = Column(String, nullable=True)