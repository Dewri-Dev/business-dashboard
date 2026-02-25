from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import webbrowser

app = Flask(__name__)
CORS(app)

DB_NAME = "database.db"

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            revenue REAL,
            expenses REAL,
            inventory_cost REAL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------- HOME  ----------
@app.route("/")
def dashboard():
    return render_template("index.html")


# ---------- ADD DATA ----------
@app.route('/add-data', methods=['POST'])
def add_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO business_data (date, revenue, expenses, inventory_cost)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get('date'),
            data.get('revenue', 0),
            data.get('expenses', 0),
            data.get('inventory_cost', 0)
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Data added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- HEALTH SCORE ----------
def calculate_health_score(revenue, expenses, profit):
    score = 100

    if profit < 0:
        score -= 30
    else:
        score += 10

    if revenue > 0 and expenses / revenue > 0.8:
        score -= 20

    if profit > 0:
        score += 10

    return max(0, min(score, 100))


# ---------- SUMMARY ----------
@app.route('/summary', methods=['GET'])
def summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(revenue), SUM(expenses) FROM business_data")
    result = cursor.fetchone()

    total_revenue = result[0] or 0
    total_expenses = result[1] or 0

    profit = total_revenue - total_expenses

    profit_margin = 0
    if total_revenue > 0:
        profit_margin = (profit / total_revenue) * 100

    health_score = calculate_health_score(total_revenue, total_expenses, profit)

    alerts = []

    if profit < 0:
        alerts.append("Business running at loss")

    if total_revenue > 0 and total_expenses / total_revenue > 0.8:
        alerts.append("Expenses too high")

    if 0 < profit_margin < 10:
        alerts.append("Low profit margin")

    if not alerts:
        alerts.append("Business stable")

    conn.close()

    return jsonify({
        "revenue": total_revenue,
        "expenses": total_expenses,
        "profit": profit,
        "profit_margin": round(profit_margin, 2),
        "health_score": health_score,
        "alerts": alerts
    })


# ---------- TRENDS ----------
@app.route('/trends', methods=['GET'])
def trends():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT date, revenue, expenses FROM business_data")
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append({
            "date": row[0],
            "revenue": row[1],
            "expenses": row[2]
        })

    return jsonify(data)


if __name__ == '__main__':
    # Automatically open the browser when the script runs
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)