-- =============================================================================
-- Travel Agency Booking and Tourism Trend Analysis System
-- Master Seed Dataset (Realistic Tourism Data for DBMS & Python Analytics)
-- Student: Kishor K (RegNo: 732925ITR051) | Class: 25IT3A
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Seed Customers
-- -----------------------------------------------------------------------------
INSERT INTO customers (customer_id, name, email, phone, city) VALUES
(1, 'Kishor Kumar', 'kishor.k@example.com', '9876543210', 'Erode'),
(2, 'Priya Dharshini', 'priya.d@example.com', '9845123456', 'Coimbatore'),
(3, 'Rajesh Kannan', 'rajesh.k@example.com', '9712345678', 'Chennai'),
(4, 'Sneha Murali', 'sneha.m@example.com', '9623456789', 'Bengaluru'),
(5, 'Arun Prasath', 'arun.p@example.com', '9534567890', 'Salem'),
(6, 'Deepa Balaji', 'deepa.b@example.com', '9445678901', 'Madurai'),
(7, 'Vigneshwaran S', 'vignesh.s@example.com', '9356789012', 'Tiruppur'),
(8, 'Kavitha Ramesh', 'kavitha.r@example.com', '9267890123', 'Trichy'),
(9, 'Siddharth Iyer', 'sid.iyer@example.com', '9178901234', 'Mumbai'),
(10, 'Ananya Nambiar', 'ananya.n@example.com', '9089012345', 'Kochi'),
(11, 'Manish Tiwari', 'manish.t@example.com', '8990123456', 'Delhi'),
(12, 'Pooja Hegde', 'pooja.h@example.com', '8801234567', 'Hyderabad');

-- -----------------------------------------------------------------------------
-- 2. Seed Travel Packages
-- -----------------------------------------------------------------------------
INSERT INTO travel_packages (package_id, destination, duration_days, price_per_person, max_capacity, category, season) VALUES
(101, 'Manali & Kasol Alpine Tour', 5, 14500.00, 25, 'Adventure', 'Summer'),
(102, 'Goa Sun & Sand Gateway', 4, 11000.00, 30, 'Domestic', 'Winter'),
(103, 'Kerala Backwaters & Munnar', 6, 18500.00, 20, 'Luxury', 'Monsoon'),
(104, 'Kashmir Paradise Odyssey', 7, 24000.00, 18, 'Domestic', 'Summer'),
(105, 'Dubai Desert & City Lights', 5, 48000.00, 15, 'International', 'Winter'),
(106, 'Varanasi & Ayodhya Heritage', 4, 9500.00, 28, 'Pilgrimage', 'Autumn'),
(107, 'Andaman Island Coral Explorer', 6, 29000.00, 16, 'Adventure', 'Winter'),
(108, 'Thailand Island Extravaganza', 5, 36000.00, 20, 'International', 'Winter');

-- -----------------------------------------------------------------------------
-- 3. Seed Bookings
-- Spanning January to December 2026 to give seasonal patterns
-- -----------------------------------------------------------------------------
INSERT INTO bookings (booking_id, customer_id, package_id, booking_date, travel_date, num_travelers, total_amount, booking_status) VALUES
-- January & February 2026 (Winter)
(201, 1, 102, '2026-01-05', '2026-01-20', 3, 33000.00, 'COMPLETED'),
(202, 2, 105, '2026-01-12', '2026-02-05', 2, 96000.00, 'COMPLETED'),
(203, 3, 107, '2026-01-18', '2026-02-14', 2, 58000.00, 'COMPLETED'),
(204, 4, 102, '2026-02-01', '2026-02-22', 4, 44000.00, 'COMPLETED'),
(205, 5, 108, '2026-02-10', '2026-03-01', 3, 108000.00, 'COMPLETED'),

-- March, April & May 2026 (Summer Spike)
(206, 6, 101, '2026-03-02', '2026-04-10', 4, 58000.00, 'COMPLETED'),
(207, 7, 104, '2026-03-15', '2026-04-20', 2, 48000.00, 'COMPLETED'),
(208, 8, 101, '2026-04-01', '2026-05-05', 5, 72500.00, 'COMPLETED'),
(209, 9, 104, '2026-04-10', '2026-05-15', 3, 72000.00, 'COMPLETED'),
(210, 10, 101, '2026-04-22', '2026-05-25', 2, 29000.00, 'COMPLETED'),
(211, 11, 106, '2026-05-02', '2026-05-28', 4, 38000.00, 'COMPLETED'),
(212, 12, 101, '2026-05-14', '2026-06-02', 3, 43500.00, 'CANCELLED'),

-- June, July & August 2026 (Monsoon)
(213, 1, 103, '2026-06-01', '2026-07-10', 2, 37000.00, 'COMPLETED'),
(214, 2, 103, '2026-06-18', '2026-07-25', 4, 74000.00, 'COMPLETED'),
(215, 3, 101, '2026-07-04', '2026-08-01', 2, 29000.00, 'CANCELLED'),
(216, 4, 103, '2026-07-20', '2026-08-15', 3, 55500.00, 'COMPLETED'),
(217, 5, 106, '2026-08-05', '2026-08-28', 5, 47500.00, 'COMPLETED'),

-- September, October & November 2026 (Autumn / Festival Season)
(218, 6, 106, '2026-09-01', '2026-09-20', 6, 57000.00, 'COMPLETED'),
(219, 7, 102, '2026-09-15', '2026-10-10', 3, 33000.00, 'CONFIRMED'),
(220, 8, 105, '2026-10-02', '2026-11-05', 2, 96000.00, 'CONFIRMED'),
(221, 9, 108, '2026-10-12', '2026-11-18', 4, 144000.00, 'CONFIRMED'),
(222, 10, 107, '2026-10-25', '2026-11-25', 3, 87000.00, 'CONFIRMED'),

-- December 2026 (Upcoming Peak Winter)
(223, 11, 102, '2026-11-01', '2026-12-15', 5, 55000.00, 'CONFIRMED'),
(224, 12, 105, '2026-11-05', '2026-12-20', 3, 144000.00, 'CONFIRMED'),
(225, 1, 104, '2026-11-10', '2026-12-24', 2, 48000.00, 'CONFIRMED'),
(226, 2, 102, '2026-11-12', '2026-12-28', 2, 22000.00, 'CONFIRMED'),
(227, 3, 107, '2026-11-13', '2026-12-30', 2, 58000.00, 'CANCELLED');

-- -----------------------------------------------------------------------------
-- 4. Seed Payments
-- -----------------------------------------------------------------------------
INSERT INTO payments (payment_id, booking_id, payment_date, amount, payment_method, payment_status) VALUES
(301, 201, '2026-01-05', 33000.00, 'UPI', 'PAID'),
(302, 202, '2026-01-12', 96000.00, 'Credit Card', 'PAID'),
(303, 203, '2026-01-18', 58000.00, 'Net Banking', 'PAID'),
(304, 204, '2026-02-01', 44000.00, 'UPI', 'PAID'),
(305, 205, '2026-02-10', 108000.00, 'Credit Card', 'PAID'),
(306, 206, '2026-03-02', 58000.00, 'Debit Card', 'PAID'),
(307, 207, '2026-03-15', 48000.00, 'UPI', 'PAID'),
(308, 208, '2026-04-01', 72500.00, 'Credit Card', 'PAID'),
(309, 209, '2026-04-10', 72000.00, 'Net Banking', 'PAID'),
(310, 210, '2026-04-22', 29000.00, 'UPI', 'PAID'),
(311, 211, '2026-05-02', 38000.00, 'Cash', 'PAID'),
(312, 212, '2026-05-14', 43500.00, 'UPI', 'REFUNDED'),
(313, 213, '2026-06-01', 37000.00, 'Credit Card', 'PAID'),
(314, 214, '2026-06-18', 74000.00, 'UPI', 'PAID'),
(315, 215, '2026-07-04', 29000.00, 'Debit Card', 'REFUNDED'),
(316, 216, '2026-07-20', 55500.00, 'Net Banking', 'PAID'),
(317, 217, '2026-08-05', 47500.00, 'UPI', 'PAID'),
(318, 218, '2026-09-01', 57000.00, 'Credit Card', 'PAID'),
(319, 219, '2026-09-15', 33000.00, 'UPI', 'PAID'),
(320, 220, '2026-10-02', 96000.00, 'Net Banking', 'PAID'),
(321, 221, '2026-10-12', 144000.00, 'Credit Card', 'PAID'),
(322, 222, '2026-10-25', 87000.00, 'UPI', 'PAID'),
(323, 223, '2026-11-01', 55000.00, 'Debit Card', 'PAID'),
(324, 224, '2026-11-05', 144000.00, 'Credit Card', 'PAID'),
(325, 225, '2026-11-10', 48000.00, 'UPI', 'PAID'),
(326, 226, '2026-11-12', 22000.00, 'UPI', 'PAID'),
(327, 227, '2026-11-13', 58000.00, 'Net Banking', 'REFUNDED');

-- -----------------------------------------------------------------------------
-- 5. Seed Cancellations
-- -----------------------------------------------------------------------------
INSERT INTO cancellations (cancellation_id, booking_id, cancellation_date, reason, refund_amount) VALUES
(401, 212, '2026-05-20', 'Sudden Family Emergency', 39150.00),
(402, 215, '2026-07-15', 'Flight Schedule Rescheduled by Airline', 26100.00),
(403, 227, '2026-11-14', 'Medical Unfitness / Doctor Advice', 52200.00);
