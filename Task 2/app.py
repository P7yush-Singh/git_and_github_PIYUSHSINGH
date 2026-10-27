from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

@app.route("/")
def home():
    return render_template( "index.html",form_data={} )

@app.route("/submit", methods=["POST"])
def submit():
    form_data = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "message": request.form.get("message", "").strip()
    }

    if not MONGO_URI:
        return render_template(
            "index.html",
            error="MongoDB connection string is missing. Please configure MONGO_URI in your .env file.",
            form_data=form_data
        ), 503

    client = None

    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )

        client.admin.command("ping")

        collection = client.practice["flask-tutorial"]
        result = collection.insert_one(form_data)

        if result.acknowledged:
            return redirect(url_for("success"))

        return render_template(
            "index.html",
            error="Data could not be saved. Please try again.",
            form_data=form_data
        ), 500

    except (ValueError):
        app.logger.exception("MongoDB operation failed.")

        return render_template(
            "index.html",
            error="Unable to connect to MongoDB or save your data. Please check your configuration.",
            form_data=form_data
        ), 500


@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
