from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path

from database import initialize_database, create_ticket
from services.ai_service import generate_response
from services.search_service import search_documents
from services.vision_service import analyze_image


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
UPLOAD_DIR = BASE_DIR / "uploads"


# Create uploads folder if it does not exist
UPLOAD_DIR.mkdir(exist_ok=True)


# =========================================================
# FLASK APP
# =========================================================

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(STATIC_DIR)
)


# Maximum upload size = 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


# Allowed image formats
ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


# =========================================================
# DATABASE
# =========================================================

# Create the SQLite database/table if it does not exist
initialize_database()


# =========================================================
# HELPERS
# =========================================================

def allowed_file(filename: str) -> bool:

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return render_template("index.html")


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/api/health")
def health():

    return jsonify({
        "success": True,
        "status": "online",
        "service": "NODEFIX"
    })


# =========================================================
# CHAT / TROUBLESHOOTING API
# =========================================================

@app.post("/api/chat")
def chat():

    # -----------------------------------------------------
    # GET TEXT INPUT
    # -----------------------------------------------------

    equipment = request.form.get(
        "equipment",
        ""
    ).strip()

    message = request.form.get(
        "message",
        ""
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not equipment:

        return jsonify({
            "success": False,
            "error": "Please select the equipment."
        }), 400


    if not message:

        return jsonify({
            "success": False,
            "error": "Please describe the problem."
        }), 400


    # -----------------------------------------------------
    # IMAGE UPLOAD
    # -----------------------------------------------------

    photo = request.files.get("photo")

    photo_name = None

    photo_path = None


    if photo and photo.filename:

        if not allowed_file(photo.filename):

            return jsonify({
                "success": False,
                "error": (
                    "Please upload a PNG, JPG, JPEG "
                    "or WEBP image."
                )
            }), 400


        # Make filename safe
        safe_name = secure_filename(
            photo.filename
        )


        # Final path
        photo_path = UPLOAD_DIR / safe_name


        # Save image
        photo.save(photo_path)


        photo_name = safe_name


    # -----------------------------------------------------
    # IMAGE ANALYSIS
    #
    # CURRENT:
    # Local placeholder
    #
    # LATER:
    # Azure Foundry multimodal model
    # -----------------------------------------------------

    photo_analysis = analyze_image(

        image_path=(
            str(photo_path)
            if photo_path
            else None
        ),

        equipment=equipment

    )


    # -----------------------------------------------------
    # DOCUMENT RETRIEVAL
    #
    # CURRENT:
    # Local mock knowledge base
    #
    # LATER:
    # Azure AI Search
    # -----------------------------------------------------

    documents = search_documents(

        equipment=equipment,

        query=message

    )


    # -----------------------------------------------------
    # AI ANALYSIS
    #
    # CURRENT:
    # Local mock AI
    #
    # LATER:
    # Microsoft Foundry
    # -----------------------------------------------------

    result = generate_response(

        equipment=equipment,

        problem=message,

        documents=documents,

        photo_provided=(
            photo_name is not None
        ),

        image_observation=(
            photo_analysis["observation"]
        )

    )


    # -----------------------------------------------------
    # HUMAN ESCALATION
    # -----------------------------------------------------

    ticket_id = None


    if result["escalated"]:

        reason = result.get(

            "reason",

            "Unable to confidently resolve the issue."

        )


        # Safety-critical issue
        if "safety" in reason.lower():

            priority = "CRITICAL"

        else:

            priority = "HIGH"


        # Create SQLite ticket
        ticket_id = create_ticket(

            equipment=equipment,

            problem=message,

            priority=priority

        )


    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    return jsonify({

        "success": True,

        "equipment": equipment,

        "answer": result["answer"],

        "confidence": result["confidence"],

        "sources": result["sources"],

        "escalated": result["escalated"],

        "ticket_id": ticket_id,

        "escalation_reason": result.get(
            "reason",
            None
        ),

        "image_analysis": {

            "detected": photo_analysis["detected"],

            "observation": (
                photo_analysis["observation"]
            ),

            "confidence": (
                photo_analysis["confidence"]
            )

        }

    })


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )