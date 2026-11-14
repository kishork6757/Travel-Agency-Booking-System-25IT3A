package com.travel.service;

import com.travel.dao.BookingDAO;
import com.travel.dao.CustomerDAO;
import com.travel.dao.PackageDAO;
import com.travel.dao.PaymentDAO;
import com.travel.exception.BookingNotFoundException;
import com.travel.exception.CapacityExceededException;
import com.travel.exception.InvalidInputException;
import com.travel.model.Booking;
import com.travel.model.Customer;
import com.travel.model.Payment;
import com.travel.model.TravelPackage;

import java.sql.SQLException;
import java.time.LocalDate;
import java.util.List;

public class BookingService {
    private final BookingDAO bookingDAO;
    private final PackageDAO packageDAO;
    private final CustomerDAO customerDAO;
    private final PaymentDAO paymentDAO;

    public BookingService() {
        this.bookingDAO = new BookingDAO();
        this.packageDAO = new PackageDAO();
        this.customerDAO = new CustomerDAO();
        this.paymentDAO = new PaymentDAO();
    }

    /**
     * Creates a new travel booking with strict capacity verification and anti-overbooking enforcement.
     */
    public Booking processBooking(int customerId, int packageId, String travelDate, 
                                  int numTravelers, String paymentMethod)
            throws InvalidInputException, CapacityExceededException, SQLException {
        
        // 1. Validate inputs
        if (numTravelers <= 0) {
            throw new InvalidInputException("Number of travelers must be at least 1.");
        }
        if (travelDate == null || travelDate.trim().isEmpty()) {
            throw new InvalidInputException("Travel date cannot be empty.");
        }

        // 2. Verify Customer Exists
        Customer customer = customerDAO.getCustomerById(customerId);
        if (customer == null) {
            throw new InvalidInputException("Customer with ID " + customerId + " not found.");
        }

        // 3. Verify Package Exists
        TravelPackage pkg = packageDAO.getPackageById(packageId);
        if (pkg == null) {
            throw new InvalidInputException("Travel Package with ID " + packageId + " not found.");
        }

        // 4. CRITICAL: Capacity Check
        int remainingCapacity = packageDAO.getRemainingCapacity(packageId);
        if (numTravelers > remainingCapacity) {
            throw new CapacityExceededException(String.format(
                "Booking Rejected: Requested %d seats, but only %d seats are available for '%s' (Capacity: %d).",
                numTravelers, remainingCapacity, pkg.getDestination(), pkg.getMaxCapacity()
            ));
        }

        // 5. Calculate Total Price
        double totalAmount = pkg.getPricePerPerson() * numTravelers;
        String bookingDate = LocalDate.now().toString();

        // 6. Persist Booking
        Booking booking = new Booking(0, customerId, packageId, bookingDate, travelDate, 
                                      numTravelers, totalAmount, "CONFIRMED");
        boolean created = bookingDAO.createBooking(booking);

        if (created) {
            booking.setCustomerName(customer.getName());
            booking.setDestination(pkg.getDestination());

            // 7. Record Payment
            Payment payment = new Payment(0, booking.getBookingId(), bookingDate, totalAmount, 
                                          paymentMethod, "PAID");
            paymentDAO.addPayment(payment);
            return booking;
        } else {
            throw new SQLException("Failed to record booking in database.");
        }
    }

    /**
     * Cancels an existing booking, records reason, issues refund, and restores package capacity.
     */
    public boolean cancelBooking(int bookingId, String reason)
            throws BookingNotFoundException, InvalidInputException, SQLException {
        
        Booking booking = bookingDAO.getBookingById(bookingId);
        if (booking == null) {
            throw new BookingNotFoundException("Booking with ID " + bookingId + " not found.");
        }

        if ("CANCELLED".equalsIgnoreCase(booking.getBookingStatus())) {
            throw new InvalidInputException("Booking ID " + bookingId + " is already CANCELLED.");
        }

        if (reason == null || reason.trim().isEmpty()) {
            reason = "Customer Request / Schedule Change";
        }

        // Calculate 90% refund policy (10% standard cancellation fee)
        double refundAmount = Math.round(booking.getTotalAmount() * 0.90 * 100.0) / 100.0;

        return bookingDAO.processCancellation(bookingId, reason.trim(), refundAmount);
    }

    public List<Booking> getAllBookings() throws SQLException {
        return bookingDAO.getAllBookings();
    }

    public Booking getBookingById(int bookingId) throws SQLException {
        return bookingDAO.getBookingById(bookingId);
    }
}
