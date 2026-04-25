from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
import json
import os
from functools import wraps

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "replace_this_with_strong_secret"


# ------------------ LOGIN REQUIRED DECORATOR ------------------ #
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


# ------------------ DB CONNECTION ------------------ #
def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "localhost"),
        user=os.getenv("MYSQLUSER", "root"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE", "carbon_app"),
        port=int(os.getenv("MYSQLPORT", 3306))
    )


# ------------------ HOME ------------------ #
@app.route("/")
def home():
    return redirect("/login")


# ------------------ LOGIN ------------------ #
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "").strip()

        conn = get_db()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT id, full_name, username, email
            FROM users
            WHERE (LOWER(username)=%s OR LOWER(email)=%s)
            AND password=%s
        """, (identifier, identifier, password))

        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/dashboard")
        else:
            msg = "Invalid username/email or password."

    return render_template("login.html", msg=msg)


# ------------------ REGISTER ------------------ #
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
        if cur.fetchone():
            msg = "Username or email already exists."
            conn.close()
            return render_template("register.html", msg=msg)

        cur.execute("""
            INSERT INTO users (full_name, username, email, password)
            VALUES (%s, %s, %s, %s)
        """, (full_name, username, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html", msg=msg)


# ------------------ LOGOUT ------------------ #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ------------------ DASHBOARD ------------------ #
@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT total_kg, breakdown_json, recommendations
        FROM carbon_results
        WHERE user_id=%s
        ORDER BY id DESC LIMIT 1
    """, (session["user_id"],))

    last_result = cur.fetchone()
    conn.close()

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        last_result=last_result
    )


# ------------------ CALCULATOR PAGE ------------------ #
@app.route("/calculator")
@login_required
def calculator_page():
    return render_template("calculator.html")


# ------------------ CALCULATE ------------------ #
@app.route("/calculate", methods=["POST"])
@login_required
def calculate():
    data = request.get_json() or {}

    # ------- Travel ------- #
    bike = float(data.get("bike") or 0)
    car = float(data.get("car") or 0)
    bus = float(data.get("bus") or 0)
    train = float(data.get("train") or 0)

    travel = bike * 0.12 + car * 0.21 + bus * 0.05 + train * 0.06

    # ------- Electricity ------- #
    mode = data.get("elec_mode")

    if mode == "units":
        units = float(data.get("units") or 0)
        electricity = units * 0.82
    else:
        lights = int(data.get("lights") or 0)
        fans = int(data.get("fans") or 0)
        fridge = int(data.get("fridge") or 0)
        ac = int(data.get("ac") or 0)
        wm = int(data.get("washing_machine") or 0)
        tv = int(data.get("tv") or 0)

        electricity = lights * 0.10 + fans * 0.15 + fridge * 0.6 + ac * 1.5 + wm * 0.5 + tv * 0.2

    # ------- Food ------- #
    food_map = {
        "veg": 1.2,
        "1-2": 1.8,
        "2-3": 2.3,
        "nonveg": 3.5
    }
    food = food_map.get(data.get("food"), 0)

    # ------- Waste ------- #
    waste_map = {
        "small": 0.2,
        "medium": 0.5,
        "high": 1.0
    }

    waste = waste_map.get(data.get("waste_category"), 0)

    habit = data.get("waste_habit")
    if habit == "recycle":
        waste *= 0.7
    elif habit == "compost":
        waste *= 0.5

    # ------- TOTAL ------- #
    total = round(travel + electricity + food + waste, 2)

    breakdown = {
        "travel": round(travel, 3),
        "electricity": round(electricity, 3),
        "food": round(food, 3),
        "waste": round(waste, 3)
    }

    # ------- RECOMMENDATIONS ------- #
    rec = []

    if any([bike, car, bus, train]):
        if travel < 2:
            rec.append("🚗 Travel: Excellent low travel emissions.")
        elif travel < 8:
            rec.append("🚗 Travel: Use public transport or carpool more.")
        elif travel < 15:
            rec.append("🚗 Travel: Replace short car trips with cycling.")
        else:
            rec.append("🚗 Travel: High travel emissions — reduce solo car use.")

    if electricity > 0:
        if electricity < 1:
            rec.append("⚡ Electricity: Very low usage — great!")
        elif electricity < 4:
            rec.append("⚡ Electricity: Switch to LED bulbs.")
        elif electricity < 8:
            rec.append("⚡ Electricity: Reduce AC/fan usage.")
        else:
            rec.append("⚡ Electricity: Consider solar energy.")

    if data.get("food") and data.get("food") != "none":
        if food < 1.5:
            rec.append("🍽 Vegetarian diet reduces emissions.")
        elif food < 2.5:
            rec.append("🍽 Reduce non-veg meals.")
        else:
            rec.append("🍽 Prefer plant-based meals.")

    if data.get("waste_category") and data.get("waste_category") != "none":
        if waste < 0.3:
            rec.append("🗑 Low waste — great!")
        elif waste < 0.6:
            rec.append("🗑 Increase recycling.")
        else:
            rec.append("🗑 Start composting.")

    rec_text = "<br>".join(rec) if rec else "Enter input values to get recommendations."

    # ------- SAVE ------- #
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO carbon_results (user_id, total_kg, breakdown_json, recommendations)
        VALUES (%s, %s, %s, %s)
    """, (session["user_id"], total, json.dumps(breakdown), rec_text))

    conn.commit()
    conn.close()

    return jsonify({
        "total": total,
        "breakdown": breakdown,
        "recommendations": rec_text
    })


# ------------------ HISTORY ------------------ #
@app.route("/history")
@login_required
def history():
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    conn = get_db()
    cur = conn.cursor(dictionary=True)

    query = """
        SELECT total_kg, breakdown_json, recommendations, created_at
        FROM carbon_results
        WHERE user_id = %s
    """
    params = [session["user_id"]]

    if start_date:
        query += " AND created_at >= %s"
        params.append(start_date + " 00:00:00")

    if end_date:
        query += " AND created_at <= %s"
        params.append(end_date + " 23:59:59")

    query += " ORDER BY created_at ASC"
    cur.execute(query, params)

    rows = cur.fetchall()
    conn.close()

    dates = [r["created_at"].strftime("%Y-%m-%d") for r in rows]
    totals = [r["total_kg"] for r in rows]

    return render_template(
        "history.html",
        records=rows,
        username=session.get("username"),
        dates=dates,
        totals=totals
    )

# ------------------ RUN ------------------ #
if __name__ == "__main__":
    app.run(debug=True)