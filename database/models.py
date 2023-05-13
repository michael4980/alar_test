from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Data1(Base):
    __tablename__ = 'data_1'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def as_dict(self):
        return {'id': self.id,
                'name': self.name}


class Data2(Base):
    __tablename__ = 'data_2'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def as_dict(self):
        return {'id': self.id,
                'name': self.name}


class Data3(Base):
    __tablename__ = 'data_3'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def as_dict(self):
        return {'id': self.id,
                'name': self.name}
