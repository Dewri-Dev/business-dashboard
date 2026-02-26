import os
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from utils.auth import User, users
from reportlab.pdfgen import canvas
from flask import send_file
import io
import webbrowser
import threading

# Importing utilities
from utils.db import init_db, get_connection
from utils.calculations import calculate_health_score, generate_alerts
from utils.risk_logic import generate_risk_alerts  # Your new import!
from utils.translations import LANGUAGES           # The language dictionary

app = Flask(__name__)
app.secret_key = "super_secret_business_key" # Required for language memory
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Initialize the database on startup
init_db()

# --- Language Switching Logic ---
@app.route("/set_lang/<lang>")
def set_lang(lang):
    """Saves the selected language to the user's session and reloads the page."""
    if lang in LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.context_processor
def inject_translations():
    """Automatically injects the correct language dictionary into EVERY HTML page!"""
    lang = session.get('lang', 'en') # Default to English
    return dict(t=LANGUAGES.get(lang, LANGUAGES['en']), current_lang=lang)
# --------------------------------

@app.route("/")
def home():
    """Renders the landing page."""
    return render_template("home.html")

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

@app.route("/download-report")
@login_required
def download_report():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(revenue), SUM(expenses) FROM business_data")
    revenue, expenses = cursor.fetchone()
    profit = (revenue or 0) - (expenses or 0)

    p.drawString(100, 750, f"Revenue: {revenue}")
    p.drawString(100, 730, f"Expenses: {expenses}")
    p.drawString(100, 710, f"Profit: {profit}")

    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="report.pdf")

@app.route("/demo")
def demo_page():
    """Renders the frontend-only interactive demo."""
    return render_template("demo.html")

# YOUR NEW ALERTS ROUTE
@app.route("/alerts-page", methods=["GET", "POST"])
def alerts_page():
    """Handles the advanced risk alerts via form submission."""
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)