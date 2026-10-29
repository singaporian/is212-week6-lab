from flask import Flask, jsonify, request

from duckfine import DuckFine

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/fine")
def fine():
    raw = request.args.get("days", "")
    try:
        days = int(raw)
    except ValueError:
        return jsonify({"error": "days must be a non-negative integer"}), 400
    if days < 0:
        return jsonify({"error": "days must not be negative"}), 400

    deluxe = request.args.get("deluxe") == "1"
    amount = DuckFine("anonymous").charge(days, deluxe=deluxe)
    return jsonify({"days": days, "deluxe": deluxe, "fee": amount})


if __name__ == "__main__":
    app.run()
