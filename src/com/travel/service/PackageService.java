package com.travel.service;

import com.travel.dao.PackageDAO;
import com.travel.exception.InvalidInputException;
import com.travel.model.TravelPackage;
import java.sql.SQLException;
import java.util.List;

public class PackageService {
    private final PackageDAO packageDAO;

    public PackageService() {
        this.packageDAO = new PackageDAO();
    }

    public boolean addPackage(String destination, int durationDays, double pricePerPerson, 
                              int maxCapacity, String category, String season) 
            throws InvalidInputException, SQLException {
        if (destination == null || destination.trim().isEmpty()) {
            throw new InvalidInputException("Destination cannot be empty.");
        }
        if (durationDays <= 0) {
            throw new InvalidInputException("Duration must be at least 1 day.");
        }
        if (pricePerPerson <= 0) {
            throw new InvalidInputException("Price per person must be greater than zero.");
        }
        if (maxCapacity <= 0) {
            throw new InvalidInputException("Maximum capacity must be at least 1 seat.");
        }

        TravelPackage pkg = new TravelPackage(0, destination.trim(), durationDays, 
                                              pricePerPerson, maxCapacity, category, season);
        return packageDAO.addPackage(pkg);
    }

    public List<TravelPackage> getAllPackages() throws SQLException {
        return packageDAO.getAllPackages();
    }

    public TravelPackage getPackageById(int packageId) throws SQLException {
        return packageDAO.getPackageById(packageId);
    }

    public int getAvailableSeats(int packageId) throws SQLException {
        return packageDAO.getRemainingCapacity(packageId);
    }
}
