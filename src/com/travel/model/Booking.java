package com.travel.model;

import java.io.Serializable;

public class Booking implements Serializable {
    private static final long serialVersionUID = 1L;

    private int bookingId;
    private int customerId;
    private int packageId;
    private String bookingDate;
    private String travelDate;
    private int numTravelers;
    private double totalAmount;
    private String bookingStatus; // CONFIRMED, CANCELLED, COMPLETED

    // Display fields from joins
    private String customerName;
    private String destination;

    public Booking() {}

    public Booking(int bookingId, int customerId, int packageId, String bookingDate, 
                   String travelDate, int numTravelers, double totalAmount, String bookingStatus) {
        this.bookingId = bookingId;
        this.customerId = customerId;
        this.packageId = packageId;
        this.bookingDate = bookingDate;
        this.travelDate = travelDate;
        this.numTravelers = numTravelers;
        this.totalAmount = totalAmount;
        this.bookingStatus = bookingStatus;
    }

    public int getBookingId() { return bookingId; }
    public void setBookingId(int bookingId) { this.bookingId = bookingId; }

    public int getCustomerId() { return customerId; }
    public void setCustomerId(int customerId) { this.customerId = customerId; }

    public int getPackageId() { return packageId; }
    public void setPackageId(int packageId) { this.packageId = packageId; }

    public String getBookingDate() { return bookingDate; }
    public void setBookingDate(String bookingDate) { this.bookingDate = bookingDate; }

    public String getTravelDate() { return travelDate; }
    public void setTravelDate(String travelDate) { this.travelDate = travelDate; }

    public int getNumTravelers() { return numTravelers; }
    public void setNumTravelers(int numTravelers) { this.numTravelers = numTravelers; }

    public double getTotalAmount() { return totalAmount; }
    public void setTotalAmount(double totalAmount) { this.totalAmount = totalAmount; }

    public String getBookingStatus() { return bookingStatus; }
    public void setBookingStatus(String bookingStatus) { this.bookingStatus = bookingStatus; }

    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }

    public String getDestination() { return destination; }
    public void setDestination(String destination) { this.destination = destination; }

    @Override
    public String toString() {
        return String.format("[%d] Cust: %-16s | Pkg: %-26s | Travel: %s | Guests: %2d | Total: Rs. %9.2f | Status: %s",
                bookingId, 
                (customerName != null ? customerName : "ID:" + customerId),
                (destination != null ? destination : "ID:" + packageId),
                travelDate, numTravelers, totalAmount, bookingStatus);
    }
}
