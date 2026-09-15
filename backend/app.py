from flask import Flask, render_template, request, jsonify
import os

# Project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/troubleshoot", methods=["POST"])
def troubleshoot():

    data = request.get_json()

    equipment = data.get("equipment", "")
    problem = data.get("problem", "")

    # TEMPORARY LOCAL RESPONSE
    # Azure will replace this later.

    answer = (
        f"NODEFIX received your {equipment} problem. "
        f"Your description was: {problem} "
        "The next version will retrieve relevant lab documentation "
        "and generate a grounded troubleshooting response."
    )

    return jsonify({
        "title": "Initial analysis",
        "answer": answer,
        "confidence": "Demo",
        "sources": [
            "Local test mode"
        ]
    })


if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )