package com.travel;

import com.travel.exception.BookingNotFoundException;
import com.travel.exception.CapacityExceededException;
import com.travel.exception.InvalidInputException;
import com.travel.model.Booking;
import com.travel.model.Customer;
import com.travel.model.Payment;
import com.travel.model.TravelPackage;
import com.travel.service.BookingService;
import com.travel.service.CustomerService;
import com.travel.service.PackageService;
import com.travel.service.ReportService;
import com.travel.util.ConsoleFormatter;
import com.travel.util.DBInitializer;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.sql.SQLException;
import java.util.List;
import java.util.Scanner;

public class Main {
    private static final Scanner scanner = new Scanner(System.in);
    private static final CustomerService customerService = new CustomerService();
    private static final PackageService packageService = new PackageService();
    private static final BookingService bookingService = new BookingService();
    private static final ReportService reportService = new ReportService();

    public static void main(String[] args) {
        // Initialize and verify DB connection
        DBInitializer.initializeDatabaseIfEmpty();

        boolean running = true;
        while (running) {
            printMainMenu();
            System.out.print(ConsoleFormatter.CYAN + "Enter your choice (1 - 12, or 0 to Exit): " + ConsoleFormatter.RESET);
            String input = scanner.nextLine().trim();

            try {
                switch (input) {
                    case "1": handleRegisterCustomer(); break;
                    case "2": handleViewAllCustomers(); break;
                    case "3": handleViewAllPackages(); break;
                    case "4": handleAddNewPackage(); break;
                    case "5": handleCheckSeatAvailability(); break;
                    case "6": handleBookPackage(); break;
                    case "7": handleViewAllBookings(); break;
                    case "8": handleCancelBooking(); break;
                    case "9": handleViewPayments(); break;
                    case "10": handleDestinationRevenueReport(); break;
                    case "11": handleRecentBookingsLog(); break;
                    case "12": handleRunPythonTrendAnalysis(); break;
                    case "0":
                    case "exit":
                        running = false;
                        ConsoleFormatter.printSuccess("Thank you for using the Travel Agency Management System. Goodbye!");
                        break;
                    default:
                        ConsoleFormatter.printWarning("Invalid option! Please enter a number between 0 and 12.");
                }
            } catch (Exception e) {
                ConsoleFormatter.printError("An unexpected error occurred: " + e.getMessage());
            }

            if (running) {
                System.out.println("\nPress [ENTER] to return to the Main Menu...");
                scanner.nextLine();
            }
        }
    }

    private static void printMainMenu() {
        ConsoleFormatter.printHeader("Travel Agency Booking & Tourism Trend Analysis System");
        System.out.println(ConsoleFormatter.WHITE + "Student: Kishor K | Reg No: 732925ITR051 | Class: 25IT3A | Scenario 21" + ConsoleFormatter.RESET);
        ConsoleFormatter.printDivider();
        System.out.println(ConsoleFormatter.YELLOW + "[CUSTOMER MANAGEMENT]" + ConsoleFormatter.RESET);
        System.out.println("  1. Register New Customer Profile");
        System.out.println("  2. View All Registered Customers");
        System.out.println(ConsoleFormatter.YELLOW + "[PACKAGE CATALOG & INVENTORY]" + ConsoleFormatter.RESET);
        System.out.println("  3. View All Travel Packages");
        System.out.println("  4. Add New Travel Package");
        System.out.println("  5. Check Live Seat Availability & Remaining Capacity");
        System.out.println(ConsoleFormatter.YELLOW + "[BOOKING & CANCELLATION OPERATIONS]" + ConsoleFormatter.RESET);
        System.out.println("  6. Book Travel Package (with Capacity Verification & Anti-Overbooking)");
        System.out.println("  7. View All Bookings Log");
        System.out.println("  8. Cancel Booking (Automatic Capacity Release & 90% Refund)");
        System.out.println(ConsoleFormatter.YELLOW + "[FINANCES & REPORTS]" + ConsoleFormatter.RESET);
        System.out.println("  9. View All Payment Records");
        System.out.println(" 10. Destination Popularity, Occupancy & Revenue Performance Report");
        System.out.println(" 11. Recent Transactions & Operational Summary");
        System.out.println(ConsoleFormatter.YELLOW + "[TOURISM TREND ANALYTICS]" + ConsoleFormatter.RESET);
        System.out.println(" 12. Run Python Data Preprocessing & Generate Visualizations");
        System.out.println(ConsoleFormatter.RED + "  0. Exit System" + ConsoleFormatter.RESET);
        ConsoleFormatter.printDivider();
    }

    private static void handleRegisterCustomer() throws SQLException {
        ConsoleFormatter.printSubHeader("Register New Customer");
        System.out.print("Enter Customer Name: ");
        String name = scanner.nextLine();
        System.out.print("Enter Email Address: ");
        String email = scanner.nextLine();
        System.out.print("Enter Phone Number: ");
        String phone = scanner.nextLine();
        System.out.print("Enter City: ");
        String city = scanner.nextLine();

        try {
            boolean success = customerService.registerCustomer(name, email, phone, city);
            if (success) {
                ConsoleFormatter.printSuccess("Customer registered successfully!");
            }
        } catch (InvalidInputException e) {
            ConsoleFormatter.printError(e.getMessage());
        }
    }

    private static void handleViewAllCustomers() throws SQLException {
        ConsoleFormatter.printSubHeader("Registered Customers List");
        List<Customer> list = customerService.getAllCustomers();
        if (list.isEmpty()) {
            ConsoleFormatter.printWarning("No customers registered yet.");
            return;
        }
        System.out.printf("%-5s | %-18s | %-24s | %-12s | %-12s%n", "ID", "Name", "Email", "Phone", "City");
        ConsoleFormatter.printDivider();
        for (Customer c : list) {
            System.out.printf("%-5d | %-18s | %-24s | %-12s | %-12s%n",
                    c.getCustomerId(), c.getName(), c.getEmail(), c.getPhone(), c.getCity());
        }
    }

    private static void handleViewAllPackages() throws SQLException {
        ConsoleFormatter.printSubHeader("Available Travel Packages");
        List<TravelPackage> list = packageService.getAllPackages();
        if (list.isEmpty()) {
            ConsoleFormatter.printWarning("No travel packages available.");
            return;
        }
        System.out.printf("%-5s | %-30s | %-8s | %-12s | %-8s | %-13s | %-8s%n", 
                "ID", "Destination", "Duration", "Price/Person", "Capacity", "Category", "Season");
        ConsoleFormatter.printDivider();
        for (TravelPackage p : list) {
            System.out.printf("%-5d | %-30s | %2d Days | Rs. %8.2f | %8d | %-13s | %-8s%n",
                    p.getPackageId(), p.getDestination(), p.getDurationDays(),
                    p.getPricePerPerson(), p.getMaxCapacity(), p.getCategory(), p.getSeason());
        }
    }

    private static void handleAddNewPackage() throws SQLException {
        ConsoleFormatter.printSubHeader("Create New Travel Package");
        System.out.print("Destination Name: ");
        String dest = scanner.nextLine();
        System.out.print("Duration (in days): ");
        int days = Integer.parseInt(scanner.nextLine().trim());
        System.out.print("Price per Person (Rs.): ");
        double price = Double.parseDouble(scanner.nextLine().trim());
        System.out.print("Maximum Seating Capacity: ");
        int capacity = Integer.parseInt(scanner.nextLine().trim());
        System.out.print("Category (Domestic/International/Adventure/Pilgrimage/Luxury): ");
        String category = scanner.nextLine().trim();
        System.out.print("Season (Summer/Monsoon/Autumn/Winter/All Season): ");
        String season = scanner.nextLine().trim();

        try {
            boolean success = packageService.addPackage(dest, days, price, capacity, category, season);
            if (success) {
                ConsoleFormatter.printSuccess("Travel package '" + dest + "' created successfully!");
            }
        } catch (InvalidInputException e) {
            ConsoleFormatter.printError(e.getMessage());
        }
    }

    private static void handleCheckSeatAvailability() throws SQLException {
        ConsoleFormatter.printSubHeader("Check Live Seat Availability");
        System.out.print("Enter Package ID: ");
        int pkgId = Integer.parseInt(scanner.nextLine().trim());

        TravelPackage pkg = packageService.getPackageById(pkgId);
        if (pkg == null) {
            ConsoleFormatter.printError("Travel package ID " + pkgId + " not found.");
            return;
        }

        int remaining = packageService.getAvailableSeats(pkgId);
        int booked = pkg.getMaxCapacity() - remaining;

        System.out.println("Destination     : " + pkg.getDestination());
        System.out.println("Category        : " + pkg.getCategory());
        System.out.println("Total Capacity  : " + pkg.getMaxCapacity() + " seats");
        System.out.println("Booked Seats    : " + booked + " seats");
        System.out.println(ConsoleFormatter.GREEN + "Remaining Seats : " + remaining + " seats" + ConsoleFormatter.RESET);

        if (remaining == 0) {
            ConsoleFormatter.printWarning("STATUS: FULLY BOOKED! No further reservations can be accepted.");
        }
    }

    private static void handleBookPackage() {
        ConsoleFormatter.printSubHeader("Book Travel Package (Anti-Overbooking Protected)");
        try {
            System.out.print("Enter Customer ID: ");
            int custId = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Enter Package ID: ");
            int pkgId = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Enter Travel Date (YYYY-MM-DD): ");
            String date = scanner.nextLine().trim();
            System.out.print("Enter Number of Travelers: ");
            int travelers = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Payment Method (UPI / Credit Card / Debit Card / Net Banking / Cash): ");
            String method = scanner.nextLine().trim();

            Booking booking = bookingService.processBooking(custId, pkgId, date, travelers, method);
            ConsoleFormatter.printSuccess("BOOKING CONFIRMED!");
            System.out.println("  Booking Reference ID : " + booking.getBookingId());
            System.out.println("  Customer Name        : " + booking.getCustomerName());
            System.out.println("  Destination          : " + booking.getDestination());
            System.out.println("  Travel Date          : " + booking.getTravelDate());
            System.out.println("  Travelers Headcount  : " + booking.getNumTravelers());
            System.out.println("  Total Invoice Amount : Rs. " + String.format("%,.2f", booking.getTotalAmount()));
            System.out.println("  Payment Status       : PAID (" + method + ")");

        } catch (CapacityExceededException e) {
            ConsoleFormatter.printError("[OVERBOOKING BLOCKED] " + e.getMessage());
        } catch (InvalidInputException e) {
            ConsoleFormatter.printError("[INVALID INPUT] " + e.getMessage());
        } catch (NumberFormatException e) {
            ConsoleFormatter.printError("Please enter valid numeric values for IDs and headcount.");
        } catch (SQLException e) {
            ConsoleFormatter.printError("Database Error: " + e.getMessage());
        }
    }

    private static void handleViewAllBookings() throws SQLException {
        ConsoleFormatter.printSubHeader("Master Bookings Log");
        List<Booking> list = bookingService.getAllBookings();
        if (list.isEmpty()) {
            ConsoleFormatter.printWarning("No bookings recorded yet.");
            return;
        }
        System.out.printf("%-5s | %-16s | %-26s | %-10s | %-6s | %-13s | %-9s%n",
                "ID", "Customer", "Destination", "TravelDate", "Guests", "Total Amount", "Status");
        ConsoleFormatter.printDivider();
        for (Booking b : list) {
            System.out.printf("%-5d | %-16s | %-26s | %-10s | %6d | Rs. %9.2f | %-9s%n",
                    b.getBookingId(), b.getCustomerName(), b.getDestination(),
                    b.getTravelDate(), b.getNumTravelers(), b.getTotalAmount(), b.getBookingStatus());
        }
    }

    private static void handleCancelBooking() {
        ConsoleFormatter.printSubHeader("Cancel Booking & Issue Refund");
        try {
            System.out.print("Enter Booking ID to Cancel: ");
            int bookingId = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Enter Cancellation Reason: ");
            String reason = scanner.nextLine().trim();

            boolean success = bookingService.cancelBooking(bookingId, reason);
            if (success) {
                ConsoleFormatter.printSuccess("Booking ID " + bookingId + " has been CANCELLED.");
                ConsoleFormatter.printInfo("Allocated seats have been released back to available package inventory.");
                ConsoleFormatter.printInfo("Processed 90% refund credit back to customer.");
            }
        } catch (BookingNotFoundException | InvalidInputException e) {
            ConsoleFormatter.printError(e.getMessage());
        } catch (Exception e) {
            ConsoleFormatter.printError("Failed to cancel booking: " + e.getMessage());
        }
    }

    private static void handleViewPayments() throws SQLException {
        ConsoleFormatter.printSubHeader("Payment Transactions Register");
        com.travel.dao.PaymentDAO dao = new com.travel.dao.PaymentDAO();
        List<Payment> list = dao.getAllPayments();
        if (list.isEmpty()) {
            ConsoleFormatter.printWarning("No payment records found.");
            return;
        }
        System.out.printf("%-5s | %-9s | %-11s | %-14s | %-12s | %-9s%n",
                "PayID", "BookingID", "Date", "Amount", "Method", "Status");
        ConsoleFormatter.printDivider();
        for (Payment p : list) {
            System.out.printf("%-5d | %-9d | %-11s | Rs. %10.2f | %-12s | %-9s%n",
                    p.getPaymentId(), p.getBookingId(), p.getPaymentDate(),
                    p.getAmount(), p.getPaymentMethod(), p.getPaymentStatus());
        }
    }

    private static void handleDestinationRevenueReport() throws SQLException {
        reportService.displayDestinationRevenueReport();
    }

    private static void handleRecentBookingsLog() throws SQLException {
        reportService.displayRecentBookingsSummary();
    }

    private static void handleRunPythonTrendAnalysis() {
        ConsoleFormatter.printHeader("Executing Python Tourism Trend Analytics Pipeline");
        ConsoleFormatter.printInfo("Launching Python data preprocessing & visualization engine...");

        try {
            String venvPython = "e:\\Assingment_Kishor\\.venv\\Scripts\\python.exe";
            String scriptPath = "e:\\Assingment_Kishor\\analytics\\tourism_trend_analysis.py";

            ProcessBuilder pb = new ProcessBuilder(venvPython, scriptPath);
            pb.redirectErrorStream(true);
            Process process = pb.start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println("  [Python] " + line);
            }

            int exitCode = process.waitFor();
            if (exitCode == 0) {
                ConsoleFormatter.printSuccess("Python Analytics completed successfully!");
                ConsoleFormatter.printInfo("Generated high-res visualizations saved in: 'visualizations/' folder.");
            } else {
                ConsoleFormatter.printError("Python process exited with code: " + exitCode);
            }
        } catch (Exception e) {
            ConsoleFormatter.printError("Failed to launch Python process: " + e.getMessage());
        }
    }
}
