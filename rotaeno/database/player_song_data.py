import os
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Index
from sqlalchemy.dialects.sqlite import insert


Base = declarative_base()


class PlayerSongScore:
    def __init__(self, song_id: str, object_id: str, difficulty: str, score: int, rating: float = 0.0):
        self.song_id = song_id
        self.object_id = object_id
        self.difficulty = difficulty
        self.score = score
        self.rating = rating


class Latest(Base):
    __tablename__ = "player_song_latest"

    id = Column(Integer, primary_key=True, autoincrement=True)

    song_id = Column(String, nullable=False)
    object_id = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)

    score = Column(Integer, nullable=False)
    rating = Column(Float, nullable=True)

    __table_args__ = (
        Index("idx_latest_unique", "song_id", "object_id", "difficulty", unique=True),
    )


class History(Base):
    __tablename__ = "player_song_history"

    id = Column(Integer, primary_key=True, autoincrement=True)

    timestamp = Column(DateTime, nullable=False, index=True, default=datetime.now)

    song_id = Column(String, nullable=False, index=True)
    object_id = Column(String, nullable=False, index=True)
    difficulty = Column(String, nullable=False)

    score = Column(Integer, nullable=False)
    rating = Column(Float, nullable=True)


class PlayerSongData:
    def __init__(self, db_path: str):
        self.engine = create_engine(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False}
        )

        with self.engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
            conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")
            conn.exec_driver_sql("PRAGMA cache_size=10000;")

        Base.metadata.create_all(self.engine)

        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def add_score(self, score: PlayerSongScore, timestamp: datetime = None):
        session = self.Session()
        try:
            stmt = insert(Latest).values(
                song_id=score.song_id,
                object_id=score.object_id,
                difficulty=score.difficulty,
                score=score.score,
                rating=score.rating
            ).on_conflict_do_update(
                index_elements=["song_id", "object_id", "difficulty"],
                set_={
                    "score": score.score,
                    "rating": score.rating
                }
            )

            session.execute(stmt)

            if timestamp is None:
                timestamp = datetime.now()

            history = History(
                timestamp=timestamp,
                song_id=score.song_id,
                object_id=score.object_id,
                difficulty=score.difficulty,
                score=score.score,
                rating=score.rating
            )

            session.add(history)

            session.commit()

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_latest(self, song_id: str, object_id: str, difficulty: str) -> dict | None:
        session = self.Session()
        try:
            row = session.query(Latest).filter_by(
                song_id=song_id,
                object_id=object_id,
                difficulty=difficulty
            ).first()

            return None if row is None else dict(
                song_id=row.song_id,
                object_id=row.object_id,
                difficulty=row.difficulty,
                score=row.score,
                rating=row.rating
            )
        finally:
            session.close()

    def get_history(self, song_id: str, object_id: str, difficulty: str, limit: int = 50) -> list[dict]:
        session = self.Session()
        try:
            rows = (
                session.query(History)
                .filter_by(
                    song_id=song_id,
                    object_id=object_id,
                    difficulty=difficulty
                )
                .order_by(History.timestamp.desc())
                .limit(limit)
                .all()
            )

            return [
                dict(
                    timestamp=row.timestamp,
                    song_id=row.song_id,
                    object_id=row.object_id,
                    difficulty=row.difficulty,
                    score=row.score,
                    rating=row.rating
                )
                for row in rows
            ]
        finally:
            session.close()

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "player_song.db")

player_song_data = PlayerSongData(db_path)