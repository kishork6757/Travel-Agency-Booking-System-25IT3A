"""
=============================================================================
Travel Agency Booking and Tourism Trend Analysis System
Foundations of Data Science (25ITC31) - Practical Implementation
Student: Kishor K (RegNo: 732925ITR051) | Class: 25IT3A
=============================================================================
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication style aesthetics
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "travel_agency.db")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")
os.makedirs(VIZ_DIR, exist_ok=True)

STUDENT_WATERMARK = "Kishor K (732925ITR051) | Scenario 21 - Tourism Trend Analysis"

def load_data_from_db(db_path: str):
    """Retrieve raw dataset tables from SQLite database into Pandas DataFrames."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    packages_df = pd.read_sql_query("SELECT * FROM travel_packages", conn)
    bookings_df = pd.read_sql_query("SELECT * FROM bookings", conn)
    payments_df = pd.read_sql_query("SELECT * FROM payments", conn)
    cancellations_df = pd.read_sql_query("SELECT * FROM cancellations", conn)
    
    conn.close()
    print("[INFO] Successfully fetched data from database.")
    return customers_df, packages_df, bookings_df, payments_df, cancellations_df

def preprocess_and_merge(customers_df, packages_df, bookings_df, payments_df, cancellations_df):
    """
    Data Cleaning, Transformation & Feature Engineering:
    - Date parsing
    - Handling missing values
    - Calculating lead time (days between booking and travel)
    - Calculating total revenue and cancellation status
    """
    print("\n" + "="*70)
    print("DATA PREPROCESSING & FEATURE ENGINEERING")
    print("="*70)
    
    # 1. Date conversion
    bookings_df['booking_date'] = pd.to_datetime(bookings_df['booking_date'])
    bookings_df['travel_date'] = pd.to_datetime(bookings_df['travel_date'])
    
    # 2. Derive lead time
    bookings_df['lead_time_days'] = (bookings_df['travel_date'] - bookings_df['booking_date']).dt.days
    
    # 3. Derive Month-Year and Month name for seasonal trends
    bookings_df['booking_month'] = bookings_df['booking_date'].dt.strftime('%B')
    bookings_df['booking_month_num'] = bookings_df['booking_date'].dt.month
    bookings_df['travel_month'] = bookings_df['travel_date'].dt.strftime('%B')
    
    # 4. Merge datasets into master analytical dataframe
    master_df = bookings_df.merge(packages_df, on='package_id', how='left', suffixes=('', '_pkg'))
    master_df = master_df.merge(customers_df, on='customer_id', how='left', suffixes=('', '_cust'))
    master_df = master_df.merge(payments_df[['booking_id', 'payment_method', 'payment_status']], on='booking_id', how='left')
    master_df = master_df.merge(cancellations_df[['booking_id', 'reason', 'refund_amount']], on='booking_id', how='left')
    
    # 5. Fill missing values
    master_df['refund_amount'] = master_df['refund_amount'].fillna(0.0)
    master_df['reason'] = master_df['reason'].fillna("None (Active Booking)")
    master_df['payment_status'] = master_df['payment_status'].fillna("PENDING")
    
    # 6. Derived financial feature: net revenue realized (after refunds)
    master_df['net_revenue'] = np.where(
        master_df['booking_status'] == 'CANCELLED',
        master_df['total_amount'] - master_df['refund_amount'],
        master_df['total_amount']
    )
    
    print(f"Master Dataset Shape: {master_df.shape[0]} rows x {master_df.shape[1]} columns")
    print(f"Total Unique Customers: {master_df['customer_id'].nunique()}")
    print(f"Total Unique Packages: {master_df['package_id'].nunique()}")
    print(f"Gross Booking Volume: Rs. {master_df['total_amount'].sum():,.2f}")
    print(f"Net Realized Revenue: Rs. {master_df['net_revenue'].sum():,.2f}")
    print(f"Overall Cancellation Rate: {(master_df['booking_status'] == 'CANCELLED').mean() * 100:.2f}%")
    print("="*70 + "\n")
    
    return master_df

def generate_visualizations(master_df, packages_df):
    """Generate 6 distinct, publication-quality visualizations."""
    print("[INFO] Generating visualizations...")
    
    # -------------------------------------------------------------------------
    # Chart 1: Destination Popularity (Total Travelers Booked per Destination)
    # -------------------------------------------------------------------------
    plt.figure(figsize=(10, 6))
    dest_demand = master_df[master_df['booking_status'] != 'CANCELLED'].groupby('destination')['num_travelers'].sum().reset_index()
    dest_demand = dest_demand.sort_values(by='num_travelers', ascending=True)
    
    colors = sns.color_palette("viridis", len(dest_demand))
    bars = plt.barh(dest_demand['destination'], dest_demand['num_travelers'], color=colors, edgecolor='#333333', height=0.65)
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.3, bar.get_y() + bar.get_height()/2, f'{int(width)} travelers', 
                 va='center', ha='left', fontsize=10, fontweight='bold', color='#222222')
        
    plt.title("Top Tourist Destinations by Confirmed Traveler Headcount", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Total Travelers Booked", fontsize=11, labelpad=8)
    plt.ylabel("Destination", fontsize=11)
    plt.xlim(0, dest_demand['num_travelers'].max() + 3)
    plt.figtext(0.99, 0.01, STUDENT_WATERMARK, ha='right', fontsize=8, color='gray', style='italic')
    plt.tight_layout()
    chart1_path = os.path.join(VIZ_DIR, "01_destination_popularity.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f" -> Saved: {chart1_path}")

    # -------------------------------------------------------------------------
    # Chart 2: Monthly & Seasonal Booking Demand Trends
    # -------------------------------------------------------------------------
    plt.figure(figsize=(11, 5.5))
    monthly_trend = master_df.groupby(['booking_month_num', 'booking_month']).agg(
        total_bookings=('booking_id', 'count'),
        total_guests=('num_travelers', 'sum'),
        total_revenue=('total_amount', 'sum')
    ).reset_index().sort_values('booking_month_num')
    
    plt.plot(monthly_trend['booking_month'], monthly_trend['total_guests'], 
             marker='o', markersize=8, linewidth=2.5, color='#1f77b4', label='Total Travelers Headcount')
    plt.plot(monthly_trend['booking_month'], monthly_trend['total_bookings'], 
             marker='s', markersize=7, linewidth=2.0, color='#ff7f0e', linestyle='--', label='Number of Bookings')
    
    for i, txt in enumerate(monthly_trend['total_guests']):
        plt.annotate(f"{txt} guests", (monthly_trend['booking_month'].iloc[i], txt + 0.6),
                     ha='center', fontsize=9, fontweight='bold', color='#1f77b4')

    plt.title("2026 Monthly & Seasonal Tourism Demand Trajectory", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Booking Month", fontsize=11, labelpad=8)
    plt.ylabel("Volume Count", fontsize=11)
    plt.ylim(0, monthly_trend['total_guests'].max() + 3)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.figtext(0.99, 0.01, STUDENT_WATERMARK, ha='right', fontsize=8, color='gray', style='italic')
    plt.tight_layout()
    chart2_path = os.path.join(VIZ_DIR, "02_monthly_booking_trends.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f" -> Saved: {chart2_path}")

    # -------------------------------------------------------------------------
    # Chart 3: Revenue Contribution by Tour Category (Donut Chart)
    # -------------------------------------------------------------------------
    plt.figure(figsize=(8, 7))
    cat_rev = master_df[master_df['booking_status'] != 'CANCELLED'].groupby('category')['total_amount'].sum()
    
    colors = ['#2ca02c', '#d62728', '#9467bd', '#8c564b', '#17becf']
    explode = [0.03] * len(cat_rev)
    
    wedges, texts, autotexts = plt.pie(
        cat_rev, 
        labels=cat_rev.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=colors,
        explode=explode,
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=2),
        pctdistance=0.75,
        textprops=dict(fontsize=11)
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_weight('bold')
        at.set_color('white')
        
    plt.title("Revenue Share by Package Category (Total: Rs. {:,.0f})".format(cat_rev.sum()), 
              fontsize=13, fontweight='bold', pad=15)
    plt.figtext(0.99, 0.01, STUDENT_WATERMARK, ha='right', fontsize=8, color='gray', style='italic')
    plt.tight_layout()
    chart3_path = os.path.join(VIZ_DIR, "03_revenue_by_category.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f" -> Saved: {chart3_path}")

    # -------------------------------------------------------------------------
    # Chart 4: Booking Status Distribution (Confirmed vs Cancelled vs Completed)
    # -------------------------------------------------------------------------
    plt.figure(figsize=(8, 5.5))
    status_counts = master_df['booking_status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    
    status_colors = {'COMPLETED': '#2b9348', 'CONFIRMED': '#0077b6', 'CANCELLED': '#d90429'}
    palette = [status_colors.get(s, '#4a4e69') for s in status_counts['status']]
    
    ax = sns.barplot(x='status', y='count', data=status_counts, palette=palette, edgecolor='#333333')
    for p in ax.patches:
        height = p.get_height()
        pct = (height / len(master_df)) * 100
        ax.annotate(f'{int(height)} ({pct:.1f}%)', 
                    (p.get_x() + p.get_width() / 2., height + 0.3),
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.title("Distribution of Booking Outcomes and Cancellation Rates", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Booking Lifecycle Status", fontsize=11, labelpad=8)
    plt.ylabel("Number of Bookings", fontsize=11)
    plt.ylim(0, status_counts['count'].max() + 3)
    plt.figtext(0.99, 0.01, STUDENT_WATERMARK, ha='right', fontsize=8, color='gray', style='italic')
    plt.tight_layout()
    chart4_path = os.path.join(VIZ_DIR, "04_booking_status_distribution.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f" -> Saved: {chart4_path}")

    # -------------------------------------------------------------------------
    # Chart 5: Traveler Group Size Distribution (Histogram with KDE)
    # -------------------------------------------------------------------------
    plt.figure(figsize=(9, 5.5))
    sns.histplot(master_df['num_travelers'], discrete=True, kde=True, color='#023e8a', edgecolor='black', alpha=0.6)
    
    mean_val = master_df['num_travelers'].mean()
    median_val = master_df['num_travelers'].median()
    plt.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean Party Size: {mean_val:.2f}')
    plt.axvline(median_val, color='green', linestyle=':', linewidth=2, label=f'Median Party Size: {median_val:.0f}')
    
    plt.title("Traveler Group / Party Size Distribution Analysis", fontsize=13, fontweight='bold', pad=15)
    plt.xlabel("Number of Travelers per Booking", fontsize=11, labelpad=8)
    plt.ylabel("Frequency (Count)", fontsize=11)
    plt.legend(frameon=True, facecolor='white')
    plt.figtext(0.99, 0.01, STUDENT_WATERMARK, ha='right', fontsize=8, color='gray', style='italic')
    plt.tight_layout()
    chart5_path = os.path.join(VIZ_DIR, "05_traveler_group_size_distribution.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f" -> Saved: {chart5_path}")

    # -------------------------------------------------------------------------
    # Chart 6: Package Capacity Utilization & Revenue Heatmap Correlation
    # -------------------------------------------------------------------------
    plt.figure(figsize=(8, 6))
    pkg_analysis = master_df.groupby('package_id').agg(
        duration=('duration_days', 'first'),
        unit_price=('price_per_person', 'first'),
        capacity=('max_capacity', 'first'),
        booked_guests=('num_travelers', lambda x: x[master_df.loc[x.index, 'booking_status'] != 'CANCELLED'].sum()),
        total_revenue=('total_amount', lambda x: x[master_df.loc[x.index, 'booking_status'] != 'CANCELLED'].sum())
    )
    pkg_analysis['occupancy_rate'] = (pkg_analysis['booked_guests'] / pkg_analysis['capacity']) * 100
    
    corr_matrix = pkg_analysis.corr()
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='Blues', vmin=-1, vmax=1,
                linewidths=1, linecolor='white', cbar_kws={'label': 'Pearson Correlation'})
    
    plt.title("Correlation Matrix: Package Attributes vs Demand & Revenue", fontsize=13, fontweight='bold', pad=15)
    plt.figtext(0.99, 0.01, STUDENT_WATERMARK, ha='right', fontsize=8, color='gray', style='italic')
    plt.tight_layout()
    chart6_path = os.path.join(VIZ_DIR, "06_package_occupancy_heatmap.png")
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print(f" -> Saved: {chart6_path}")

    print("\n[SUCCESS] All 6 charts generated and saved successfully to:", VIZ_DIR)

def main():
    print("="*70)
    print("TRAVEL AGENCY TOURISM TREND ANALYSIS SYSTEM - PYTHON ANALYTICS")
    print(f"Author: {STUDENT_WATERMARK}")
    print("="*70)
    
    customers_df, packages_df, bookings_df, payments_df, cancellations_df = load_data_from_db(DB_PATH)
    master_df = preprocess_and_merge(customers_df, packages_df, bookings_df, payments_df, cancellations_df)
    generate_visualizations(master_df, packages_df)

if __name__ == "__main__":
    main()
