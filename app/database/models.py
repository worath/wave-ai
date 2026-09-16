from sqlalchemy import Column, Integer, String
from app.database.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    code = Column(String, unique=True, nullable=False)

    category = Column(String, nullable=False)

    price = Column(Integer, nullable=False, default=0)