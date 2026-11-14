package com.travel.model;

import java.io.Serializable;

public class Payment implements Serializable {
    private static final long serialVersionUID = 1L;

    private int paymentId;
    private int bookingId;
    private String paymentDate;
    private double amount;
    private String paymentMethod; // UPI, Credit Card, Debit Card, Net Banking, Cash
    private String paymentStatus; // PAID, PENDING, REFUNDED

    public Payment() {}

    public Payment(int paymentId, int bookingId, String paymentDate, double amount, 
                   String paymentMethod, String paymentStatus) {
        this.paymentId = paymentId;
        this.bookingId = bookingId;
        this.paymentDate = paymentDate;
        this.amount = amount;
        this.paymentMethod = paymentMethod;
        this.paymentStatus = paymentStatus;
    }

    public int getPaymentId() { return paymentId; }
    public void setPaymentId(int paymentId) { this.paymentId = paymentId; }

    public int getBookingId() { return bookingId; }
    public void setBookingId(int bookingId) { this.bookingId = bookingId; }

    public String getPaymentDate() { return paymentDate; }
    public void setPaymentDate(String paymentDate) { this.paymentDate = paymentDate; }

    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }

    public String getPaymentMethod() { return paymentMethod; }
    public void setPaymentMethod(String paymentMethod) { this.paymentMethod = paymentMethod; }

    public String getPaymentStatus() { return paymentStatus; }
    public void setPaymentStatus(String paymentStatus) { this.paymentStatus = paymentStatus; }

    @Override
    public String toString() {
        return String.format("[%d] Booking ID: %-5d | Date: %s | Rs. %9.2f | Method: %-12s | Status: %s",
                paymentId, bookingId, paymentDate, amount, paymentMethod, paymentStatus);
    }
}
