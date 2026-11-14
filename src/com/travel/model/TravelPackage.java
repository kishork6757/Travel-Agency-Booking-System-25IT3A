package com.travel.model;

import java.io.Serializable;

public class TravelPackage implements Serializable {
    private static final long serialVersionUID = 1L;

    private int packageId;
    private String destination;
    private int durationDays;
    private double pricePerPerson;
    private int maxCapacity;
    private String category;
    private String season;

    public TravelPackage() {}

    public TravelPackage(int packageId, String destination, int durationDays, 
                         double pricePerPerson, int maxCapacity, String category, String season) {
        this.packageId = packageId;
        this.destination = destination;
        this.durationDays = durationDays;
        this.pricePerPerson = pricePerPerson;
        this.maxCapacity = maxCapacity;
        this.category = category;
        this.season = season;
    }

    public int getPackageId() { return packageId; }
    public void setPackageId(int packageId) { this.packageId = packageId; }

    public String getDestination() { return destination; }
    public void setDestination(String destination) { this.destination = destination; }

    public int getDurationDays() { return durationDays; }
    public void setDurationDays(int durationDays) { this.durationDays = durationDays; }

    public double getPricePerPerson() { return pricePerPerson; }
    public void setPricePerPerson(double pricePerPerson) { this.pricePerPerson = pricePerPerson; }

    public int getMaxCapacity() { return maxCapacity; }
    public void setMaxCapacity(int maxCapacity) { this.maxCapacity = maxCapacity; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public String getSeason() { return season; }
    public void setSeason(String season) { this.season = season; }

    @Override
    public String toString() {
        return String.format("[%d] %-30s | %2d Days | Rs. %9.2f | Cap: %2d | %-13s | %-8s", 
                packageId, destination, durationDays, pricePerPerson, maxCapacity, category, season);
    }
}
