# Software Requirements Specification (SRS)
## Travel Agency Booking and Tourism Trend Analysis System
**Academic Year:** 2026 - 2027 (ODD)  
**Institution:** Velalar College of Engineering and Technology, Erode - 12  
**Department:** Department of Information Technology  
**Course Code & Title:** 25ITT33 - Software Engineering / 25ITT31 - DBMS / 25ITT32 - Java / 25ITC31 - Foundations of Data Science  
**Class:** 25IT3A  
**Student Name:** Kishor K  
**Register Number:** 732925ITR051  
**Assigned Scenario:** Scenario 21 (Register No.: 21, 51, 81, 111)

---

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to define the functional, non-functional, interface, and performance requirements for the **Travel Agency Booking and Tourism Trend Analysis System**. This specification serves as a binding reference for system design, database development, object-oriented implementation in Java, and predictive/descriptive data analytics in Python.

### 1.2 Scope of the System
The system automates the core operational and analytical workflows of a modern tourism and travel agency. It provides:
- **Customer Management:** Registration and tracking of individual and corporate travelers.
- **Travel Package Management:** Configuration of tour packages, pricing, durations, destinations, and strictly enforced maximum capacities.
- **Booking & Reservation:** Real-time seat allocation, party size handling, date scheduling, and automated prevention of overbooking.
- **Cancellation & Refund Management:** Processing cancellations, updating status, and releasing seats back into available inventory.
- **Revenue & Financial Tracking:** Recording payment statuses (Paid, Pending, Refunded) and calculating gross and net revenue.
- **Tourism Trend Analysis & Business Intelligence:** Integration with Python (Pandas/Seaborn/Matplotlib) to discover seasonal demand spikes, popular tourist destinations, cancellation rates, and customer spending habits.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS:** Software Requirements Specification
- **DBMS:** Database Management System
- **JDBC:** Java Database Connectivity
- **EDA:** Exploratory Data Analysis
- **DDL / DML:** Data Definition Language / Data Manipulation Language
- **1NF / 2NF / 3NF / BCNF:** First, Second, Third, and Boyce-Codd Normal Forms
- **ACID:** Atomicity, Consistency, Isolation, Durability
- **COCOMO:** Constructive Cost Model

---

## 2. Overall Description

### 2.1 Product Perspective
The application operates as a 3-tier architecture:
1. **Presentation / Client Tier:** Menu-driven, interactive Java console application offering rich feedback, input validation, and formatted tabular reports.
2. **Business Logic & Persistence Tier:** Java Service and DAO (Data Access Object) layers enforcing business rules, capacity constraints, transactional integrity, and database operations.
3. **Data Storage & Analytics Tier:** Relational Database (SQLite / MySQL) storing operational records, coupled with a Python data science pipeline that extracts dataset snapshots to execute data wrangling and visualization routines.

### 2.2 Product Functions
- Maintain detailed customer records (ID, name, phone, email, address).
- Maintain travel package details (ID, destination, duration in days, price per traveler, maximum seating capacity).
- Real-time booking engine that checks live availability and rejects any booking exceeding remaining package capacity.
- Record booking timestamp, travel start date, payment status, and cancellation reasons.
- Generate operational reports (top destinations by booking volume, total package revenue, occupancy rates).
- Extract database data into Python DataFrames for statistical analysis and graphical visualization.

### 2.3 User Classes and Characteristics
- **Travel Agency Administrator / Manager:** Has complete administrative rights to create packages, view financial reports, inspect cancellation metrics, and trigger tourism trend analyses.
- **Booking Agent / Desk Staff:** Handles customer registration, creates and cancels bookings, collects payments, and checks seat availability.
- **Data Analyst / Tourism Strategist:** Uses the Python analytics engine to observe patterns, forecast seasonal demand, and recommend promotional package pricing.

### 2.4 Operating Environment
- **Operating System:** Windows 10/11, Linux, or macOS
- **Java Platform:** JDK 17 / JDK 21+
- **Database Engine:** SQLite 3 (self-contained zero-config) / MySQL Server 8.0+
- **Python Environment:** Python 3.10+ with NumPy, Pandas, Matplotlib, Seaborn

---

## 3. Specific Requirements

### 3.1 Functional Requirements (FR)

| Req ID | Requirement Title | Description |
| :--- | :--- | :--- |
| **FR-01** | Customer Profile Management | Maintain complete customer profiles including unique Customer ID, full name, phone number, and validated email address. |
| **FR-02** | Package Inventory Management | Create, view, update, and manage travel packages with destination details, duration in days, package price per head, and maximum traveler capacity. |
| **FR-03** | Dynamic Capacity Verification | Dynamically check the current sum of confirmed travelers for any package. Calculate `available_seats = max_capacity - total_booked_seats`. |
| **FR-04** | Overbooking Prevention | If requested traveler count exceeds available seats, immediately abort the transaction with a clear `CapacityExceededException` notification. |
| **FR-05** | Booking Creation & Traveler Allocation | Record booking date, chosen travel date, number of travelers, total price (`travelers * price_per_head`), and set default payment status (`PENDING` or `PAID`). |
| **FR-06** | Cancellation & Inventory Restoration | Allow booking cancellation with recorded cancellation date and reason. Instantly restore capacity for other travelers. |
| **FR-07** | Payment Status Recording | Track and update payment status across `PENDING`, `PAID`, `CANCELLED`, and `REFUNDED`. |
| **FR-08** | Operational Report Generation | Generate formatted reports on destination popularity, package capacity utilization, and total revenue accrued. |
| **FR-09** | Python Data Extraction & Preprocessing | Connect to the operational database from Python, preprocess raw tables (clean nulls, convert data types, derive features like `occupancy_rate` and `net_revenue`). |
| **FR-10** | Tourism Trend Visualization | Generate publication-quality visualizations representing monthly demand spikes, destination revenue contributions, traveler group size distribution, and cancellation trends. |

### 3.2 Non-Functional Requirements (NFR)

#### 3.2.1 Reliability & Data Integrity
- All transactional operations (booking creation, cancellations) must obey **ACID** properties.
- Relational foreign keys and check constraints guarantee referential and domain integrity.

#### 3.2.2 Usability
- Formatted tabular outputs with clear ASCII borders and colored state badges.
- Intuitive numeric menus with input validation preventing program crashes on invalid inputs.

#### 3.2.3 Performance & Scalability
- Sub-second execution for all database queries using indexed primary and foreign keys.
- Analytics script processes thousands of historical booking records in under 3 seconds.

#### 3.2.4 Maintainability
- Clean layered architecture separating Models, Data Access Objects (DAO), Service Layer, and UI.

---

## 4. Software Project Estimation (COCOMO & LOC)

### 4.1 Lines of Code (LOC) Estimation
- **Java Source Code (Core, DAO, Service, Models, Util):** ~1,200 LOC
- **Database Scripts (DDL, DML, Triggers, Views):** ~350 LOC
- **Python Analytics & Preprocessing Script:** ~300 LOC
- **Documentation (SRS, Design, Testing, Normalization):** ~850 LOC
- **Total Estimated Project Size:** **~2,700 Lines**

### 4.2 Basic COCOMO Estimation (Organic Mode)
Using the Boehm Basic COCOMO formula for an Organic software project:
- Size \(KLOC = 2.7\)
- Effort Equation: \(E = 2.4 \times (KLOC)^{1.05} = 2.4 \times (2.7)^{1.05} \approx 6.77 \text{ Person-Months}\)
- Development Time Equation: \(D = 2.5 \times (E)^{0.38} = 2.5 \times (6.77)^{0.38} \approx 5.16 \text{ Months}\)
- Recommended Team Size: \(P = E / D \approx 1.3 \approx 1 \text{ Developer (Kishor K)}\)

---

## 5. Acceptance Criteria
1. Full Java compilation with zero errors or warnings.
2. Complete test case execution covering positive, negative, and boundary condition paths.
3. 3NF normalized database schema populated with realistic test records.
4. Python scripts generating 6 high-resolution charts saved in `visualizations/`.
5. Comprehensive documentation ready for GitHub submission.
