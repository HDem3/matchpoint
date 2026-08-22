import os
from datetime import datetime
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, Float, ForeignKey, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

URL = os.getenv("DATABASE_URL", "sqlite:///./matchpoint.db")
engine = create_engine(URL, connect_args={"check_same_thread": False} if URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
class Base(DeclarativeBase): pass

class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    city: Mapped[str] = mapped_column(String(80), index=True)
    level: Mapped[float] = mapped_column(Float, default=3.0)

class Match(Base):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(primary_key=True)
    player_one_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player_two_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)
    venue: Mapped[str] = mapped_column(String(120))
    score: Mapped[str | None] = mapped_column(String(80), nullable=True)

Base.metadata.create_all(engine)
app = FastAPI(title="MatchPoint API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
def db():
    session = SessionLocal()
    try: yield session
    finally: session.close()

class PlayerIn(BaseModel):
    name: str = Field(min_length=2); city: str = Field(min_length=2); level: float = Field(ge=1, le=5)
class PlayerOut(PlayerIn):
    id: int; model_config = ConfigDict(from_attributes=True)
class MatchIn(BaseModel):
    player_one_id: int; player_two_id: int; scheduled_at: datetime; venue: str = Field(min_length=2)
class MatchOut(MatchIn):
    id: int; score: str | None; model_config = ConfigDict(from_attributes=True)
class ScoreIn(BaseModel): score: str = Field(pattern=r"^\d+-\d+(,\s*\d+-\d+)*$")

@app.get("/health")
def health(): return {"status": "ok"}
@app.get("/players", response_model=list[PlayerOut])
def players(session: Session = Depends(db)): return session.scalars(select(Player).order_by(Player.name)).all()
@app.post("/players", response_model=PlayerOut, status_code=201)
def add_player(data: PlayerIn, session: Session = Depends(db)):
    player = Player(**data.model_dump()); session.add(player); session.commit(); session.refresh(player); return player
@app.get("/players/{player_id}/suggestions", response_model=list[PlayerOut])
def suggestions(player_id: int, session: Session = Depends(db)):
    player = session.get(Player, player_id)
    if not player: raise HTTPException(404, "Player not found")
    candidates = session.scalars(select(Player).where(Player.id != player.id, Player.city == player.city)).all()
    return sorted(candidates, key=lambda p: abs(p.level-player.level))[:5]
@app.get("/matches", response_model=list[MatchOut])
def matches(session: Session = Depends(db)): return session.scalars(select(Match).order_by(Match.scheduled_at)).all()
@app.post("/matches", response_model=MatchOut, status_code=201)
def add_match(data: MatchIn, session: Session = Depends(db)):
    if data.player_one_id == data.player_two_id: raise HTTPException(422, "Choose two different players")
    if not session.get(Player, data.player_one_id) or not session.get(Player, data.player_two_id): raise HTTPException(404, "Player not found")
    match = Match(**data.model_dump()); session.add(match); session.commit(); session.refresh(match); return match
@app.patch("/matches/{match_id}/score", response_model=MatchOut)
def add_score(match_id: int, data: ScoreIn, session: Session = Depends(db)):
    match = session.get(Match, match_id)
    if not match: raise HTTPException(404, "Match not found")
    match.score = data.score; session.commit(); session.refresh(match); return match


