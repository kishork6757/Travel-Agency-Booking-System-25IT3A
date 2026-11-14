package com.travel.dao;

import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ReportDAO {

    public List<Map<String, Object>> getDestinationRevenueReport() throws SQLException {
        List<Map<String, Object>> report = new ArrayList<>();
        String sql = "SELECT package_id, destination, category, max_capacity, " +
                     "total_confirmed_guests, remaining_seats, occupancy_rate_pct, total_revenue " +
                     "FROM v_destination_revenue ORDER BY total_revenue DESC";
        
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                Map<String, Object> row = new HashMap<>();
                row.put("packageId", rs.getInt("package_id"));
                row.put("destination", rs.getString("destination"));
                row.put("category", rs.getString("category"));
                row.put("maxCapacity", rs.getInt("max_capacity"));
                row.put("confirmedGuests", rs.getInt("total_confirmed_guests"));
                row.put("remainingSeats", rs.getInt("remaining_seats"));
                row.put("occupancyRate", rs.getDouble("occupancy_rate_pct"));
                row.put("totalRevenue", rs.getDouble("total_revenue"));
                report.add(row);
            }
        }
        return report;
    }

    public List<Map<String, Object>> getRecentBookingsSummary() throws SQLException {
        List<Map<String, Object>> report = new ArrayList<>();
        String sql = "SELECT booking_id, customer_name, customer_phone, destination, " +
                     "num_travelers, travel_date, total_amount, booking_status, payment_status " +
                     "FROM v_booking_summary ORDER BY booking_id DESC LIMIT 10";
        
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                Map<String, Object> row = new HashMap<>();
                row.put("bookingId", rs.getInt("booking_id"));
                row.put("customerName", rs.getString("customer_name"));
                row.put("customerPhone", rs.getString("customer_phone"));
                row.put("destination", rs.getString("destination"));
                row.put("numTravelers", rs.getInt("num_travelers"));
                row.put("travelDate", rs.getString("travel_date"));
                row.put("totalAmount", rs.getDouble("total_amount"));
                row.put("bookingStatus", rs.getString("booking_status"));
                row.put("paymentStatus", rs.getString("payment_status"));
                report.add(row);
            }
        }
        return report;
    }
}
