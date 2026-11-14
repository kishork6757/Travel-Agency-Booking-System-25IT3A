package com.travel.dao;

import com.travel.model.Booking;
import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

public class BookingDAO {

    public boolean createBooking(Booking booking) throws SQLException {
        String sql = "INSERT INTO bookings (customer_id, package_id, booking_date, travel_date, " +
                     "num_travelers, total_amount, booking_status) VALUES (?, ?, ?, ?, ?, ?, ?)";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            
            pstmt.setInt(1, booking.getCustomerId());
            pstmt.setInt(2, booking.getPackageId());
            pstmt.setString(3, booking.getBookingDate());
            pstmt.setString(4, booking.getTravelDate());
            pstmt.setInt(5, booking.getNumTravelers());
            pstmt.setDouble(6, booking.getTotalAmount());
            pstmt.setString(7, booking.getBookingStatus());
            
            int affected = pstmt.executeUpdate();
            if (affected > 0) {
                try (ResultSet rs = pstmt.getGeneratedKeys()) {
                    if (rs.next()) {
                        booking.setBookingId(rs.getInt(1));
                    }
                }
                return true;
            }
        }
        return false;
    }

    public List<Booking> getAllBookings() throws SQLException {
        List<Booking> list = new ArrayList<>();
        String sql = "SELECT b.booking_id, b.customer_id, b.package_id, b.booking_date, b.travel_date, " +
                     "b.num_travelers, b.total_amount, b.booking_status, " +
                     "c.name AS customer_name, p.destination " +
                     "FROM bookings b " +
                     "JOIN customers c ON b.customer_id = c.customer_id " +
                     "JOIN travel_packages p ON b.package_id = p.package_id " +
                     "ORDER BY b.booking_id DESC";
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                Booking b = new Booking(
                    rs.getInt("booking_id"),
                    rs.getInt("customer_id"),
                    rs.getInt("package_id"),
                    rs.getString("booking_date"),
                    rs.getString("travel_date"),
                    rs.getInt("num_travelers"),
                    rs.getDouble("total_amount"),
                    rs.getString("booking_status")
                );
                b.setCustomerName(rs.getString("customer_name"));
                b.setDestination(rs.getString("destination"));
                list.add(b);
            }
        }
        return list;
    }

    public Booking getBookingById(int bookingId) throws SQLException {
        String sql = "SELECT b.booking_id, b.customer_id, b.package_id, b.booking_date, b.travel_date, " +
                     "b.num_travelers, b.total_amount, b.booking_status, " +
                     "c.name AS customer_name, p.destination " +
                     "FROM bookings b " +
                     "JOIN customers c ON b.customer_id = c.customer_id " +
                     "JOIN travel_packages p ON b.package_id = p.package_id " +
                     "WHERE b.booking_id = ?";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setInt(1, bookingId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    Booking b = new Booking(
                        rs.getInt("booking_id"),
                        rs.getInt("customer_id"),
                        rs.getInt("package_id"),
                        rs.getString("booking_date"),
                        rs.getString("travel_date"),
                        rs.getInt("num_travelers"),
                        rs.getDouble("total_amount"),
                        rs.getString("booking_status")
                    );
                    b.setCustomerName(rs.getString("customer_name"));
                    b.setDestination(rs.getString("destination"));
                    return b;
                }
            }
        }
        return null;
    }

    /**
     * Executes atomic cancellation transaction (ACID compliance):
     * 1. Updates booking status to 'CANCELLED'
     * 2. Inserts record into cancellations table
     * 3. Updates payment status to 'REFUNDED'
     */
    public boolean processCancellation(int bookingId, String reason, double refundAmount) throws SQLException {
        Connection conn = DBConnection.getConnection();
        boolean autoCommitOrig = conn.getAutoCommit();
        
        try {
            conn.setAutoCommit(false); // Begin Transaction
            
            // Step 1: Update Booking status
            String updateBookingSql = "UPDATE bookings SET booking_status = 'CANCELLED' WHERE booking_id = ?";
            try (PreparedStatement pstmt1 = conn.prepareStatement(updateBookingSql)) {
                pstmt1.setInt(1, bookingId);
                pstmt1.executeUpdate();
            }
            
            // Step 2: Insert into cancellations table
            String insertCancelSql = "INSERT INTO cancellations (booking_id, cancellation_date, reason, refund_amount) " +
                                     "VALUES (?, ?, ?, ?)";
            try (PreparedStatement pstmt2 = conn.prepareStatement(insertCancelSql)) {
                pstmt2.setInt(1, bookingId);
                pstmt2.setString(2, LocalDate.now().toString());
                pstmt2.setString(3, reason);
                pstmt2.setDouble(4, refundAmount);
                pstmt2.executeUpdate();
            }
            
            // Step 3: Update Payment status to REFUNDED
            String updatePaymentSql = "UPDATE payments SET payment_status = 'REFUNDED' WHERE booking_id = ?";
            try (PreparedStatement pstmt3 = conn.prepareStatement(updatePaymentSql)) {
                pstmt3.setInt(1, bookingId);
                pstmt3.executeUpdate();
            }
            
            conn.commit(); // Commit Transaction
            return true;
        } catch (SQLException ex) {
            conn.rollback(); // Rollback on failure
            throw ex;
        } finally {
            conn.setAutoCommit(autoCommitOrig);
        }
    }
}
