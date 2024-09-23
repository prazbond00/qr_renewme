from sqlalchemy import create_engine, Column, String, Integer, Date, DECIMAL, ForeignKey, Text # type: ignore
from sqlalchemy.orm import relationship, declarative_base, sessionmaker # type: ignore

# Create engine and Base
engine = create_engine('mysql+pymysql://root:123456789@localhost:3306/renewme', echo=True)
Base = declarative_base()

# Farmer Model
class Farmer(Base):
    __tablename__ = 'farmers'
    id = Column(Integer, primary_key=True)
    farmer_name = Column(String(255), nullable=False)
    farmer_debut = Column(Date)
    intro_vdo = Column(String(255))
    labour_time = Column(Integer)
    farmer_story = Column(Text)
    farmer_photo = Column(String(255))
    labour_cost = Column(DECIMAL(10, 2))

    project = relationship("Project", back_populates="farmer", uselist=False)

# Store Model
class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True)
    store_name = Column(String(255), nullable=False)
    store_location = Column(String(255))
    store_photo = Column(String(255))

    project = relationship("Project", back_populates="store", uselist=False)

# Project Model
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    project_name = Column(String(255), nullable=False)
    project_location = Column(String(255))
    project_altitude = Column(DECIMAL(8, 2))
    variety_of_crop = Column(String(255))
    carbon_emission = Column(DECIMAL(10, 2))
    product_visit_count = Column(Integer)

    farmer_id = Column(Integer, ForeignKey('farmers.id'))
    store_id = Column(Integer, ForeignKey('stores.id'))
    crop_id = Column(Integer, ForeignKey('crops.id'))

    farmer = relationship("Farmer", back_populates="project")
    store = relationship("Store", back_populates="project")
    crop = relationship("Crop", back_populates="projects")

# Crop Model
class Crop(Base):
    __tablename__ = 'crops'
    id = Column(Integer, primary_key=True)
    crop_name = Column(String(255), nullable=False)
    seed_type = Column(String(255))
    manu_fac_date = Column(Date)
    harvesting_time = Column(Date)
    intro_vdo = Column(String(255))
    product_desc = Column(Text)
    product_photo = Column(String(255))
    production_cost = Column(DECIMAL(10, 2))

    projects = relationship("Project", back_populates="crop")
    crop_phases = relationship("CropPhase", back_populates="crop")

# Crop Phase Model
class CropPhase(Base):
    __tablename__ = 'crop_phases'
    id = Column(Integer, primary_key=True)
    phase_name = Column(String(255))
    phase_desc = Column(Text)
    photo_phases = Column(String(255))

    crop_id = Column(Integer, ForeignKey('crops.id'))
    pest_id = Column(Integer, ForeignKey('pesticides.id'))

    crop = relationship("Crop", back_populates="crop_phases")
    pesticide = relationship("Pesticide", back_populates="crop_phases")

# Pesticide Model
class Pesticide(Base):
    __tablename__ = 'pesticides'
    id = Column(Integer, primary_key=True)
    pest_name = Column(String(255))
    pest_type = Column(String(255))
    DOU = Column(Date)
    pest_quantity = Column(DECIMAL(10, 2))
    pest_method_of_use = Column(Text)
    pest_photo = Column(String(255))

    crop_phases = relationship("CropPhase", back_populates="pesticide")

# Create tables
Base.metadata.create_all(engine)

from fastapi import FastAPI # type: ignore

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the RenewMe API"}
