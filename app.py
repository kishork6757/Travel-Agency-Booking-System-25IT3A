"""
=============================================================================
Wanderlust Journeys - Travel Agency Booking & Tourism Trend Analysis System
Modern Professional Full-Stack Web Application
Student: Kishor K | RegNo: 732925ITR051 | Class: 25IT3A
Department of Information Technology | Velalar College of Engg & Tech
=============================================================================
"""

import os
import sqlite3
from datetime import date, datetime
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Wanderlust | Travel Agency & Tourism Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Modern UI Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Top Header Styling */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        color: white;
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.25);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem;
        color: #FFFFFF;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #E2E8F0;
        max-width: 800px;
        line-height: 1.5;
        margin-bottom: 1.2rem;
    }
    .student-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #F8FAFC;
    }

    /* KPI Stat Cards */
    .stat-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .stat-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    .stat-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }

    /* Package Cards */
    .tour-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
        margin-bottom: 1.5rem;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .tour-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 20px -2px rgba(0, 0, 0, 0.1);
    }
    .tour-img {
        width: 100%;
        height: 190px;
        object-fit: cover;
    }
    .tour-body {
        padding: 1.2rem;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .tour-category {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 8px;
    }
    .cat-adventure { background: #FEF3C7; color: #D97706; }
    .cat-luxury { background: #EDE9FE; color: #7C3AED; }
    .cat-domestic { background: #DBEAFE; color: #1D4ED8; }
    .cat-international { background: #FCE7F3; color: #DB2777; }
    .cat-pilgrimage { background: #DCFCE7; color: #15803D; }

    /* Digital Boarding Pass Ticket */
    .boarding-pass {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 12px 24px rgba(30, 58, 138, 0.25);
        margin-top: 1rem;
        border: 2px dashed rgba(255, 255, 255, 0.35);
    }
</style>
""", unsafe_allow_html=True)

# Curated High-Definition Destination Imagery (Unsplash CDN)
DESTINATION_IMAGES = {
    "Manali & Kasol Alpine Tour": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80",
    "Goa Sun & Sand Gateway": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80",
    "Kerala Backwaters & Munnar": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80",
    "Kashmir Paradise Odyssey": "https://images.unsplash.com/photo-1566837945700-30057527ade0?auto=format&fit=crop&w=800&q=80",
    "Dubai Desert & City Lights": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80",
    "Varanasi & Ayodhya Heritage": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80",
    "Andaman Island Coral Explorer": "https://images.unsplash.com/photo-1589394815804-964ed0be2eb5?auto=format&fit=crop&w=800&q=80",
    "Thailand Island Extravaganza": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?auto=format&fit=crop&w=800&q=80",
    "Default": "https://images.unsplash.com/photo-1488646953014-85cb44e25828?auto=format&fit=crop&w=800&q=80"
}

# -----------------------------------------------------------------------------
# 2. Database Connection & Self-Healing Initializer
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "travel_agency.db")

def get_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='customers';")
    if cur.fetchone()[0] == 0:
        schema_file = os.path.join(DB_DIR, "schema_sqlite.sql")
        seed_file = os.path.join(DB_DIR, "seed_data.sql")
        if os.path.exists(schema_file):
            with open(schema_file, 'r', encoding='utf-8') as f:
                cur.executescript(f.read())
        if os.path.exists(seed_file):
            with open(seed_file, 'r', encoding='utf-8') as f:
                cur.executescript(f.read())
        conn.commit()
    conn.close()

init_db()

def query_df(sql, params=None):
    conn = get_db()
    df = pd.read_sql_query(sql, conn, params=params if params else [])
    conn.close()
    return df

# -----------------------------------------------------------------------------
# 3. Hero Banner & Academic Identity
# -----------------------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
        <div>
            <div class="hero-title">✈️ Wanderlust Travel & Tourism Portal</div>
            <div class="hero-subtitle">
                An intelligent travel booking platform with real-time anti-overbooking inventory protection, 
                automated refund settlement, and live predictive tourism trend analytics.
            </div>
        </div>
        <div>
            <div class="student-badge">
                🎓 <b>Kishor K</b> (732925ITR051) &nbsp;|&nbsp; Class: <b>25IT3A</b> &nbsp;|&nbsp; Scenario 21
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. Live Operational Metrics (KPI Bar)
# -----------------------------------------------------------------------------
metrics_df = query_df("""
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

gross_rev = metrics_df['gross_revenue'].iloc[0]
total_guests = int(metrics_df['total_guests'].iloc[0])
total_bookings = int(metrics_df['total_bookings'].iloc[0])
refunded = metrics_df['total_refunded'].iloc[0]
net_rev = gross_rev - refunded
fleet_occupancy = metrics_df['fleet_occupancy_rate'].iloc[0]

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Gross Revenue</div>
        <div class="stat-val">₹{gross_rev:,.0f}</div>
        <div style="color: #10B981; font-size: 0.8rem; font-weight: 600; margin-top: 4px;">↑ 100% Verified</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Net Realized</div>
        <div class="stat-val">₹{net_rev:,.0f}</div>
        <div style="color: #64748B; font-size: 0.8rem; font-weight: 600; margin-top: 4px;">-₹{refunded:,.0f} refunds</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Confirmed Guests</div>
        <div class="stat-val">{total_guests}</div>
        <div style="color: #3B82F6; font-size: 0.8rem; font-weight: 600; margin-top: 4px;">Travelers Booked</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Total Bookings</div>
        <div class="stat-val">{total_bookings}</div>
        <div style="color: #8B5CF6; font-size: 0.8rem; font-weight: 600; margin-top: 4px;">Reservations Made</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Fleet Occupancy</div>
        <div class="stat-val">{fleet_occupancy:.1f}%</div>
        <div style="color: #F59E0B; font-size: 0.8rem; font-weight: 600; margin-top: 4px;">Capacity Utilized</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Interactive Navigation Tabs
# -----------------------------------------------------------------------------
tab_explore, tab_book, tab_manage, tab_analytics, tab_admin = st.tabs([
    "🏖️ Explore Destinations",
    "📝 Book a Package (Anti-Overbooking)",
    "🎫 My Bookings & Cancellations",
    "📊 Live Tourism Analytics & Trends",
    "⚙️ Operations & SQL Explorer"
])

# =============================================================================
# TAB 1: Explore Destinations & Catalog
# =============================================================================
with tab_explore:
    st.markdown("### 🗺️ Discover Handcrafted Tour Packages")
    st.markdown("Filter our vacation packages by category, season, or budget. Real-time availability is tracked automatically.")
    
    # Filter Bar
    f1, f2, f3 = st.columns([1.5, 1, 1])
    with f1:
        search_query = st.text_input("🔍 Search Destination:", placeholder="e.g. Goa, Kashmir, Dubai, Thailand...")
    with f2:
        cat_filter = st.selectbox("Category:", ["All Categories", "Domestic", "International", "Adventure", "Luxury", "Pilgrimage"])
    with f3:
        season_filter = st.selectbox("Season:", ["All Seasons", "Summer", "Winter", "Monsoon", "Autumn"])

    # Build SQL Query with Filters
    sql = "SELECT * FROM v_destination_revenue WHERE 1=1"
    params = []
    if search_query:
        sql += " AND destination LIKE ?"
        params.append(f"%{search_query.strip()}%")
    if cat_filter != "All Categories":
        sql += " AND category = ?"
        params.append(cat_filter)
    if season_filter != "All Seasons":
        conn_temp = get_db()
        # look up season from travel_packages
        sql += " AND package_id IN (SELECT package_id FROM travel_packages WHERE season = ?)"
        params.append(season_filter)
        conn_temp.close()
        
    sql += " ORDER BY package_id ASC"
    packages = query_df(sql, params)

    if packages.empty:
        st.warning("No destinations match your search filters. Try adjusting your search query.")
    else:
        # Display responsive 3-column card grid
        cols = st.columns(3)
        for idx, row in packages.iterrows():
            col = cols[idx % 3]
            with col:
                dest_name = row['destination']
                img_url = DESTINATION_IMAGES.get(dest_name, DESTINATION_IMAGES["Default"])
                avail = int(row['remaining_seats'])
                cap = int(row['max_capacity'])
                booked = int(row['total_confirmed_guests'])
                occ = float(row['occupancy_rate_pct'])
                cat = row['category']
                cat_class = f"cat-{cat.lower()}"
                
                # Fetch price and duration
                conn_p = get_db()
                pkg_info = conn_p.execute("SELECT duration_days, price_per_person, season FROM travel_packages WHERE package_id = ?", (row['package_id'],)).fetchone()
                conn_p.close()
                duration = pkg_info['duration_days'] if pkg_info else 5
                price = pkg_info['price_per_person'] if pkg_info else 15000.0
                season = pkg_info['season'] if pkg_info else "All Season"
                
                badge_bg = "#10B981" if avail > 5 else ("#F59E0B" if avail > 0 else "#EF4444")
                badge_txt = f"{avail} Seats Left" if avail > 0 else "SOLD OUT"
                
                st.markdown(f"""
                <div class="tour-card">
                    <img src="{img_url}" class="tour-img" alt="{dest_name}"/>
                    <div class="tour-body">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span class="tour-category {cat_class}">{cat}</span>
                                <span style="background: {badge_bg}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.72rem; font-weight: 700;">{badge_txt}</span>
                            </div>
                            <h3 style="margin: 4px 0 6px 0; font-size: 1.15rem; color: #0F172A; font-weight: 700;">{dest_name}</h3>
                            <div style="color: #64748B; font-size: 0.85rem; margin-bottom: 8px;">
                                📅 <b>{duration} Days / {duration-1} Nights</b> &nbsp;|&nbsp; ☀️ {season}
                            </div>
                        </div>
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 10px;">
                                <div>
                                    <span style="font-size: 1.3rem; font-weight: 800; color: #2563EB;">₹{price:,.0f}</span>
                                    <span style="font-size: 0.75rem; color: #64748B;">/ guest</span>
                                </div>
                                <div style="font-size: 0.8rem; font-weight: 600; color: #64748B;">
                                    {booked}/{cap} booked ({occ:.0f}%)
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(min(occ / 100.0, 1.0))
                st.markdown("<div style='margin-bottom: 1.2rem;'></div>", unsafe_allow_html=True)

# =============================================================================
# TAB 2: Book Tour (Anti-Overbooking Protected Engine)
# =============================================================================
with tab_book:
    st.markdown("### 📝 Instant Tour Reservation")
    st.markdown("Reserve travel packages with real-time capacity validation and instant boarding pass ticket generation.")
    
    col_form, col_summary = st.columns([1.3, 1])
    
    with col_form:
        # Load Data
        all_customers = query_df("SELECT customer_id, name, email, phone, city FROM customers ORDER BY name ASC;")
        all_packages = query_df("SELECT * FROM v_destination_revenue ORDER BY destination ASC;")
        
        cust_choices = {f"{r['name']} ({r['city']} - {r['phone']})": r['customer_id'] for _, r in all_customers.iterrows()}
        pkg_choices = {f"{r['destination']} (ID: #{r['package_id']} | {r['remaining_seats']} seats free)": r['package_id'] for _, r in all_packages.iterrows()}
        
        with st.form("booking_engine_form", clear_on_submit=False):
            st.markdown("#### 1. Select Customer & Package")
            c1, c2 = st.columns(2)
            with c1:
                selected_cust_label = st.selectbox("Customer Profile:", list(cust_choices.keys()))
            with c2:
                selected_pkg_label = st.selectbox("Travel Package Destination:", list(pkg_choices.keys()))
            
            # Lookup Package Details
            chosen_pkg_id = pkg_choices[selected_pkg_label]
            chosen_pkg = all_packages[all_packages['package_id'] == chosen_pkg_id].iloc[0]
            remaining_seats = int(chosen_pkg['remaining_seats'])
            
            conn_u = get_db()
            unit_price = conn_u.execute("SELECT price_per_person, duration_days FROM travel_packages WHERE package_id = ?", (chosen_pkg_id,)).fetchone()
            conn_u.close()
            unit_fare = unit_price['price_per_person']
            duration_days = unit_price['duration_days']

            st.markdown("#### 2. Travel Details & Party Size")
            t1, t2, t3 = st.columns(3)
            with t1:
                travel_date = st.date_input("Scheduled Travel Date:", min_value=date.today())
            with t2:
                num_travelers = st.number_input("Number of Travelers:", min_value=1, max_value=25, value=2, step=1)
            with t3:
                payment_method = st.selectbox("Payment Mode:", ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"])

            # Compute Price
            total_fare = unit_fare * num_travelers
            gst_amount = round(total_fare * 0.05, 2)
            grand_total = total_fare + gst_amount

            # -------------------------------------------------------------
            # LIVE ANTI-OVERBOOKING GUARD NOTIFICATION
            # -------------------------------------------------------------
            if num_travelers > remaining_seats:
                st.error(f"""
                🛑 **OVERBOOKING BLOCKED!**  
                You requested **{num_travelers} seats**, but only **{remaining_seats} seats** are remaining for **{chosen_pkg['destination']}**.  
                *Please reduce the traveler headcount or choose another departure date.*
                """)
                is_disabled = True
            else:
                st.success(f"✅ **Seats Confirmed Available:** {remaining_seats} seats remaining. Booking is fully approved to proceed.")
                is_disabled = False

            book_btn = st.form_submit_button("Confirm Booking & Issue Boarding Ticket 🚀", disabled=is_disabled)
            
            if book_btn and not is_disabled:
                cust_id = cust_choices[selected_cust_label]
                conn = get_db()
                cur = conn.cursor()
                try:
                    # Insert Booking
                    cur.execute("""
                        INSERT INTO bookings (customer_id, package_id, booking_date, travel_date, num_travelers, total_amount, booking_status)
                        VALUES (?, ?, ?, ?, ?, ?, 'CONFIRMED');
                    """, (cust_id, chosen_pkg_id, str(date.today()), str(travel_date), num_travelers, grand_total))
                    new_id = cur.lastrowid

                    # Insert Payment
                    cur.execute("""
                        INSERT INTO payments (booking_id, payment_date, amount, payment_method, payment_status)
                        VALUES (?, ?, ?, ?, 'PAID');
                    """, (new_id, str(date.today()), grand_total, payment_method))

                    conn.commit()
                    st.session_state['last_booking'] = {
                        'id': new_id,
                        'customer': selected_cust_label.split('(')[0].strip(),
                        'destination': chosen_pkg['destination'],
                        'date': str(travel_date),
                        'travelers': num_travelers,
                        'amount': grand_total,
                        'method': payment_method,
                        'duration': duration_days
                    }
                    st.balloons()
                    st.success(f"🎉 Booking Confirmed Successfully! Reference ID: `#{new_id}`")
                except Exception as ex:
                    conn.rollback()
                    st.error(f"Booking Transaction Failed: {ex}")
                finally:
                    conn.close()

    with col_summary:
        st.markdown("#### 🧾 Live Price Breakdown")
        st.markdown(f"""
        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 14px; padding: 1.25rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748B;">Destination:</span>
                <b>{chosen_pkg['destination']}</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748B;">Base Fare per Guest:</span>
                <span>₹{unit_fare:,.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748B;">Travelers Count:</span>
                <span>× {num_travelers} Guest(s)</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748B;">Subtotal:</span>
                <span>₹{total_fare:,.2f}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748B;">Standard GST (5%):</span>
                <span>₹{gst_amount:,.2f}</span>
            </div>
            <hr style="margin: 10px 0; border: none; border-top: 1px solid #E2E8F0;"/>
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
                <span style="font-weight: 800; font-size: 1.1rem; color: #0F172A;">Total Amount:</span>
                <span style="font-weight: 800; font-size: 1.3rem; color: #2563EB;">₹{grand_total:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display Boarding Pass if just booked
        if 'last_booking' in st.session_state:
            b = st.session_state['last_booking']
            st.markdown(f"""
            <div class="boarding-pass">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.25); padding-bottom: 10px; margin-bottom: 12px;">
                    <div>
                        <span style="font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase;">WANDERLUST E-TICKET</span>
                        <h3 style="margin: 0; font-size: 1.3rem;">{b['destination']}</h3>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.75rem;">BOOKING REF</span>
                        <div style="font-size: 1.2rem; font-weight: 800;">#{b['id']}</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.85rem;">
                    <div><b>Passenger:</b> {b['customer']}</div>
                    <div><b>Departure:</b> {b['date']}</div>
                    <div><b>Party Size:</b> {b['travelers']} Guest(s)</div>
                    <div><b>Duration:</b> {b['duration']} Days</div>
                    <div><b>Settlement:</b> ₹{b['amount']:,.2f} (PAID)</div>
                    <div><b>Gateway:</b> {b['method']}</div>
                </div>
                <div style="margin-top: 12px; font-size: 0.75rem; opacity: 0.85; text-align: center;">
                    ✅ Boarding Confirmed & Inventory Locked &nbsp;|&nbsp; 90% Refund Cancellation Protection
                </div>
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# TAB 3: My Bookings & Manage Cancellations
# =============================================================================
with tab_manage:
    st.markdown("### 🎫 Manage Reservations & 90% Refund Portal")
    st.markdown("Search existing customer bookings, inspect reservation invoices, and cancel trips with automated seat restoration.")
    
    all_b = query_df("""
        SELECT 
            b.booking_id as 'Booking ID',
            c.name as 'Customer Name',
            c.phone as 'Contact',
            p.destination as 'Destination',
            b.travel_date as 'Travel Date',
            b.num_travelers as 'Guests',
            b.total_amount as 'Total (₹)',
            b.booking_status as 'Status',
            COALESCE(pay.payment_status, 'UNPAID') as 'Payment'
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN travel_packages p ON b.package_id = p.package_id
        LEFT JOIN payments pay ON b.booking_id = pay.booking_id
        ORDER BY b.booking_id DESC;
    """)
    
    st.dataframe(all_b, use_container_width=True, hide_index=True)
    st.markdown("---")
    
    st.markdown("#### 🔄 Cancel Reservation & Release Seats")
    active_b = query_df("""
        SELECT b.booking_id, c.name, p.destination, b.num_travelers, b.total_amount
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN travel_packages p ON b.package_id = p.package_id
        WHERE b.booking_status = 'CONFIRMED'
        ORDER BY b.booking_id DESC;
    """)
    
    if active_b.empty:
        st.info("No active confirmed bookings available for cancellation.")
    else:
        cancel_map = {
            f"Booking #{r['booking_id']} — {r['name']} to {r['destination']} ({r['num_travelers']} Guests, ₹{r['total_amount']:,.0f})": r['booking_id']
            for _, r in active_b.iterrows()
        }
        
        c_col1, c_col2 = st.columns([1.5, 1])
        with c_col1:
            sel_cancel_label = st.selectbox("Select Booking to Cancel:", list(cancel_map.keys()))
            cancel_id = cancel_map[sel_cancel_label]
            cancel_row = active_b[active_b['booking_id'] == cancel_id].iloc[0]
            
            refund_val = round(cancel_row['total_amount'] * 0.90, 2)
            fee_val = round(cancel_row['total_amount'] * 0.10, 2)
            
            reason = st.text_input("Reason for Cancellation:", value="Customer Medical Emergency / Schedule Conflict")
            
            if st.button("Confirm Cancellation & Release Seats 🔄", type="primary"):
                conn = get_db()
                cur = conn.cursor()
                try:
                    cur.execute("UPDATE bookings SET booking_status = 'CANCELLED' WHERE booking_id = ?", (cancel_id,))
                    cur.execute("""
                        INSERT INTO cancellations (booking_id, cancellation_date, reason, refund_amount)
                        VALUES (?, ?, ?, ?);
                    """, (cancel_id, str(date.today()), reason.strip(), refund_val))
                    cur.execute("UPDATE payments SET payment_status = 'REFUNDED' WHERE booking_id = ?", (cancel_id,))
                    conn.commit()
                    st.success(f"Booking `#{cancel_id}` has been CANCELLED.")
                    st.info(f"✅ **{cancel_row['num_travelers']} seats** immediately released back to '{cancel_row['destination']}'.")
                    st.rerun()
                except Exception as ex:
                    conn.rollback()
                    st.error(f"Cancellation failed: {ex}")
                finally:
                    conn.close()

        with c_col2:
            st.markdown(f"""
            <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 12px; padding: 1.2rem; color: #92400E;">
                <h4 style="margin: 0 0 6px 0; color: #B45309;">⚠️ Refund Settlement Policy</h4>
                <p style="font-size: 0.88rem; margin-bottom: 8px;">
                    Our policy issues an automatic <b>90% refund</b> with a 10% administrative processing fee.
                </p>
                <div style="font-size: 0.92rem;">
                    • Original Fare: <b>₹{cancel_row['total_amount']:,.2f}</b><br/>
                    • 10% Cancellation Fee: <b>₹{fee_val:,.2f}</b><br/>
                    • <b>Refund Issued to Customer:</b> <span style="font-size: 1.15rem; color: #15803D; font-weight: 800;">₹{refund_val:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# =============================================================================
# TAB 4: Live Tourism Trend Analytics & Business Intelligence
# =============================================================================
with tab_analytics:
    st.markdown("### 📊 Interactive Tourism Trends & Business Intelligence")
    st.markdown("Visual analytics generated dynamically from live relational database records using Pandas and Plotly.")
    
    analytics_master = query_df("""
        SELECT 
            b.booking_id, b.booking_date, b.travel_date, b.num_travelers, b.total_amount, b.booking_status,
            p.package_id, p.destination, p.category, p.duration_days, p.price_per_person, p.max_capacity, p.season,
            c.city, c.name as customer_name,
            pay.payment_method, pay.payment_status,
            canc.refund_amount
        FROM bookings b
        JOIN travel_packages p ON b.package_id = p.package_id
        JOIN customers c ON b.customer_id = c.customer_id
        LEFT JOIN payments pay ON b.booking_id = pay.booking_id
        LEFT JOIN cancellations canc ON b.booking_id = canc.booking_id;
    """)
    analytics_master['booking_date'] = pd.to_datetime(analytics_master['booking_date'])
    analytics_master['month'] = analytics_master['booking_date'].dt.strftime('%B')
    analytics_master['month_num'] = analytics_master['booking_date'].dt.month

    # Row 1 Charts
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("#### 1. Top Tourist Destinations by Confirmed Guests")
        dest_grp = analytics_master[analytics_master['booking_status'] != 'CANCELLED'].groupby('destination')['num_travelers'].sum().reset_index()
        dest_grp = dest_grp.sort_values(by='num_travelers', ascending=True)
        fig_dest = px.bar(
            dest_grp, x='num_travelers', y='destination', orientation='h',
            labels={'num_travelers': 'Confirmed Travelers', 'destination': 'Destination'},
            color='num_travelers', color_continuous_scale='Blues', text_auto=True
        )
        fig_dest.update_layout(height=360, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_dest, use_container_width=True)

    with g2:
        st.markdown("#### 2. Seasonal Demand Trajectory (Monthly)")
        m_grp = analytics_master.groupby(['month_num', 'month'])['num_travelers'].sum().reset_index().sort_values('month_num')
        fig_line = px.area(
            m_grp, x='month', y='num_travelers', markers=True,
            labels={'num_travelers': 'Travelers Headcount', 'month': 'Booking Month'},
            color_discrete_sequence=['#2563EB']
        )
        fig_line.update_traces(line=dict(width=3))
        fig_line.update_layout(height=360, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_line, use_container_width=True)

    # Row 2 Charts
    g3, g4 = st.columns(2)
    with g3:
        st.markdown("#### 3. Revenue Share by Tour Category")
        cat_grp = analytics_master[analytics_master['booking_status'] != 'CANCELLED'].groupby('category')['total_amount'].sum().reset_index()
        fig_pie = px.pie(
            cat_grp, values='total_amount', names='category', hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=340, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with g4:
        st.markdown("#### 4. Booking Health: Confirmed vs Cancelled")
        stat_grp = analytics_master['booking_status'].value_counts().reset_index()
        stat_grp.columns = ['Status', 'Count']
        fig_stat = px.bar(
            stat_grp, x='Status', y='Count', color='Status',
            color_discrete_map={'CONFIRMED': '#2563EB', 'COMPLETED': '#10B981', 'CANCELLED': '#EF4444'},
            text_auto=True
        )
        fig_stat.update_layout(showlegend=False, height=340, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_stat, use_container_width=True)

# =============================================================================
# TAB 5: Operations & Database SQL Explorer
# =============================================================================
with tab_admin:
    st.markdown("### ⚙️ Agency Operations & Database Explorer")
    
    adm1, adm2 = st.columns([1, 1])
    with adm1:
        st.markdown("#### ➕ Add New Tour Package")
        with st.form("new_pkg_form"):
            p_dest = st.text_input("Destination Name:", placeholder="e.g. Ooty & Kodaikanal Hill Station")
            p_dur = st.number_input("Duration (Days):", min_value=1, max_value=30, value=4)
            p_price = st.number_input("Price per Guest (₹):", min_value=500.0, max_value=200000.0, value=12500.0, step=500.0)
            p_cap = st.number_input("Maximum Seating Capacity:", min_value=5, max_value=100, value=20)
            p_cat = st.selectbox("Category:", ["Domestic", "International", "Adventure", "Luxury", "Pilgrimage"])
            p_season = st.selectbox("Season:", ["Summer", "Winter", "Monsoon", "Autumn", "All Season"])
            
            if st.form_submit_button("Create Package 🚀"):
                if p_dest.strip():
                    conn = get_db()
                    conn.execute("""
                        INSERT INTO travel_packages (destination, duration_days, price_per_person, max_capacity, category, season)
                        VALUES (?, ?, ?, ?, ?, ?);
                    """, (p_dest.strip(), p_dur, p_price, p_cap, p_cat, p_season))
                    conn.commit()
                    conn.close()
                    st.success(f"Package '{p_dest}' created successfully!")
                    st.rerun()

    with adm2:
        st.markdown("#### 👤 Register New Customer Profile")
        with st.form("new_cust_form"):
            c_name = st.text_input("Customer Name:", placeholder="e.g. Balaji Narayanan")
            c_email = st.text_input("Email:", placeholder="e.g. balaji@example.com")
            c_phone = st.text_input("Phone Number:", placeholder="e.g. 9845112233")
            c_city = st.text_input("City:", placeholder="e.g. Coimbatore")
            
            if st.form_submit_button("Register Customer 💾"):
                if c_name and c_email and c_phone and c_city:
                    conn = get_db()
                    try:
                        conn.execute("""
                            INSERT INTO customers (name, email, phone, city)
                            VALUES (?, ?, ?, ?);
                        """, (c_name.strip(), c_email.strip(), c_phone.strip(), c_city.strip()))
                        conn.commit()
                        st.success(f"Customer '{c_name}' registered successfully!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Customer email already exists in database.")
                    finally:
                        conn.close()

    st.markdown("---")
    st.markdown("#### 🗃️ Raw Database Table Viewer & Export")
    tbl_choice = st.selectbox("Select SQL Table / View:", ["travel_packages", "customers", "bookings", "payments", "cancellations", "v_destination_revenue", "v_booking_summary"])
    df_table = query_df(f"SELECT * FROM {tbl_choice};")
    st.dataframe(df_table, use_container_width=True)
    
    st.download_button(
        label=f"Download {tbl_choice}.csv 📥",
        data=df_table.to_csv(index=False).encode('utf-8'),
        file_name=f"{tbl_choice}.csv",
        mime="text/csv"
    )

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.88rem; padding: 1rem 0;">
    <b>Wanderlust Travel Agency Booking & Tourism Trend Analysis System</b> (Scenario 21)<br/>
    Academic Activity Assessment (2026 - 2027) | Department of Information Technology<br/>
    <b>Velalar College of Engineering and Technology, Erode - 12</b><br/>
    Student: <b>Kishor K</b> (Reg No: 732925ITR051) | Class: <b>25IT3A</b>
</div>
""", unsafe_allow_html=True)
