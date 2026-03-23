from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import joblib
import pandas as pd
import os

from database import init_db, get_db_connection
from auth import get_password_hash, verify_password, create_access_token, get_current_user, get_optional_current_user

app = FastAPI(title="ImpactSense API")

# Initialize SQLite database schema
init_db()

# Setup CORS to allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the pipeline on startup
try:
    pipeline_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "notebooks", "earthquake_pipeline.pkl"))
    pipeline = joblib.load(pipeline_path)
    model = pipeline["model"]
    scaler = pipeline["scaler"]
    encoder = pipeline["encoder"]
    features = pipeline["features"]
    print(f"Pipeline loaded successfully with features: {features}")
except Exception as e:
    import traceback
    print(f"Error loading pipeline: {e}")
    print(traceback.format_exc())
    # Initialize as None, will handle in predict endpoint
    model, scaler, encoder, features = None, None, None, None

class PredictionRequest(BaseModel):
    cdi: float
    mmi: float
    sig: float
    magnitude: float
    depth: float

    class Config:
        json_schema_extra = {
            "example": {
                "cdi": 4.5,
                "mmi": 5.0,
                "sig": 600,
                "magnitude": 6.5,
                "depth": 10.0
            }
        }

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/api/auth/register")
def register(user: UserCreate):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = get_password_hash(user.password)
    try:
        cursor.execute(
            "INSERT INTO users (email, hashed_password) VALUES (%s, %s)", 
            (user.email, hashed_password)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=500, detail="Error creating user")
        
    cursor.close()
    conn.close()
    return {"message": "User created successfully"}

@app.post("/api/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (form_data.username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/debug")
def debug():
    pipeline_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "notebooks", "earthquake_pipeline.pkl"))
    return {
        "pipeline_path": pipeline_path,
        "path_exists": os.path.exists(pipeline_path),
        "model_loaded": model is not None,
        "features": features
    }

@app.get("/")
def read_root():
    return {"status": "ImpactSense API is running"}

@app.post("/api/predict")
def predict(request: PredictionRequest, current_user: dict = Depends(get_optional_current_user)):
    if model is None:
        raise HTTPException(status_code=500, detail="Machine learning pipeline not loaded")
    
    try:
        # Create a DataFrame from the request using the expected feature order
        input_data = pd.DataFrame([{
            "cdi": request.cdi,
            "mmi": request.mmi,
            "sig": request.sig,
            "magnitude": request.magnitude,
            "depth": request.depth
        }])
        
        # Ensure we only use the features the model was trained on, in the right order
        try:
            input_features = input_data[features]
        except KeyError as e:
            raise HTTPException(status_code=400, detail=f"Missing expected features. Required: {features}")

        # Scale the features
        scaled_features = scaler.transform(input_features)
        scaled_df = pd.DataFrame(scaled_features, columns=features)
        
        # Predict
        pred = model.predict(scaled_df)
        model_result = encoder.inverse_transform(pred)[0]
        
        # --- SAFETY OVERRIDE LAYER ---
        # Heuristic rules to handle extreme events misclassified due to training data bias.
        alert_result = model_result
        
        # Rule 1: Extreme Red (Severe Disasters)
        if request.magnitude >= 8.0 or request.sig >= 2000 or request.mmi >= 9.0:
            alert_result = "red"
        # Rule 2: Strong Orange (Significant Impact)
        elif request.magnitude >= 7.0 or request.sig >= 1000 or request.mmi >= 8.0:
            if model_result != "red": # Don't downgrade if model already says red
                alert_result = "orange"
        # -----------------------------
        
        # Save to database if user is authenticated
        if current_user:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        """INSERT INTO predictions (user_id, cdi, mmi, sig, magnitude, depth, alert_level) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                        (current_user["id"], request.cdi, request.mmi, request.sig, request.magnitude, request.depth, alert_result)
                    )
                    conn.commit()
                except Exception as db_e:
                    print(f"Database error: {db_e}")
                finally:
                    cursor.close()
                    conn.close()

        return {
            "alert": alert_result,
            "input": request.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
def get_history(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=503, detail="Database connection failed")
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM predictions WHERE user_id = %s ORDER BY timestamp DESC", 
        (current_user["id"],)
    )
    predictions = cursor.fetchall()
    cursor.close()
    conn.close()
    return predictions
