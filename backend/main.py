
# ==========================================
# INTERNSHIELD AI
# FASTAPI + MACHINE LEARNING INTEGRATION
# ==========================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from pathlib import Path
import joblib
import re


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

MODEL_FILE = MODEL_DIR / "best_model.joblib"
VECTORIZER_FILE = MODEL_DIR / "tfidf_vectorizer.joblib"


# ==========================================
# 2. LOAD TRAINED ML MODEL
# ==========================================

if not MODEL_FILE.exists():
    raise FileNotFoundError(
        f"Trained model not found: {MODEL_FILE}"
    )

if not VECTORIZER_FILE.exists():
    raise FileNotFoundError(
        f"TF-IDF vectorizer not found: {VECTORIZER_FILE}"
    )

model = joblib.load(MODEL_FILE)
vectorizer = joblib.load(VECTORIZER_FILE)

MODEL_NAME = type(model).__name__

print("InternShield AI ML model loaded successfully!")
print("Model:", MODEL_NAME)


# ==========================================
# 3. CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="InternShield AI",
    description="AI-powered Job and Internship Scam Detection API",
    version="2.1.0"
)


# ==========================================
# 4. CORS CONFIGURATION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 5. INPUT FORMAT
# ==========================================

class JobRequest(BaseModel):
    description: str = Field(
        ...,
        min_length=1,
        max_length=50000
    )


# ==========================================
# 6. PREPARE INPUT LIKE TRAINING DATA
# ==========================================

def prepare_job_text(description: str) -> str:
    """
    The model was trained using only the description column.
    Therefore, inference must use only the original description.

    Do not add placeholder fields or apply different text cleaning.
    TF-IDF performs its configured text processing.
    """

    return description


# ==========================================
# 7. IDENTIFY SUSPICIOUS INDICATORS
# ==========================================

def find_warning_signs(description: str):

    text = description.lower()

    patterns = {

        "Upfront registration or payment fee": [
            r"registration fee",
            r"pay.*(?:fee|money|amount)",
            r"payment.*(?:internship|job)",
            r"deposit.*(?:job|internship)",
            r"processing fee",
            r"refundable fee"
        ],

        "Guaranteed selection without assessment": [
            r"no interview",
            r"guaranteed selection",
            r"selected without interview",
            r"no experience required.*selected"
        ],

        "Unrealistic earning promises": [
            r"earn.*(?:per day|daily)",
            r"guaranteed income",
            r"earn.*(?:lakhs|lakh).*month"
        ],

        "Pressure to act immediately": [
            r"limited seats",
            r"apply immediately",
            r"urgent payment",
            r"offer expires today"
        ],

        "Requests for sensitive information": [
            r"share.*(?:otp|password)",
            r"send.*(?:atm|card) number",
            r"share.*bank details"
        ]
    }

    warnings = []

    for category, expressions in patterns.items():

        if any(
            re.search(pattern, text)
            for pattern in expressions
        ):
            warnings.append(category)

    return warnings


# ==========================================
# 8. HOME ROUTE
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to InternShield AI!",
        "status": "Running successfully",
        "model_loaded": True,
        "model": MODEL_NAME
    }


# ==========================================
# 9. HEALTH CHECK
# ==========================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "project": "InternShield AI",
        "ml_model": MODEL_NAME,
        "model_loaded": True
    }


# ==========================================
# 10. REAL ML ANALYSIS ENDPOINT
# ==========================================

@app.post("/api/analyze")
def analyze_job(request: JobRequest):

    description = request.description.strip()

    if not description:
        raise HTTPException(
            status_code=400,
            detail="Please provide a job description."
        )

    try:

        # Prepare input consistently with model training
        prepared_text = prepare_job_text(description)

        # Convert job description into TF-IDF features
        features = vectorizer.transform(
            [prepared_text]
        )

        # Predict using the trained ML model
        prediction = int(
            model.predict(features)[0]
        )

        # Identify additional rule-based warning indicators
        warnings = find_warning_signs(description)

        # Determine risk level
        if prediction == 1 and warnings:

            risk_level = "High Risk"

        elif prediction == 1 or len(warnings) >= 2:

            risk_level = "Suspicious"

        else:

            risk_level = "Lower Risk"

        # Generate recommendations
        if risk_level == "High Risk":

            recommendation = (
                "Do not pay any fees or share sensitive "
                "information. Independently verify the "
                "recruiter and company before proceeding."
            )

        elif risk_level == "Suspicious":

            recommendation = (
                "Proceed cautiously. Verify the company, "
                "recruiter identity and offer details "
                "through independent official sources."
            )

        else:

            recommendation = (
                "No major warning pattern was identified "
                "by this screening. This does not guarantee "
                "that the opportunity is genuine. "
                "Verify the employer independently."
            )

        # Final API response
        return {

            "success": True,

            "message": "Job opportunity analysis completed!",

            "prediction": (
                "Fake / Potentially Fraudulent"
                if prediction == 1
                else "Genuine-like"
            ),

            "prediction_label": prediction,

            "risk_level": risk_level,

            "warning_signs": warnings,

            "warning_count": len(warnings),

            "recommendation": recommendation,

            "model_used": MODEL_NAME,

            "analysis_type": "ML prediction + rule-based indicators"
        }

    except HTTPException:
        raise

    except Exception as error:

        print("Analysis error:", str(error))

        raise HTTPException(
            status_code=500,
            detail="An error occurred during job analysis."
        )


# ==========================================
# END OF INTERN SHIELD AI BACKEND
# ==========================================
