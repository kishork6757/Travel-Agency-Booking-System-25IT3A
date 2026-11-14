package com.travel.model;

import java.io.Serializable;

public class Cancellation implements Serializable {
    private static final long serialVersionUID = 1L;

    private int cancellationId;
    private int bookingId;
    private String cancellationDate;
    private String reason;
    private double refundAmount;

    public Cancellation() {}

    public Cancellation(int cancellationId, int bookingId, String cancellationDate, String reason, double refundAmount) {
        this.cancellationId = cancellationId;
        this.bookingId = bookingId;
        this.cancellationDate = cancellationDate;
        this.reason = reason;
        this.refundAmount = refundAmount;
    }

    public int getCancellationId() { return cancellationId; }
    public void setCancellationId(int cancellationId) { this.cancellationId = cancellationId; }

    public int getBookingId() { return bookingId; }
    public void setBookingId(int bookingId) { this.bookingId = bookingId; }

    public String getCancellationDate() { return cancellationDate; }
    public void setCancellationDate(String cancellationDate) { this.cancellationDate = cancellationDate; }

    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }

    public double getRefundAmount() { return refundAmount; }
    public void setRefundAmount(double refundAmount) { this.refundAmount = refundAmount; }

    @Override
    public String toString() {
        return String.format("[%d] Booking ID: %-5d | Date: %s | Refund: Rs. %9.2f | Reason: %s",
                cancellationId, bookingId, cancellationDate, refundAmount, reason);
    }
}
