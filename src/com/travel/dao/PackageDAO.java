package com.travel.dao;

import com.travel.model.TravelPackage;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class PackageDAO {

    public boolean addPackage(TravelPackage pkg) throws SQLException {
        String sql = "INSERT INTO travel_packages (destination, duration_days, price_per_person, max_capacity, category, season) " +
                     "VALUES (?, ?, ?, ?, ?, ?)";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            
            pstmt.setString(1, pkg.getDestination());
            pstmt.setInt(2, pkg.getDurationDays());
            pstmt.setDouble(3, pkg.getPricePerPerson());
            pstmt.setInt(4, pkg.getMaxCapacity());
            pstmt.setString(5, pkg.getCategory());
            pstmt.setString(6, pkg.getSeason());
            
            int affected = pstmt.executeUpdate();
            if (affected > 0) {
                try (ResultSet rs = pstmt.getGeneratedKeys()) {
                    if (rs.next()) {
                        pkg.setPackageId(rs.getInt(1));
                    }
                }
                return true;
            }
        }
        return false;
    }

    public List<TravelPackage> getAllPackages() throws SQLException {
        List<TravelPackage> list = new ArrayList<>();
        String sql = "SELECT package_id, destination, duration_days, price_per_person, max_capacity, category, season " +
                     "FROM travel_packages ORDER BY package_id ASC";
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            
            while (rs.next()) {
                TravelPackage p = new TravelPackage(
                    rs.getInt("package_id"),
                    rs.getString("destination"),
                    rs.getInt("duration_days"),
                    rs.getDouble("price_per_person"),
                    rs.getInt("max_capacity"),
                    rs.getString("category"),
                    rs.getString("season")
                );
                list.add(p);
            }
        }
        return list;
    }

    public TravelPackage getPackageById(int packageId) throws SQLException {
        String sql = "SELECT package_id, destination, duration_days, price_per_person, max_capacity, category, season " +
                     "FROM travel_packages WHERE package_id = ?";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setInt(1, packageId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return new TravelPackage(
                        rs.getInt("package_id"),
                        rs.getString("destination"),
                        rs.getInt("duration_days"),
                        rs.getDouble("price_per_person"),
                        rs.getInt("max_capacity"),
                        rs.getString("category"),
                        rs.getString("season")
                    );
                }
            }
        }
        return null;
    }

    public int getBookedSeats(int packageId) throws SQLException {
        String sql = "SELECT COALESCE(SUM(num_travelers), 0) FROM bookings " +
                     "WHERE package_id = ? AND booking_status = 'CONFIRMED'";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setInt(1, packageId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt(1);
                }
            }
        }
        return 0;
    }

    public int getRemainingCapacity(int packageId) throws SQLException {
        TravelPackage pkg = getPackageById(packageId);
        if (pkg == null) return 0;
        int booked = getBookedSeats(packageId);
        return Math.max(0, pkg.getMaxCapacity() - booked);
    }
}
