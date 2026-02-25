from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import webbrowser
import threading
from utils.db import init_db, get_connection
from utils.calculations import calculate_health_score, generate_alerts

app = Flask(__name__)
CORS(app)

# Initialize the database on startup
init_db()

@app.route("/")
def home():
    """Renders the landing page."""
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    """Renders the main analytics dashboard."""
    return render_template("dashboard.html")

@app.route("/add-data", methods=["POST"])
def add_data():
    """Adds a new financial record with validation."""
    data = request.get_json()
    
    # Required fields validation
    required = ["date", "revenue", "expenses", "inventory_cost", "category"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO business_data 
            (date, revenue, expenses, inventory_cost, category)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["date"],
            float(data.get("revenue", 0)),
            float(data.get("expenses", 0)),
            float(data.get("inventory_cost", 0)),
            data.get("category", "General")
        ))
        conn.commit()
        return jsonify({"message": "Data recorded successfully", "status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/summary", methods=["GET"])
def summary():
    """Calculates high-level business metrics and health scores."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Fetch aggregates
        cursor.execute("""
            SELECT 
                SUM(revenue), 
                SUM(expenses), 
                SUM(inventory_cost) 
            FROM business_data
        """)
        result = cursor.fetchone()
        
        rev = result[0] or 0
        exp = result[1] or 0
        inv = result[2] or 0
        
        profit = rev - exp
        margin = (profit / rev * 100) if rev > 0 else 0
        
        # Logic from calculations utility
        health_score = calculate_health_score(rev, exp, profit)
        alerts = generate_alerts(rev, exp, profit, margin)

        return jsonify({
            "metrics": {
                "total_revenue": round(rev, 2),
                "total_expenses": round(exp, 2),
                "total_inventory": round(inv, 2),
                "net_profit": round(profit, 2),
                "profit_margin": round(margin, 2)
            },
            "health_score": health_score,
            "alerts": alerts
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/trends", methods=["GET"])
def trends():
    """Returns historical data for charts."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, revenue, expenses, category FROM business_data ORDER BY date ASC")
        rows = cursor.fetchall()
        
        data = [{"date": r[0], "revenue": r[1], "expenses": r[2], "category": r[3]} for r in rows]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Start browser in a separate thread so it doesn't block the server
    threading.Timer(1, open_browser).start()
    app.run(debug=True)