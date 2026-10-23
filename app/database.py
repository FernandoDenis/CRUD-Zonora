from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./zonora.db"

engine = create_engine(DATABASE_URL)

