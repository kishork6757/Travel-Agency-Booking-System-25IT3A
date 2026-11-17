"""
=============================================================================
Travel Agency Booking and Tourism Trend Analysis System - Web Application
Student: Kishor K | RegNo: 732925ITR051 | Class: 25IT3A
Institution: Velalar College of Engineering and Technology, Erode - 12
Assigned Scenario: Scenario 21 (Travel Agency Booking & Tourism Trend Analysis)
=============================================================================
"""

import os
import sqlite3
from datetime import date
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom CSS
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Travel Agency Booking & Tourism Trends",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .badge-card {
        background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .package-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .package-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Database Connection & Auto-Initialization Helper
# -----------------------------------------------------------------------------
DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "travel_agency.db")

def get_db_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_database():
    """Ensure database tables and initial seed data exist."""
    conn = get_db_connection()
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

init_database()

def query_df(sql, params=None):
    conn = get_db_connection()
    df = pd.read_sql_query(sql, conn, params=params if params else [])
    conn.close()
    return df

# -----------------------------------------------------------------------------
# 3. Sidebar Navigation & Academic Metadata
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ✈️ Travel Agency Portal")
    st.markdown("**Academic Assessment (2026 - 2027)**")
    
    st.markdown("""
    <div style='background-color: #EEF2F6; padding: 10px 12px; border-radius: 8px; font-size: 0.88rem; margin-bottom: 1rem;'>
        <b>Student:</b> Kishor K<br/>
        <b>Reg No:</b> 732925ITR051<br/>
        <b>Class:</b> 25IT3A<br/>
        <b>College:</b> VCET, Erode - 12<br/>
        <b>Assigned:</b> Scenario 21
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigation Menu:",
        [
            "🏠 Overview Dashboard",
            "📦 Browse Travel Packages",
            "📝 Book Tour (Anti-Overbooking Guard)",
            "👤 Register Customer",
            "🔄 Cancel Booking & Refund",
            "📊 Tourism Trend Analytics",
            "🗃️ Raw Database Explorer"
        ]
    )
    
    st.markdown("---")
    # Live Quick Stats
    conn = get_db_connection()
    c_count = conn.execute("SELECT count(*) FROM customers").fetchone()[0]
    p_count = conn.execute("SELECT count(*) FROM travel_packages").fetchone()[0]
    b_count = conn.execute("SELECT count(*) FROM bookings").fetchone()[0]
    conn.close()
    
    st.markdown(f"**Live System Status:**")
    st.markdown(f"👥 **{c_count}** Customers | 📦 **{p_count}** Packages")
    st.markdown(f"🎫 **{b_count}** Total Bookings Recorded")
    st.markdown("🟢 **Database:** Connected & Active")

# -----------------------------------------------------------------------------
# 4. Main Header Banner
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">Travel Agency Booking & Tourism Trend Analysis System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Integrated Academic Project-Based Assessment | Department of Information Technology</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# View 1: Overview Dashboard
# -----------------------------------------------------------------------------
if menu == "🏠 Overview Dashboard":
    st.markdown("### 📈 Executive Performance & Operational Summary")
    
    # Compute Top Metrics
    metrics_df = query_df("""
        SELECT 
            COUNT(DISTINCT b.booking_id) as total_bookings,
            COALESCE(SUM(CASE WHEN b.booking_status != 'CANCELLED' THEN b.num_travelers ELSE 0 END), 0) as total_guests,
            COALESCE(SUM(CASE WHEN b.booking_status != 'CANCELLED' THEN b.total_amount ELSE 0 END), 0.0) as gross_revenue,
            COALESCE(SUM(c.refund_amount), 0.0) as total_refunded,
            ROUND(AVG(CASE WHEN b.booking_status != 'CANCELLED' THEN b.total_amount ELSE NULL END), 2) as avg_booking_val
        FROM bookings b
        LEFT JOIN cancellations c ON b.booking_id = c.booking_id;
    """)
    
    total_rev = metrics_df['gross_revenue'].iloc[0]
    total_guests = int(metrics_df['total_guests'].iloc[0])
    total_b = int(metrics_df['total_bookings'].iloc[0])
    avg_val = metrics_df['avg_booking_val'].iloc[0]
    refunded = metrics_df['total_refunded'].iloc[0]
    net_rev = total_rev - refunded

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="💰 Gross Booking Revenue", value=f"₹{total_rev:,.0f}")
    with c2:
        st.metric(label="👥 Confirmed Travelers", value=f"{total_guests} Guests")
    with c3:
        st.metric(label="🎟️ Total Reservations", value=f"{total_b} Bookings")
    with c4:
        st.metric(label="💵 Net Realized Revenue", value=f"₹{net_rev:,.0f}", delta=f"-₹{refunded:,.0f} refunds")

    st.markdown("---")
    
    col_left, col_right = st.columns([1.4, 1])
    with col_left:
        st.markdown("#### 🏆 Destination Popularity & Revenue Performance")
        revenue_df = query_df("SELECT * FROM v_destination_revenue ORDER BY total_revenue DESC;")
        st.dataframe(
            revenue_df[[
                'destination', 'category', 'max_capacity', 'total_confirmed_guests', 
                'remaining_seats', 'occupancy_rate_pct', 'total_revenue'
            ]].rename(columns={
                'destination': 'Destination',
                'category': 'Category',
                'max_capacity': 'Capacity',
                'total_confirmed_guests': 'Booked',
                'remaining_seats': 'Available',
                'occupancy_rate_pct': 'Occupancy %',
                'total_revenue': 'Revenue (₹)'
            }),
            use_container_width=True,
            hide_index=True
        )

    with col_right:
        st.markdown("#### 🛡️ Anti-Overbooking Protection Engine")
        st.info("""
        **How the System Protects Capacity:**
        1. **Live Inventory Calculation:** Computes `available_seats = max_capacity - total_confirmed_guests` in real time.
        2. **Multi-tier Safeguard:** Both Java (`BookingService`) and SQLite DB Triggers (`trg_prevent_overbooking`) reject bookings exceeding remaining capacity.
        3. **Dynamic Re-allocation:** When a booking is cancelled, seats are immediately released back to available inventory with 90% refund processing.
        """)

# -----------------------------------------------------------------------------
# View 2: Browse Travel Packages
# -----------------------------------------------------------------------------
elif menu == "📦 Browse Travel Packages":
    st.markdown("### 📦 Available Travel Packages Catalog")
    st.markdown("Explore tour destinations, pricing, trip durations, and live seating availability.")
    
    packages_df = query_df("SELECT * FROM v_destination_revenue ORDER BY package_id ASC;")
    
    cols = st.columns(3)
    for idx, row in packages_df.iterrows():
        col = cols[idx % 3]
        with col:
            avail = int(row['remaining_seats'])
            cap = int(row['max_capacity'])
            booked = int(row['total_confirmed_guests'])
            occ = float(row['occupancy_rate_pct'])
            
            badge_color = "#10B981" if avail > 5 else ("#F59E0B" if avail > 0 else "#EF4444")
            badge_text = f"{avail} Seats Left" if avail > 0 else "SOLD OUT"
            
            st.markdown(f"""
            <div class="package-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 0.8rem; font-weight: 700; color: #64748B;">ID: #{row['package_id']} | {row['category']}</span>
                    <span style="background-color: {badge_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">{badge_text}</span>
                </div>
                <h4 style="margin: 0 0 6px 0; color: #1E293B;">{row['destination']}</h4>
                <div style="font-size: 0.9rem; color: #475569; margin-bottom: 10px;">
                    ⏱️ <b>Capacity:</b> {cap} Seats | <b>Booked:</b> {booked} Guests
                </div>
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <span style="font-size: 1.15rem; font-weight: 800; color: #0EA5E9;">₹{row['total_revenue'] / (booked if booked>0 else 1):,.0f} <span style="font-size: 0.75rem; color: #64748B;">/person</span></span>
                    <span style="font-size: 0.85rem; font-weight: 600; color: #64748B;">Occupancy: {occ:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(min(occ / 100.0, 1.0))

# -----------------------------------------------------------------------------
# View 3: Book Tour (Anti-Overbooking Protected)
# -----------------------------------------------------------------------------
elif menu == "📝 Book Tour (Anti-Overbooking Protected)":
    st.markdown("### 📝 Book a Travel Package")
    st.markdown("Select a customer, choose a destination, and enter travelers count. The system will automatically check capacity in real-time.")
    
    # Load Customers and Packages
    customers = query_df("SELECT customer_id, name, phone, city FROM customers ORDER BY name ASC")
    packages = query_df("SELECT * FROM v_destination_revenue ORDER BY destination ASC")
    
    cust_options = {f"{row['name']} (ID: {row['customer_id']} | {row['city']})": row['customer_id'] for _, row in customers.iterrows()}
    pkg_options = {f"{row['destination']} ({row['remaining_seats']} seats available - ₹{row['total_revenue']/(row['total_confirmed_guests'] if row['total_confirmed_guests']>0 else 1):,.0f}/person)": row['package_id'] for _, row in packages.iterrows()}
    
    with st.form("booking_form", clear_on_submit=False):
        c1, c2 = st.columns(2)
        with c1:
            selected_cust_label = st.selectbox("Select Customer:", list(cust_options.keys()))
            selected_pkg_label = st.selectbox("Select Travel Package:", list(pkg_options.keys()))
            travel_date = st.date_input("Scheduled Travel Date:", min_value=date.today())
        
        with c2:
            num_travelers = st.number_input("Number of Travelers:", min_value=1, max_value=30, value=2, step=1)
            payment_method = st.selectbox("Payment Method:", ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash"])
        
        # Look up selected package info
        pkg_id = pkg_options[selected_pkg_label]
        pkg_row = packages[packages['package_id'] == pkg_id].iloc[0]
        remaining = int(pkg_row['remaining_seats'])
        
        # Calculate price
        conn = get_db_connection()
        unit_price = conn.execute("SELECT price_per_person FROM travel_packages WHERE package_id = ?", (pkg_id,)).fetchone()[0]
        conn.close()
        
        total_price = unit_price * num_travelers
        st.markdown(f"**Total Invoice Estimate:** ₹{unit_price:,.2f} × {num_travelers} = **`₹{total_price:,.2f}`**")
        
        # Live Anti-Overbooking Guard Notification
        if num_travelers > remaining:
            st.error(f"❌ **CAPACITY EXCEEDED!** You requested **{num_travelers} seats**, but only **{remaining} seats** are available for *{pkg_row['destination']}*. Booking cannot proceed.")
            submit_disabled = True
        else:
            st.success(f"✅ **Seats Available:** {remaining} seats free. Ready to book!")
            submit_disabled = False
            
        submitted = st.form_submit_button("Confirm Booking & Issue Receipt 🚀", disabled=submit_disabled)
        
        if submitted and not submit_disabled:
            cust_id = cust_options[selected_cust_label]
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                # Insert Booking
                cur.execute("""
                    INSERT INTO bookings (customer_id, package_id, booking_date, travel_date, num_travelers, total_amount, booking_status)
                    VALUES (?, ?, ?, ?, ?, ?, 'CONFIRMED');
                """, (cust_id, pkg_id, str(date.today()), str(travel_date), num_travelers, total_price))
                new_booking_id = cur.lastrowid
                
                # Insert Payment
                cur.execute("""
                    INSERT INTO payments (booking_id, payment_date, amount, payment_method, payment_status)
                    VALUES (?, ?, ?, ?, 'PAID');
                """, (new_booking_id, str(date.today()), total_price, payment_method))
                
                conn.commit()
                st.balloons()
                st.success(f"🎉 **Booking Confirmed Successfully!** Reference ID: `#{new_booking_id}`")
                st.info(f"**Receipt:** Paid ₹{total_price:,.2f} via {payment_method} for {num_travelers} traveler(s) to {pkg_row['destination']}.")
            except Exception as e:
                conn.rollback()
                st.error(f"Booking failed: {e}")
            finally:
                conn.close()

# -----------------------------------------------------------------------------
# View 4: Customer Registration
# -----------------------------------------------------------------------------
elif menu == "👤 Register Customer":
    st.markdown("### 👤 Customer Profile Registration")
    st.markdown("Register new individual or corporate travelers into the agency database.")
    
    with st.form("cust_reg_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name:", placeholder="e.g. Ramesh Krishnan")
            email = st.text_input("Email Address:", placeholder="e.g. ramesh@example.com")
        with c2:
            phone = st.text_input("Phone Number:", placeholder="e.g. 9876543210")
            city = st.text_input("City:", placeholder="e.g. Erode / Coimbatore / Chennai")
            
        btn = st.form_submit_button("Register Customer Profile 💾")
        if btn:
            if not name or not email or not phone or not city:
                st.warning("Please fill in all customer details.")
            elif "@" not in email or "." not in email:
                st.error("Invalid email address format.")
            elif len(phone) < 10:
                st.error("Phone number must have at least 10 digits.")
            else:
                conn = get_db_connection()
                try:
                    conn.execute("""
                        INSERT INTO customers (name, email, phone, city)
                        VALUES (?, ?, ?, ?);
                    """, (name.strip(), email.strip(), phone.strip(), city.strip()))
                    conn.commit()
                    st.success(f"Customer **{name}** registered successfully!")
                except sqlite3.IntegrityError:
                    st.error("A customer with this email address already exists!")
                finally:
                    conn.close()

    st.markdown("#### 📋 Currently Registered Customers")
    all_custs = query_df("SELECT customer_id as ID, name as Name, email as Email, phone as Phone, city as City, created_at as Registered FROM customers ORDER BY customer_id DESC")
    st.dataframe(all_custs, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# View 5: Cancel Booking & 90% Refund
# -----------------------------------------------------------------------------
elif menu == "🔄 Cancel Booking & Refund":
    st.markdown("### 🔄 Booking Cancellation & Inventory Restoration")
    st.markdown("Cancel reservations, release seats immediately back into package capacity, and process standard 90% customer refunds.")
    
    active_bookings = query_df("""
        SELECT b.booking_id, c.name, p.destination, b.num_travelers, b.travel_date, b.total_amount
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN travel_packages p ON b.package_id = p.package_id
        WHERE b.booking_status = 'CONFIRMED'
        ORDER BY b.booking_id DESC;
    """)
    
    if active_bookings.empty:
        st.info("No active confirmed bookings found to cancel.")
    else:
        booking_map = {
            f"ID #{row['booking_id']} | {row['name']} -> {row['destination']} ({row['num_travelers']} seats, ₹{row['total_amount']:,.0f})": row['booking_id']
            for _, row in active_bookings.iterrows()
        }
        
        with st.form("cancel_form"):
            selected_label = st.selectbox("Select Booking to Cancel:", list(booking_map.keys()))
            b_id = booking_map[selected_label]
            b_row = active_bookings[active_bookings['booking_id'] == b_id].iloc[0]
            
            refund_calc = round(b_row['total_amount'] * 0.90, 2)
            cancellation_fee = round(b_row['total_amount'] * 0.10, 2)
            
            st.warning(f"⚠️ **Cancellation Policy:** 90% Refund = **₹{refund_calc:,.2f}** (10% standard processing fee = ₹{cancellation_fee:,.2f}).")
            reason = st.text_input("Cancellation Reason:", value="Customer Schedule Change / Medical Emergency")
            
            confirm = st.form_submit_button("Confirm Cancellation & Release Seats 🔄")
            if confirm:
                conn = get_db_connection()
                cur = conn.cursor()
                try:
                    cur.execute("UPDATE bookings SET booking_status = 'CANCELLED' WHERE booking_id = ?", (b_id,))
                    cur.execute("""
                        INSERT INTO cancellations (booking_id, cancellation_date, reason, refund_amount)
                        VALUES (?, ?, ?, ?);
                    """, (b_id, str(date.today()), reason, refund_calc))
                    cur.execute("UPDATE payments SET payment_status = 'REFUNDED' WHERE booking_id = ?", (b_id,))
                    conn.commit()
                    st.success(f"Booking `#{b_id}` has been CANCELLED.")
                    st.info(f"✅ **{b_row['num_travelers']} seats** released back to '{b_row['destination']}'. Refund of ₹{refund_calc:,.2f} recorded.")
                except Exception as ex:
                    conn.rollback()
                    st.error(f"Error cancelling booking: {ex}")
                finally:
                    conn.close()

# -----------------------------------------------------------------------------
# View 6: Live Tourism Trend Analytics
# -----------------------------------------------------------------------------
elif menu == "📊 Tourism Trend Analytics":
    st.markdown("### 📊 Live Tourism Trend Analytics & Business Intelligence")
    st.markdown("Visualizations generated dynamically from the live database using Pandas and Plotly.")
    
    # Load Master Analytics Dataset
    master_df = query_df("""
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
    
    master_df['booking_date'] = pd.to_datetime(master_df['booking_date'])
    master_df['month'] = master_df['booking_date'].dt.strftime('%B')
    master_df['month_num'] = master_df['booking_date'].dt.month

    # Row 1: Charts
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.markdown("#### 1. Top Destinations by Confirmed Guests")
        dest_df = master_df[master_df['booking_status'] != 'CANCELLED'].groupby('destination')['num_travelers'].sum().reset_index()
        dest_df = dest_df.sort_values(by='num_travelers', ascending=True)
        fig1 = px.bar(
            dest_df, x='num_travelers', y='destination', orientation='h',
            labels={'num_travelers': 'Total Confirmed Guests', 'destination': 'Destination'},
            color='num_travelers', color_continuous_scale='Viridis', text_auto=True
        )
        fig1.update_layout(showlegend=False, height=360, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig1, use_container_width=True)

    with r1_col2:
        st.markdown("#### 2. Monthly & Seasonal Demand Curve")
        monthly_df = master_df.groupby(['month_num', 'month'])['num_travelers'].sum().reset_index().sort_values('month_num')
        fig2 = px.line(
            monthly_df, x='month', y='num_travelers', markers=True,
            labels={'num_travelers': 'Total Guests', 'month': 'Month'},
            line_shape='spline'
        )
        fig2.update_traces(line_color='#2563EB', line_width=3, marker=dict(size=9, color='#1E40AF'))
        fig2.update_layout(height=360, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2: Charts
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.markdown("#### 3. Revenue Share by Tour Category")
        cat_df = master_df[master_df['booking_status'] != 'CANCELLED'].groupby('category')['total_amount'].sum().reset_index()
        fig3 = px.pie(
            cat_df, values='total_amount', names='category', hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        fig3.update_layout(height=340, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig3, use_container_width=True)

    with r2_col2:
        st.markdown("#### 4. Booking Lifecycle & Cancellation Rate")
        status_df = master_df['booking_status'].value_counts().reset_index()
        status_df.columns = ['Status', 'Count']
        fig4 = px.bar(
            status_df, x='Status', y='Count', color='Status',
            color_discrete_map={'CONFIRMED': '#3B82F6', 'COMPLETED': '#10B981', 'CANCELLED': '#EF4444'},
            text_auto=True
        )
        fig4.update_layout(showlegend=False, height=340, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------------------------------------------
# View 7: Raw Database Explorer
# -----------------------------------------------------------------------------
elif menu == "🗃️ Raw Database Explorer":
    st.markdown("### 🗃️ Relational Database Table Explorer")
    st.markdown("Inspect live SQL tables, execute queries, and download data as CSV.")
    
    tables = ["customers", "travel_packages", "bookings", "payments", "cancellations", "v_booking_summary", "v_destination_revenue"]
    selected_tbl = st.selectbox("Select Table or View:", tables)
    
    tbl_df = query_df(f"SELECT * FROM {selected_tbl};")
    st.markdown(f"**Showing `{len(tbl_df)}` records from `{selected_tbl}`:**")
    st.dataframe(tbl_df, use_container_width=True)
    
    csv = tbl_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download {selected_tbl}.csv 📥",
        data=csv,
        file_name=f"{selected_tbl}.csv",
        mime="text/csv",
    )

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem;">
    <b>Travel Agency Booking & Tourism Trend Analysis System</b> (Scenario 21)<br/>
    Student: <b>Kishor K</b> (RegNo: 732925ITR051) | Class: <b>25IT3A</b> | VCET, Erode - 12
</div>
""", unsafe_allow_html=True)
