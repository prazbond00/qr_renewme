from PythonORM import Farmer, engine
from fastapi import FastAPI, HTTPException, Depends # type: ignore
from sqlalchemy.orm import Session, sessionmaker # type: ignore
from sqlalchemy.exc import SQLAlchemyError # type: ignore
from pydantic import BaseModel, constr # type: ignore

app = FastAPI()

# Database session creation
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pydantic model for input validation
class FarmerCreate(BaseModel):
    farmer_name: constr(min_length=1, max_length=255) # type: ignore

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a farmer
@app.post("/farmers/")
async def create_farmer(farmer_data: FarmerCreate, db: Session = Depends(get_db)):
    new_farmer = Farmer(farmer_name=farmer_data.farmer_name)
    db.add(new_farmer)
    try:
        db.commit()
        db.refresh(new_farmer)  # Refresh to get the ID of the newly created farmer
        return {"message": "Farmer created successfully", "farmer_id": new_farmer.id}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the farmer")

# Endpoint to retrieve all farmers
@app.get("/farmers/")
async def get_farmers(db: Session = Depends(get_db)):
    try:
        farmers = db.query(Farmer).all()
        return farmers
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="An error occurred while fetching farmers")

# Endpoint to retrieve a specific farmer by ID
@app.get("/farmers/{farmer_id}")
async def get_farmer(farmer_id: int, db: Session = Depends(get_db)):
    try:
        farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
        if farmer is None:
            raise HTTPException(status_code=404, detail="Farmer not found")
        return farmer
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="An error occurred while fetching the farmer")
