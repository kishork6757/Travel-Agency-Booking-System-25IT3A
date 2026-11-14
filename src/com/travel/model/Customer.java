package com.travel.model;

import java.io.Serializable;

public class Customer implements Serializable {
    private static final long serialVersionUID = 1L;

    private int customerId;
    private String name;
    private String email;
    private String phone;
    private String city;

    public Customer() {}

    public Customer(int customerId, String name, String email, String phone, String city) {
        this.customerId = customerId;
        this.name = name;
        this.email = email;
        this.phone = phone;
        this.city = city;
    }

    public int getCustomerId() { return customerId; }
    public void setCustomerId(int customerId) { this.customerId = customerId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public String getCity() { return city; }
    public void setCity(String city) { this.city = city; }

    @Override
    public String toString() {
        return String.format("[%d] %-18s | %-22s | %-12s | %-12s", 
                customerId, name, email, phone, city);
    }
}
