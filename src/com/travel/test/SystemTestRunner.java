package com.travel.test;

import com.travel.exception.BookingNotFoundException;
import com.travel.exception.CapacityExceededException;
import com.travel.exception.InvalidInputException;
import com.travel.model.Booking;
import com.travel.model.Customer;
import com.travel.model.TravelPackage;
import com.travel.service.BookingService;
import com.travel.service.CustomerService;
import com.travel.service.PackageService;
import com.travel.service.ReportService;
import com.travel.util.ConsoleFormatter;

import java.sql.SQLException;
import java.util.List;

public class SystemTestRunner {
    private static int testsPassed = 0;
    private static int testsFailed = 0;

    public static void main(String[] args) {
        ConsoleFormatter.printHeader("AUTOMATED SYSTEM TEST SUITE - TRAVEL AGENCY SYSTEM");
        System.out.println("Student: Kishor K | RegNo: 732925ITR051 | Class: 25IT3A | Scenario 21\n");

        CustomerService customerService = new CustomerService();
        PackageService packageService = new PackageService();
        BookingService bookingService = new BookingService();
        ReportService reportService = new ReportService();

        // ---------------------------------------------------------------------
        // Test 1: Verify Customer Management
        // ---------------------------------------------------------------------
        runTest("TC-01: Customer Retrieval & Verification", () -> {
            List<Customer> customers = customerService.getAllCustomers();
            assertNotNull(customers, "Customer list should not be null");
            assertTrue(customers.size() >= 10, "Should have at least 10 seed customers");
        });

        runTest("TC-02: Invalid Email Validation", () -> {
            try {
                customerService.registerCustomer("Test User", "invalid-email-address", "9876543210", "Erode");
                fail("Expected InvalidInputException for bad email format");
            } catch (InvalidInputException e) {
                // Expected
            }
        });

        // ---------------------------------------------------------------------
        // Test 2: Package Inventory & Capacity
        // ---------------------------------------------------------------------
        runTest("TC-03: Travel Package Catalog Verification", () -> {
            List<TravelPackage> packages = packageService.getAllPackages();
            assertNotNull(packages, "Package list should not be null");
            assertTrue(packages.size() >= 8, "Should have at least 8 packages");
        });

        runTest("TC-04: Package Negative Price Prevention", () -> {
            try {
                packageService.addPackage("Faulty Tour", 5, -1000.0, 20, "Domestic", "Summer");
                fail("Expected InvalidInputException for negative price");
            } catch (InvalidInputException e) {
                // Expected
            }
        });

        // ---------------------------------------------------------------------
        // Test 3: Capacity Calculation & Anti-Overbooking Protection
        // ---------------------------------------------------------------------
        runTest("TC-05: Real-time Remaining Capacity Calculation", () -> {
            // Package 105: Dubai (Capacity 15)
            int avail = packageService.getAvailableSeats(105);
            assertTrue(avail >= 0 && avail <= 15, "Available seats must be within [0, 15]");
        });

        runTest("TC-06: Anti-Overbooking Guard (Exceeding Capacity Rejection)", () -> {
            int pkgId = 105;
            int remaining = packageService.getAvailableSeats(pkgId);
            // Attempt to book 50 seats (exceeding any available capacity)
            try {
                bookingService.processBooking(1, pkgId, "2026-12-25", remaining + 10, "UPI");
                fail("Expected CapacityExceededException when booking exceeds capacity!");
            } catch (CapacityExceededException e) {
                // Verified: Throws exception and rejects booking
            }
        });

        // ---------------------------------------------------------------------
        // Test 4: Valid Booking & Automatic Financial Calculation
        // ---------------------------------------------------------------------
        runTest("TC-07: Valid Booking Execution & Invoice Calculation", () -> {
            TravelPackage pkg = packageService.getPackageById(102); // Goa Tour
            int initialSeats = packageService.getAvailableSeats(102);
            if (initialSeats >= 2) {
                Booking b = bookingService.processBooking(2, 102, "2026-12-10", 2, "UPI");
                assertNotNull(b, "Booking should be created");
                assertEquals(pkg.getPricePerPerson() * 2, b.getTotalAmount(), 0.01, "Total price must equal headcount * unit price");
                assertEquals("CONFIRMED", b.getBookingStatus(), "Booking status must be CONFIRMED");
            }
        });

        // ---------------------------------------------------------------------
        // Test 5: Cancellation & Inventory Restoration
        // ---------------------------------------------------------------------
        runTest("TC-08: Booking Cancellation & Capacity Restoration", () -> {
            // Find an active booking
            List<Booking> bookings = bookingService.getAllBookings();
            Booking active = null;
            for (Booking b : bookings) {
                if ("CONFIRMED".equals(b.getBookingStatus())) {
                    active = b;
                    break;
                }
            }
            if (active != null) {
                int pkgId = active.getPackageId();
                int seatsBefore = packageService.getAvailableSeats(pkgId);
                boolean cancelled = bookingService.cancelBooking(active.getBookingId(), "Automated Test Cancellation");
                assertTrue(cancelled, "Cancellation should succeed");
                int seatsAfter = packageService.getAvailableSeats(pkgId);
                assertEquals(seatsBefore + active.getNumTravelers(), seatsAfter, "Remaining seats must increase after cancellation");
            }
        });

        // ---------------------------------------------------------------------
        // Test 6: Report Generation & Integrity
        // ---------------------------------------------------------------------
        runTest("TC-09: Destination Revenue & Occupancy Report Integrity", () -> {
            reportService.displayDestinationRevenueReport();
        });

        // ---------------------------------------------------------------------
        // Summary
        // ---------------------------------------------------------------------
        ConsoleFormatter.printHeader("TEST EXECUTION RESULTS");
        System.out.printf("Total Tests Run : %d%n", testsPassed + testsFailed);
        System.out.printf("Tests Passed    : %s%d%s%n", ConsoleFormatter.GREEN, testsPassed, ConsoleFormatter.RESET);
        System.out.printf("Tests Failed    : %s%d%s%n", (testsFailed > 0 ? ConsoleFormatter.RED : ConsoleFormatter.GREEN), testsFailed, ConsoleFormatter.RESET);
        
        if (testsFailed == 0) {
            ConsoleFormatter.printSuccess("ALL 9 AUTOMATED INTEGRATION TESTS PASSED WITH 100% SUCCESS RATE!");
        } else {
            ConsoleFormatter.printError("SOME TESTS FAILED!");
        }
    }

    private static void runTest(String testName, TestRunnable test) {
        try {
            test.run();
            System.out.printf("  [PASS] %s%n", testName);
            testsPassed++;
        } catch (Throwable t) {
            System.out.printf("  [FAIL] %s: %s%n", testName, t.getMessage());
            testsFailed++;
        }
    }

    @FunctionalInterface
    interface TestRunnable {
        void run() throws Throwable;
    }

    private static void assertTrue(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    private static void assertNotNull(Object obj, String message) {
        if (obj == null) throw new AssertionError(message);
    }

    private static void assertEquals(double expected, double actual, double delta, String message) {
        if (Math.abs(expected - actual) > delta) {
            throw new AssertionError(message + " (Expected: " + expected + ", Actual: " + actual + ")");
        }
    }

    private static void assertEquals(Object expected, Object actual, String message) {
        if (expected == null && actual == null) return;
        if (expected != null && expected.equals(actual)) return;
        throw new AssertionError(message + " (Expected: " + expected + ", Actual: " + actual + ")");
    }

    private static void fail(String message) {
        throw new AssertionError(message);
    }
}
