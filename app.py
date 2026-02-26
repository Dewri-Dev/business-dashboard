from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.risk_logic import generate_risk_alerts
import webbrowser
import threading

# Importing utilities (Based on Code 1's structure)
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

# ADD DATA
@app.route("/add-data", methods=["POST"])
def add_data():
    """Adds a new financial record with validation."""
    data = request.get_json()
    
    # Required fields validation
    required = ["date", "revenue", "expenses", "inventory_cost"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Inserts record including the optional 'category' field
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
        if 'conn' in locals():
            conn.close()

# SUMMARY
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
        if 'conn' in locals():
            conn.close()

# TRENDS
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
        if 'conn' in locals():
            conn.close()

@app.route("/analytics")
def analytics_page():
    """Renders the server-side analytics page."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Calculate totals directly from the database
        cursor.execute("SELECT SUM(revenue), SUM(expenses) FROM business_data")
        result = cursor.fetchone()
        
        rev = result[0] or 0
        exp = result[1] or 0
        profit = rev - exp
        margin = round((profit / rev * 100), 2) if rev > 0 else 0
        
        # Create the dictionary exactly as your HTML expects it
        summary_data = {
            "revenue": round(rev, 2),
            "expenses": round(exp, 2),
            "profit": round(profit, 2),
            "profit_margin": margin
        }
        
        return render_template("analytics.html", summary=summary_data)
        
    except Exception as e:
        return f"Error loading analytics: {str(e)}"
    finally:
        if 'conn' in locals():
            conn.close()

@app.route("/trends-page")
def trends_page():
    """Renders the standalone trends visualization page."""
    return render_template("trends.html")

@app.route("/health-page")
def health_page():
    """Renders the server-side health score and alerts page."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(revenue), SUM(expenses) FROM business_data")
        result = cursor.fetchone()
        
        rev = result[0] or 0
        exp = result[1] or 0
        profit = rev - exp
        margin = (profit / rev * 100) if rev > 0 else 0
        
        # Calculate health and alerts using your existing utils logic
        health_score = calculate_health_score(rev, exp, profit)
        alerts = generate_alerts(rev, exp, profit, margin)

        health_data = {
            "score": health_score,
            "alerts": alerts
        }
        
        return render_template("health.html", health=health_data)
        
    except Exception as e:
        return f"Error loading health data: {str(e)}"
    finally:
        if 'conn' in locals():
            conn.close()

@app.route("/alerts-page", methods=["GET", "POST"])
def alerts_page():

    alerts = []

    if request.method == "POST":
        current_revenue = float(request.form.get("current_revenue", 0))
        previous_revenue = float(request.form.get("previous_revenue", 0))
        current_expenses = float(request.form.get("current_expenses", 0))
        previous_expenses = float(request.form.get("previous_expenses", 0))
        inventory_cost = float(request.form.get("inventory_cost", 0))

        alerts = generate_risk_alerts(
            current_revenue,
            previous_revenue,
            current_expenses,
            previous_expenses,
            inventory_cost
        )

    return render_template("alerts.html", alerts=alerts)

def open_browser():
    """Opens the default web browser automatically."""
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == "__main__":
    # Start browser in a separate thread so it doesn't block the server
    threading.Timer(1, open_browser).start()
    app.run(debug=True)