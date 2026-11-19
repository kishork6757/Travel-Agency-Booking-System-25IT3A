"""
=============================================================================
Wanderlust Journeys - Full-Stack Flask Backend & RESTful API Service
Student: Kishor K | RegNo: 732925ITR051 | Class: 25IT3A
Institution: Velalar College of Engineering and Technology, Erode - 12
=============================================================================
"""

import os
import sqlite3
from datetime import date
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "travel_agency.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# -----------------------------------------------------------------------------
# Frontend Route
# -----------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------------------------------------------------------
# REST API Endpoints
# -----------------------------------------------------------------------------
@app.route("/api/stats")
def get_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            COUNT(DISTINCT b.booking_id) as total_bookings,
            COALESCE(SUM(CASE WHEN b.booking_status != 'CANCELLED' THEN b.num_travelers ELSE 0 END), 0) as total_guests,
            COALESCE(SUM(CASE WHEN b.booking_status != 'CANCELLED' THEN b.total_amount ELSE 0 END), 0.0) as gross_revenue,
            COALESCE(SUM(c.refund_amount), 0.0) as total_refunded,
            ROUND((CAST(COALESCE(SUM(CASE WHEN b.booking_status != 'CANCELLED' THEN b.num_travelers ELSE 0 END), 0) AS REAL) / 
                   (SELECT SUM(max_capacity) FROM travel_packages)) * 100.0, 1) as fleet_occupancy_rate
        FROM bookings b
        LEFT JOIN cancellations c ON b.booking_id = c.booking_id;
    """)
    row = cur.fetchone()
    conn.close()
    
    return jsonify({
        "gross_revenue": row["gross_revenue"],
        "net_revenue": row["gross_revenue"] - row["total_refunded"],
        "total_guests": row["total_guests"],
        "total_bookings": row["total_bookings"],
        "total_refunded": row["total_refunded"],
        "fleet_occupancy": row["fleet_occupancy_rate"] or 0.0
    })

@app.route("/api/packages")
def get_packages():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.package_id, p.destination, p.category, p.duration_days, p.price_per_person, p.max_capacity, p.season,
            COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0) as booked_seats,
            (p.max_capacity - COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0)) as remaining_seats,
            ROUND((CAST(COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0) AS REAL) / p.max_capacity) * 100.0, 1) as occupancy_rate
        FROM travel_packages p
        LEFT JOIN bookings b ON p.package_id = b.package_id
        GROUP BY p.package_id
        ORDER BY p.package_id ASC;
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route("/api/customers", methods=["GET", "POST"])
def manage_customers():
    conn = get_db()
    cur = conn.cursor()
    if request.method == "POST":
        data = request.json or {}
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        city = data.get("city", "").strip()

        if not name or not email or not phone or not city:
            return jsonify({"success": False, "error": "All fields are required"}), 400

        try:
            cur.execute("INSERT INTO customers (name, email, phone, city) VALUES (?, ?, ?, ?)",
                        (name, email, phone, city))
            conn.commit()
            new_id = cur.lastrowid
            conn.close()
            return jsonify({"success": True, "customer_id": new_id, "message": "Customer registered successfully!"})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({"success": False, "error": "Email address already registered"}), 409

    cur.execute("SELECT * FROM customers ORDER BY customer_id DESC;")
    customers = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(customers)

@app.route("/api/bookings", methods=["GET", "POST"])
def manage_bookings():
    conn = get_db()
    cur = conn.cursor()
    if request.method == "POST":
        data = request.json or {}
        customer_id = data.get("customer_id")
        package_id = data.get("package_id")
        travel_date = data.get("travel_date")
        num_travelers = int(data.get("num_travelers", 0))
        payment_method = data.get("payment_method", "UPI")

        if not customer_id or not package_id or not travel_date or num_travelers <= 0:
            return jsonify({"success": False, "error": "Invalid booking details"}), 400

        # CRITICAL: Capacity and Anti-Overbooking Check
        cur.execute("""
            SELECT p.destination, p.price_per_person, p.max_capacity,
                   (p.max_capacity - COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0)) as remaining_seats
            FROM travel_packages p
            LEFT JOIN bookings b ON p.package_id = b.package_id
            WHERE p.package_id = ?
            GROUP BY p.package_id;
        """, (package_id,))
        pkg = cur.fetchone()

        if not pkg:
            conn.close()
            return jsonify({"success": False, "error": "Package not found"}), 404

        remaining = pkg["remaining_seats"]
        if num_travelers > remaining:
            conn.close()
            return jsonify({
                "success": False,
                "error": f"OVERBOOKING BLOCKED: Requested {num_travelers} seats, but only {remaining} available for {pkg['destination']}."
            }), 400

        # Calculate Total Price + 5% GST
        subtotal = pkg["price_per_person"] * num_travelers
        grand_total = round(subtotal * 1.05, 2)
        today_str = str(date.today())

        try:
            cur.execute("""
                INSERT INTO bookings (customer_id, package_id, booking_date, travel_date, num_travelers, total_amount, booking_status)
                VALUES (?, ?, ?, ?, ?, ?, 'CONFIRMED');
            """, (customer_id, package_id, today_str, travel_date, num_travelers, grand_total))
            booking_id = cur.lastrowid

            cur.execute("""
                INSERT INTO payments (booking_id, payment_date, amount, payment_method, payment_status)
                VALUES (?, ?, ?, ?, 'PAID');
            """, (booking_id, today_str, grand_total, payment_method))

            conn.commit()
            conn.close()
            return jsonify({
                "success": True,
                "booking_id": booking_id,
                "destination": pkg["destination"],
                "total_amount": grand_total,
                "message": "Booking confirmed with live capacity protection!"
            })
        except Exception as ex:
            conn.rollback()
            conn.close()
            return jsonify({"success": False, "error": str(ex)}), 500

    cur.execute("""
        SELECT 
            b.booking_id, b.customer_id, b.package_id, b.booking_date, b.travel_date, 
            b.num_travelers, b.total_amount, b.booking_status,
            c.name as customer_name, c.phone as customer_phone,
            p.destination, p.category,
            COALESCE(pay.payment_status, 'UNPAID') as payment_status,
            pay.payment_method
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN travel_packages p ON b.package_id = p.package_id
        LEFT JOIN payments pay ON b.booking_id = pay.booking_id
        ORDER BY b.booking_id DESC;
    """)
    bookings = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(bookings)

@app.route("/api/cancel", methods=["POST"])
def cancel_booking():
    data = request.json or {}
    booking_id = data.get("booking_id")
    reason = data.get("reason", "Customer Request / Schedule Change").strip()

    if not booking_id:
        return jsonify({"success": False, "error": "Booking ID is required"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT total_amount, booking_status FROM bookings WHERE booking_id = ?", (booking_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return jsonify({"success": False, "error": "Booking not found"}), 404

    if row["booking_status"] == "CANCELLED":
        conn.close()
        return jsonify({"success": False, "error": "Booking is already cancelled"}), 400

    refund_val = round(row["total_amount"] * 0.90, 2)
    today_str = str(date.today())

    try:
        cur.execute("UPDATE bookings SET booking_status = 'CANCELLED' WHERE booking_id = ?", (booking_id,))
        cur.execute("""
            INSERT INTO cancellations (booking_id, cancellation_date, reason, refund_amount)
            VALUES (?, ?, ?, ?);
        """, (booking_id, today_str, reason, refund_val))
        cur.execute("UPDATE payments SET payment_status = 'REFUNDED' WHERE booking_id = ?", (booking_id,))
        conn.commit()
        conn.close()
        return jsonify({
            "success": True,
            "refund_amount": refund_val,
            "message": f"Booking #{booking_id} cancelled. 90% refund of ₹{refund_val:,.2f} processed."
        })
    except Exception as ex:
        conn.rollback()
        conn.close()
        return jsonify({"success": False, "error": str(ex)}), 500

@app.route("/api/analytics")
def get_analytics():
    conn = get_db()
    cur = conn.cursor()

    # Destination popularity
    cur.execute("""
        SELECT p.destination, SUM(b.num_travelers) as guests, SUM(b.total_amount) as revenue
        FROM bookings b
        JOIN travel_packages p ON b.package_id = p.package_id
        WHERE b.booking_status != 'CANCELLED'
        GROUP BY p.destination
        ORDER BY guests DESC;
    """)
    destinations = [dict(r) for r in cur.fetchall()]

    # Category breakdown
    cur.execute("""
        SELECT p.category, SUM(b.total_amount) as revenue, COUNT(b.booking_id) as bookings
        FROM bookings b
        JOIN travel_packages p ON b.package_id = p.package_id
        WHERE b.booking_status != 'CANCELLED'
        GROUP BY p.category;
    """)
    categories = [dict(r) for r in cur.fetchall()]

    # Monthly Trends
    cur.execute("""
        SELECT strftime('%m', booking_date) as month_num,
               CASE strftime('%m', booking_date)
                   WHEN '01' THEN 'Jan' WHEN '02' THEN 'Feb' WHEN '03' THEN 'Mar'
                   WHEN '04' THEN 'Apr' WHEN '05' THEN 'May' WHEN '06' THEN 'Jun'
                   WHEN '07' THEN 'Jul' WHEN '08' THEN 'Aug' WHEN '09' THEN 'Sep'
                   WHEN '10' THEN 'Oct' WHEN '11' THEN 'Nov' WHEN '12' THEN 'Dec'
               END as month_name,
               SUM(num_travelers) as guests,
               SUM(total_amount) as revenue
        FROM bookings
        GROUP BY month_num
        ORDER BY month_num ASC;
    """)
    monthly = [dict(r) for r in cur.fetchall()]

    # Booking Status counts
    cur.execute("SELECT booking_status, COUNT(*) as count FROM bookings GROUP BY booking_status;")
    statuses = [dict(r) for r in cur.fetchall()]

    conn.close()
    return jsonify({
        "destinations": destinations,
        "categories": categories,
        "monthly": monthly,
        "statuses": statuses
    })

if __name__ == "__main__":
    print("==============================================================================")
    print("Wanderlust Travel Agency - Fullstack REST Application Server Running")
    print("Student: Kishor K (RegNo: 732925ITR051) | Class: 25IT3A")
    print("Live Local URL: http://127.0.0.1:5000")
    print("==============================================================================")
    app.run(host="0.0.0.0", port=5000, debug=False)
