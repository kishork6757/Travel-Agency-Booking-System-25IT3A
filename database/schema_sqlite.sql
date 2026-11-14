-- =============================================================================
-- Travel Agency Booking and Tourism Trend Analysis System
-- SQLite Relational Database DDL Schema
-- Student: Kishor K (RegNo: 732925ITR051) | Class: 25IT3A
-- Course: 25ITT31 - Database Management Systems
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- 1. Table: customers
-- Stores profile details for individual travelers
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS cancellations;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS travel_packages;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL,
    city TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email CHECK (email LIKE '%_@__%.__%')
);

-- -----------------------------------------------------------------------------
-- 2. Table: travel_packages
-- Maintains catalog of tour destinations, pricing, and maximum guest capacities
-- -----------------------------------------------------------------------------
CREATE TABLE travel_packages (
    package_id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination TEXT NOT NULL,
    duration_days INTEGER NOT NULL CHECK (duration_days > 0),
    price_per_person REAL NOT NULL CHECK (price_per_person > 0),
    max_capacity INTEGER NOT NULL CHECK (max_capacity > 0),
    category TEXT NOT NULL CHECK (category IN ('Domestic', 'International', 'Adventure', 'Pilgrimage', 'Luxury')),
    season TEXT NOT NULL CHECK (season IN ('Summer', 'Monsoon', 'Autumn', 'Winter', 'All Season'))
);

-- -----------------------------------------------------------------------------
-- 3. Table: bookings
-- Records customer reservations and headcount with capacity checks
-- -----------------------------------------------------------------------------
CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    package_id INTEGER NOT NULL,
    booking_date TEXT NOT NULL,
    travel_date TEXT NOT NULL,
    num_travelers INTEGER NOT NULL CHECK (num_travelers > 0),
    total_amount REAL NOT NULL CHECK (total_amount >= 0),
    booking_status TEXT NOT NULL DEFAULT 'CONFIRMED' CHECK (booking_status IN ('CONFIRMED', 'CANCELLED', 'COMPLETED')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE RESTRICT,
    FOREIGN KEY (package_id) REFERENCES travel_packages(package_id) ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 4. Table: payments
-- Tracks payment transactions, invoice amounts, and settlement statuses
-- -----------------------------------------------------------------------------
CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL UNIQUE,
    payment_date TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    payment_method TEXT NOT NULL CHECK (payment_method IN ('UPI', 'Credit Card', 'Debit Card', 'Net Banking', 'Cash')),
    payment_status TEXT NOT NULL DEFAULT 'PAID' CHECK (payment_status IN ('PAID', 'PENDING', 'REFUNDED')),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 5. Table: cancellations
-- Records cancellation history, reason, and refunded finances
-- -----------------------------------------------------------------------------
CREATE TABLE cancellations (
    cancellation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL UNIQUE,
    cancellation_date TEXT NOT NULL,
    reason TEXT NOT NULL,
    refund_amount REAL NOT NULL DEFAULT 0.0 CHECK (refund_amount >= 0),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 6. Indexes for Performance & Query Optimization (Unit 3 Syllabus)
-- -----------------------------------------------------------------------------
CREATE INDEX idx_bookings_cust ON bookings(customer_id);
CREATE INDEX idx_bookings_pkg ON bookings(package_id);
CREATE INDEX idx_bookings_status ON bookings(booking_status);
CREATE INDEX idx_bookings_travel_date ON bookings(travel_date);
CREATE INDEX idx_payments_status ON payments(payment_status);

-- -----------------------------------------------------------------------------
-- 7. Database Views (Unit 2 Syllabus)
-- -----------------------------------------------------------------------------

-- View 1: Comprehensive Booking Summary View
DROP VIEW IF EXISTS v_booking_summary;
CREATE VIEW v_booking_summary AS
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

-- View 2: Destination Revenue & Occupancy Analysis View
DROP VIEW IF EXISTS v_destination_revenue;
CREATE VIEW v_destination_revenue AS
SELECT 
    p.package_id,
    p.destination,
    p.category,
    p.max_capacity,
    COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0) AS total_confirmed_guests,
    (p.max_capacity - COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0)) AS remaining_seats,
    ROUND((CAST(COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.num_travelers ELSE 0 END), 0) AS REAL) / p.max_capacity) * 100.0, 2) AS occupancy_rate_pct,
    COALESCE(SUM(CASE WHEN b.booking_status = 'CONFIRMED' THEN b.total_amount ELSE 0 END), 0.0) AS total_revenue
FROM travel_packages p
LEFT JOIN bookings b ON p.package_id = b.package_id
GROUP BY p.package_id, p.destination, p.category, p.max_capacity;

-- -----------------------------------------------------------------------------
-- 8. Advanced SQL Trigger: Overbooking Guard (Unit 2 Syllabus)
-- Prevents booking insertion if new travelers exceed available capacity
-- -----------------------------------------------------------------------------
DROP TRIGGER IF EXISTS trg_prevent_overbooking;
CREATE TRIGGER trg_prevent_overbooking
BEFORE INSERT ON bookings
WHEN (
    SELECT (p.max_capacity - COALESCE(SUM(b.num_travelers), 0))
    FROM travel_packages p
    LEFT JOIN bookings b ON p.package_id = b.package_id AND b.booking_status = 'CONFIRMED'
    WHERE p.package_id = NEW.package_id
    GROUP BY p.package_id
) < NEW.num_travelers
BEGIN
    SELECT RAISE(ABORT, 'CAPACITY_EXCEEDED: Cannot book package. Requested seats exceed available remaining capacity!');
END;
