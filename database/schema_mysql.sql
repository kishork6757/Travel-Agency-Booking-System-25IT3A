-- =============================================================================
-- Travel Agency Booking and Tourism Trend Analysis System
-- MySQL Relational Database DDL Schema
-- Student: Kishor K (RegNo: 732925ITR051) | Class: 25IT3A
-- Course: 25ITT31 - Database Management Systems
-- =============================================================================

CREATE DATABASE IF NOT EXISTS travel_agency_db;
USE travel_agency_db;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS cancellations;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS travel_packages;
DROP TABLE IF EXISTS customers;
SET FOREIGN_KEY_CHECKS = 1;

-- -----------------------------------------------------------------------------
-- 1. Table: customers
-- -----------------------------------------------------------------------------
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    city VARCHAR(80) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email_fmt CHECK (email LIKE '%_@__%.__%')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 2. Table: travel_packages
-- -----------------------------------------------------------------------------
CREATE TABLE travel_packages (
    package_id INT AUTO_INCREMENT PRIMARY KEY,
    destination VARCHAR(120) NOT NULL,
    duration_days INT NOT NULL CHECK (duration_days > 0),
    price_per_person DECIMAL(10,2) NOT NULL CHECK (price_per_person > 0),
    max_capacity INT NOT NULL CHECK (max_capacity > 0),
    category ENUM('Domestic', 'International', 'Adventure', 'Pilgrimage', 'Luxury') NOT NULL,
    season ENUM('Summer', 'Monsoon', 'Autumn', 'Winter', 'All Season') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 3. Table: bookings
-- -----------------------------------------------------------------------------
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    package_id INT NOT NULL,
    booking_date DATE NOT NULL,
    travel_date DATE NOT NULL,
    num_travelers INT NOT NULL CHECK (num_travelers > 0),
    total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),
    booking_status ENUM('CONFIRMED', 'CANCELLED', 'COMPLETED') DEFAULT 'CONFIRMED',
    CONSTRAINT fk_bookings_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    CONSTRAINT fk_bookings_package FOREIGN KEY (package_id) REFERENCES travel_packages(package_id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 4. Table: payments
-- -----------------------------------------------------------------------------
CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL UNIQUE,
    payment_date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    payment_method ENUM('UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'Cash') NOT NULL,
    payment_status ENUM('PAID', 'PENDING', 'REFUNDED') DEFAULT 'PAID',
    CONSTRAINT fk_payments_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 5. Table: cancellations
-- -----------------------------------------------------------------------------
CREATE TABLE cancellations (
    cancellation_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL UNIQUE,
    cancellation_date DATE NOT NULL,
    reason VARCHAR(255) NOT NULL,
    refund_amount DECIMAL(12,2) NOT NULL DEFAULT 0.0 CHECK (refund_amount >= 0),
    CONSTRAINT fk_cancellations_booking FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------------------------------
-- 6. Performance Indexes
-- -----------------------------------------------------------------------------
CREATE INDEX idx_bookings_cust ON bookings(customer_id);
CREATE INDEX idx_bookings_pkg ON bookings(package_id);
CREATE INDEX idx_bookings_status ON bookings(booking_status);
CREATE INDEX idx_bookings_travel_date ON bookings(travel_date);

-- -----------------------------------------------------------------------------
-- 7. Database Views
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_booking_summary AS
SELECT 
    b.booking_id,
    c.name AS customer_name,
    c.phone AS customer_phone,
    p.destination,
    p.category,
    b.num_travelers,
    b.travel_date,
    b.total_amount,
    b.booking_status,
    COALESCE(pay.payment_status, 'UNPAID') AS payment_status
FROM bookings b
JOIN customers c ON b.customer_id = c.customer_id
JOIN travel_packages p ON b.package_id = p.package_id
LEFT JOIN payments pay ON b.booking_id = pay.booking_id;

CREATE OR REPLACE VIEW v_destination_revenue AS
SELECT 
    p.package_id,
    p.destination,
    p.category,
    p.max_capacity,
    COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0) AS total_confirmed_guests,
    (p.max_capacity - COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0)) AS remaining_seats,
    ROUND((COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0) / p.max_capacity) * 100.0, 2) AS occupancy_rate_pct,
    COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.total_amount ELSE 0 END), 0.0) AS total_revenue
FROM travel_packages p
LEFT JOIN bookings b ON p.package_id = b.package_id
GROUP BY p.package_id, p.destination, p.category, p.max_capacity;

-- -----------------------------------------------------------------------------
-- 8. Advanced Stored Procedure: BookPackageWithCapacityGuard
-- -----------------------------------------------------------------------------
DELIMITER //
CREATE PROCEDURE BookPackageWithCapacityGuard(
    IN p_customer_id INT,
    IN p_package_id INT,
    IN p_travel_date DATE,
    IN p_num_travelers INT,
    IN p_payment_method VARCHAR(30),
    OUT p_status_msg VARCHAR(255),
    OUT p_new_booking_id INT
)
BEGIN
    DECLARE v_capacity INT DEFAULT 0;
    DECLARE v_booked INT DEFAULT 0;
    DECLARE v_price DECIMAL(10,2) DEFAULT 0.0;
    DECLARE v_total DECIMAL(12,2) DEFAULT 0.0;
    
    START TRANSACTION;
    
    -- Lock package record for concurrency protection
    SELECT max_capacity, price_per_person INTO v_capacity, v_price 
    FROM travel_packages WHERE package_id = p_package_id FOR UPDATE;
    
    SELECT COALESCE(SUM(num_travelers), 0) INTO v_booked 
    FROM bookings WHERE package_id = p_package_id AND booking_status = 'CONFIRMED';
    
    IF (v_capacity - v_booked) < p_num_travelers THEN
        ROLLBACK;
        SET p_status_msg = CONCAT('REJECTED: Only ', (v_capacity - v_booked), ' seats remaining.');
        SET p_new_booking_id = -1;
    ELSE
        SET v_total = v_price * p_num_travelers;
        INSERT INTO bookings (customer_id, package_id, booking_date, travel_date, num_travelers, total_amount, booking_status)
        VALUES (p_customer_id, p_package_id, CURDATE(), p_travel_date, p_num_travelers, v_total, 'CONFIRMED');
        
        SET p_new_booking_id = LAST_INSERT_ID();
        
        INSERT INTO payments (booking_id, payment_date, amount, payment_method, payment_status)
        VALUES (p_new_booking_id, CURDATE(), v_total, p_payment_method, 'PAID');
        
        COMMIT;
        SET p_status_msg = 'SUCCESS: Booking and Payment processed successfully.';
    END IF;
END //
DELIMITER ;
