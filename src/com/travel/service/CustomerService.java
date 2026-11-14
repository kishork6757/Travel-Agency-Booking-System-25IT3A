package com.travel.service;

import com.travel.dao.CustomerDAO;
import com.travel.exception.InvalidInputException;
import com.travel.model.Customer;
import java.sql.SQLException;
import java.util.List;

public class CustomerService {
    private final CustomerDAO customerDAO;

    public CustomerService() {
        this.customerDAO = new CustomerDAO();
    }

    public boolean registerCustomer(String name, String email, String phone, String city) 
            throws InvalidInputException, SQLException {
        if (name == null || name.trim().isEmpty()) {
            throw new InvalidInputException("Customer name cannot be empty.");
        }
        if (email == null || !email.matches("^[A-Za-z0-9+_.-]+@(.+)$")) {
            throw new InvalidInputException("Invalid email format: " + email);
        }
        if (phone == null || phone.trim().length() < 10) {
            throw new InvalidInputException("Phone number must contain at least 10 digits.");
        }
        if (city == null || city.trim().isEmpty()) {
            throw new InvalidInputException("City cannot be empty.");
        }

        Customer customer = new Customer(0, name.trim(), email.trim(), phone.trim(), city.trim());
        return customerDAO.addCustomer(customer);
    }

    public List<Customer> getAllCustomers() throws SQLException {
        return customerDAO.getAllCustomers();
    }

    public Customer getCustomerById(int customerId) throws SQLException {
        return customerDAO.getCustomerById(customerId);
    }
}
