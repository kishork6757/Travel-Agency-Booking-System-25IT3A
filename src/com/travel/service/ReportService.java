package com.travel.service;

import com.travel.dao.ReportDAO;
import com.travel.util.ConsoleFormatter;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

public class ReportService {
    private final ReportDAO reportDAO;

    public ReportService() {
        this.reportDAO = new ReportDAO();
    }

    public void displayDestinationRevenueReport() throws SQLException {
        List<Map<String, Object>> list = reportDAO.getDestinationRevenueReport();
        ConsoleFormatter.printHeader("Destination Popularity & Revenue Performance Report");
        
        System.out.printf("%-5s | %-30s | %-13s | %-8s | %-7s | %-9s | %-12s | %-14s%n",
                "ID", "Destination", "Category", "Capacity", "Booked", "Remaining", "Occupancy %", "Total Revenue");
        ConsoleFormatter.printDivider();

        double grandTotal = 0.0;
        int totalBookedGuests = 0;

        for (Map<String, Object> r : list) {
            double rev = (double) r.get("totalRevenue");
            int guests = (int) r.get("confirmedGuests");
            grandTotal += rev;
            totalBookedGuests += guests;

            System.out.printf("%-5d | %-30s | %-13s | %8d | %7d | %9d | %11.1f%% | Rs. %11.2f%n",
                    (int) r.get("packageId"),
                    (String) r.get("destination"),
                    (String) r.get("category"),
                    (int) r.get("maxCapacity"),
                    guests,
                    (int) r.get("remainingSeats"),
                    (double) r.get("occupancyRate"),
                    rev
            );
        }
        ConsoleFormatter.printDivider();
        System.out.printf(ConsoleFormatter.BOLD + "%-5s | %-30s | %-13s | %8s | %7d | %9s | %12s | Rs. %11.2f%n" + ConsoleFormatter.RESET,
                "TOTAL", "All Operational Destinations", "-", "-", totalBookedGuests, "-", "-", grandTotal);
    }

    public void displayRecentBookingsSummary() throws SQLException {
        List<Map<String, Object>> list = reportDAO.getRecentBookingsSummary();
        ConsoleFormatter.printHeader("Operational Booking Summary (Recent Transactions)");

        System.out.printf("%-6s | %-16s | %-12s | %-26s | %-6s | %-11s | %-13s | %-10s | %-9s%n",
                "BookID", "Customer", "Phone", "Destination", "Guests", "Travel Date", "Amount (Rs.)", "Status", "Payment");
        ConsoleFormatter.printDivider();

        for (Map<String, Object> r : list) {
            System.out.printf("%-6d | %-16s | %-12s | %-26s | %6d | %-11s | %13.2f | %-10s | %-9s%n",
                    (int) r.get("bookingId"),
                    (String) r.get("customerName"),
                    (String) r.get("customerPhone"),
                    (String) r.get("destination"),
                    (int) r.get("numTravelers"),
                    (String) r.get("travelDate"),
                    (double) r.get("totalAmount"),
                    (String) r.get("bookingStatus"),
                    (String) r.get("paymentStatus")
            );
        }
        ConsoleFormatter.printDivider();
    }
}
