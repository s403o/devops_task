from flask import Flask, request, render_template
from pymongo import MongoClient
from datetime import datetime
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

mongo_uri = os.environ.get("MONGO_URI")
# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client["users"]  # Use 'users' database

# Application-level metrics
request_counter = metrics.counter(
    "flask_request_count", "Total number of requests received by the application"
)
request_latency = metrics.histogram(
    "flask_request_latency_seconds",
    "Request latency in seconds",
    buckets=(0.1, 0.2, 0.5, 1, 2, 5),
)

@app.route("/", methods=["GET", "POST"])
@request_counter
@request_latency
def index():
    if request.method == "POST":
        name = request.form["name"]
        timestamp = datetime.now()
        # Inserting data into MongoDB
        db.users.insert_one({"name": name, "timestamp": timestamp})
        return 'Name "{}" added to the database with timestamp: {}'.format(
            name, timestamp
        )
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
