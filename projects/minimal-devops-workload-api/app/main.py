import os
import time
import logging
from flask import Flask, jsonify, request, Response
import psycopg2
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "minimal-devops-workload-api")
APP_ENV = os.getenv("APP_ENV", "local")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(message)s %(method)s %(path)s %(status)s %(duration_ms)s"
)
log_handler.setFormatter(formatter)
logger.handlers = [log_handler]

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)


def check_db():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3,
    )
    connection.close()


@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    duration_ms = round((time.time() - request.start_time) * 1000, 2)
    endpoint = request.path

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=endpoint
    ).observe(duration_ms / 1000)

    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": duration_ms,
        },
    )

    return response


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": APP_NAME,
        "env": APP_ENV
    }), 200


@app.route("/ready")
def ready():
    try:
        check_db()
        return jsonify({
            "status": "ready",
            "database": "reachable"
        }), 200
    except Exception as error:
        return jsonify({
            "status": "not_ready",
            "database": "unreachable",
            "error": str(error)
        }), 503


@app.route("/db-health")
def db_health():
    try:
        check_db()
        return jsonify({
            "database": "ok",
            "host": DB_HOST,
            "port": DB_PORT,
            "name": DB_NAME
        }), 200
    except Exception as error:
        return jsonify({
            "database": "error",
            "error": str(error)
        }), 500


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)
