from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import engine, Base, get_db
from app.scrapers.letterboxd import scrape_letterboxd_rss


Base.metadata.create_all(bind=engine) #tabelas do banco 

app = FastAPI(
    title="Letterboxd Insights",
    description="API para analisar perfis do Letterboxd e gerar estatísticas.",
    version="1.0.0"
)

@app.post("/analyze/{username}")
async def analyze_profile(username: str, db: Session = Depends(get_db)):
    """
    Fluxo principal da aplicação:
    1. Scraper do Letterboxd
    2. Consulta ao TMDb
    3. Salvar no banco
    4. Gerar estatísticas
    """
    
    try:
        movies = await scrape_letterboxd_rss(username)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    rated_movies = [movie for movie in movies if movie["user_rating"] is not None]
    average_rating = (
        round(sum(movie["user_rating"] for movie in rated_movies) / len(rated_movies), 2)
        if rated_movies else None
    )

    return {
        "username": username,
        "movies_found": len(movies),
        "average_rating": average_rating,
        "movies": movies,
    }

@app.get("/stats/{username}")
async def get_stats(username: str, db: Session = Depends(get_db)):
    """
    Retorna as estatísticas geradas pelo Pandas.
    """
    # TODO: integrar app/services/stats.py
    return {"message": f"Estatísticas do usuário {username} estarão aqui."}