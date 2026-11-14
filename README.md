# Travel Agency Booking and Tourism Trend Analysis System
### Integrated Academic Project-Based Assessment (ODD Semester 2026 - 2027)
**Department of Information Technology**  
**Velalar College of Engineering and Technology, Erode - 12**

---

## 📌 Student Details
* **Student Name:** Kishor K
* **Register Number:** 732925ITR051
* **Class & Section:** 25IT3A
* **Assigned Scenario:** **Scenario 21: Travel Agency Booking and Tourism Trend Analysis System** *(Register Nos: 21, 51, 81, 111)*

---

## 📖 Project Overview

The **Travel Agency Booking and Tourism Trend Analysis System** is an end-to-end software solution developed to automate travel desk operations, enforce strict inventory control, prevent overbooking, and unlock strategic business intelligence from historical tourism records.

Manual record-keeping in tourism operations commonly suffers from double-booking, overbooking beyond coach/flight limits, sluggish revenue reporting, and an inability to detect seasonal spikes. This project resolves these issues through a high-performance 3-tier architecture:
1. **Interactive Object-Oriented Java CLI Engine:** Enforces business logic, customer profile handling, traveler headcount verification, and real-time anti-overbooking safeguards.
2. **Relational Database Management System (3NF Normalized):** Robust schema in SQLite and MySQL with atomic transactions, referential integrity constraints, and automated database views.
3. **Python Tourism Analytics & Visualization Dashboard:** Preprocesses operational data using NumPy and Pandas to discover seasonal patterns, destination popularity, and traveler group behaviors through high-resolution Seaborn and Matplotlib visualizations.

---

## 🛠️ Technology Stack

| Domain | Technologies & Libraries |
| :--- | :--- |
| **Programming Language** | Java (JDK 17 / 21+) |
| **Object-Oriented Design** | Encapsulation, Inheritance, Interfaces, Custom Exceptions, Generics, Collections Framework, Streams API |
| **Persistence / RDBMS** | SQLite 3 (Default zero-config embedded) / MySQL 8.0+ |
| **Database Connectivity** | Standard JDBC (`java.sql.*`), PreparedStatements, Transactions (Commit/Rollback) |
| **Data Analytics** | Python 3.10+, NumPy, Pandas |
| **Data Visualization** | Matplotlib, Seaborn, Jupyter Notebook (`.ipynb`) |
| **Software Engineering** | Software Requirements Specification (SRS), UML Use Case, Class, Sequence Diagrams, Testing Matrix |

---

## 📂 Project Repository Structure

```text
Assingment_Kishor/
├── docs/                                # Software Engineering Deliverables (25ITT33)
│   ├── SRS.md                           # Software Requirements Specification (COCOMO, LOC, Requirements)
│   ├── DESIGN.md                        # Architecture, UML Use Case, Class & Sequence Diagrams (Mermaid)
│   └── TESTING.md                       # Test Strategy, BVA, ECP, and 15 Executed Test Cases Table
├── database/                            # Database Management Systems Deliverables (25ITT31)
│   ├── ER_DIAGRAM.md                    # Entity-Relationship Diagram and Relational Model Spec
│   ├── NORMALIZATION.md                 # 1NF, 2NF, 3NF, BCNF Step-by-Step Derivation
│   ├── schema_sqlite.sql                # SQLite DDL Schema (Tables, Views, Triggers, Indexes)
│   ├── schema_mysql.sql                 # MySQL DDL Schema (Tables, Views, Stored Procedures)
│   ├── seed_data.sql                    # Realistic Seed Records (12 Customers, 8 Packages, 27 Bookings)
│   └── travel_agency.db                 # Active SQLite Database File
├── src/com/travel/                      # Java Source Code (25ITT32)
│   ├── model/                           # Domain Entities (Customer, TravelPackage, Booking, Payment, Cancellation)
│   ├── dao/                             # Data Access Objects (DBConnection, CustomerDAO, PackageDAO, BookingDAO, PaymentDAO, ReportDAO)
│   ├── service/                         # Business Logic & Anti-Overbooking Engine (BookingService, CustomerService, PackageService, ReportService)
│   ├── exception/                       # Custom Exceptions (CapacityExceededException, BookingNotFoundException, InvalidInputException)
│   ├── util/                            # Console Table Formatter & DB Auto-Initializer
│   └── Main.java                        # Interactive Menu-Driven Console Application Entrypoint
├── analytics/                           # Foundations of Data Science (25ITC31)
│   ├── requirements.txt                 # Python Dependencies
│   ├── tourism_trend_analysis.py        # Automated Data Preprocessing & Plotting Script
│   └── tourism_trend_analysis.ipynb     # Interactive Jupyter Notebook with Narrative Explanations
├── visualizations/                      # High-Resolution Exported Analytics Charts
│   ├── 01_destination_popularity.png    # Horizontal Bar Chart of Destination Headcounts
│   ├── 02_monthly_booking_trends.png    # Seasonal Monthly Demand Curve
│   ├── 03_revenue_by_category.png       # Donut Chart of Revenue Share
│   ├── 04_booking_status_distribution.png # Bar Chart of Booking Outcomes (Confirmed vs Cancelled)
│   ├── 05_traveler_group_size_distribution.png # Histogram & KDE of Party Sizes
│   └── 06_package_occupancy_heatmap.png # Correlation Heatmap of Package Metrics
├── lib/                                 # Runtime Dependencies
│   ├── sqlite-jdbc.jar                  # SQLite JDBC Driver
│   ├── slf4j-api.jar                    # Logging API
│   └── slf4j-simple.jar                 # Logging Implementation
├── sample_outputs/                      # Verified Execution Logs
│   └── execution_log.txt                # Sample CLI Run & Overbooking Block Proof
├── run_java.bat                         # 1-Click Windows Batch Script to Compile & Run Java App
├── run_python.bat                       # 1-Click Windows Batch Script to Run Python Analytics
└── README.md                            # Master Project Documentation
```

---

## ⚙️ Setup and Execution Instructions

### 1. Prerequisites
Ensure you have the following installed on your workstation:
* **Java Development Kit (JDK 17 or higher):** Run `javac -version` and `java -version`
* **Python (Version 3.10 or higher):** Run `python --version`
* **Git:** For cloning and GitHub submission

---

### 2. Running the Java Application

#### Option A: 1-Click Batch Execution (Windows)
Double-click `run_java.bat` in the project root folder.

#### Option B: Command Line (PowerShell / Terminal)
```powershell
# 1. Navigate to the project directory
cd e:\Assingment_Kishor

# 2. Compile Java source files into the bin directory
javac -cp "lib/*" -d bin src/com/travel/model/*.java src/com/travel/exception/*.java src/com/travel/util/*.java src/com/travel/dao/*.java src/com/travel/service/*.java src/com/travel/Main.java

# 3. Launch the interactive application
java -cp "bin;lib/*" com.travel.Main
```

---

### 3. Running the Python Analytics & Generating Visualizations

#### Option A: 1-Click Batch Execution (Windows)
Double-click `run_python.bat` in the project root folder.

#### Option B: Command Line
```powershell
# 1. Install required Python packages (if not already installed)
pip install -r analytics/requirements.txt

# 2. Execute the analytics pipeline
python analytics/tourism_trend_analysis.py
```
*Generated plots will be automatically refreshed and saved to the `visualizations/` folder.*

---

### 4. Running the Jupyter Notebook
```powershell
jupyter notebook analytics/tourism_trend_analysis.ipynb
```

---

### 5. Database Setup (Optional for MySQL)
The project comes pre-configured with a live SQLite database (`database/travel_agency.db`) requiring **zero configuration**.

If you wish to deploy on **MySQL Server / XAMPP**:
1. Open MySQL Workbench or phpMyAdmin.
2. Execute `database/schema_mysql.sql` to generate tables, views, and stored procedures.
3. Execute `database/seed_data.sql` to populate initial records.

---

## 🛡️ Anti-Overbooking Protection: How It Works

The system enforces capacity limits at two distinct layers:
1. **Application Service Layer (`BookingService.java`):**
   ```java
   int remainingCapacity = packageDAO.getRemainingCapacity(packageId);
   if (numTravelers > remainingCapacity) {
       throw new CapacityExceededException(String.format(
           "Booking Rejected: Requested %d seats, but only %d seats are available for '%s' (Capacity: %d).",
           numTravelers, remainingCapacity, pkg.getDestination(), pkg.getMaxCapacity()
       ));
   }
   ```
2. **Database Engine Layer (`schema_sqlite.sql`):**
   An automated SQL Trigger (`trg_prevent_overbooking`) halts and aborts any `INSERT` on `bookings` if the sum of confirmed travelers would exceed `max_capacity`.

---

## 📊 Visualizations Gallery

| Chart Preview | Analysis Description |
| :--- | :--- |
| **`01_destination_popularity.png`** | Ranks tourist destinations by confirmed traveler headcount to identify high-demand locations (e.g. Goa, Dubai). |
| **`02_monthly_booking_trends.png`** | Visualizes seasonal tourist spikes across summer vacation (April–May) and winter holidays (December–January). |
| **`03_revenue_by_category.png`** | Donut chart displaying revenue contributions across International, Luxury, Domestic, Adventure, and Pilgrimage packages. |
| **`04_booking_status_distribution.png`** | Demonstrates operational health by analyzing the ratio of Confirmed, Completed, and Cancelled bookings. |
| **`05_traveler_group_size_distribution.png`** | Histogram and KDE curve illustrating party size distributions (identifying couple vs. family travel segments). |
| **`06_package_occupancy_heatmap.png`** | Correlation matrix examining the relationship between package duration, unit price, capacity, and gross revenue. |

---

## 🧪 Testing Summary

* **Testing Strategy:** Black-Box (Equivalence Partitioning, Boundary Value Analysis), White-Box Path Coverage, and Integration Testing.
* **Total Test Cases Executed:** 15
* **Results:** 15 Passed / 0 Failed (100% Pass Rate).
* *Refer to [`docs/TESTING.md`](docs/TESTING.md) for the full test cases specification table.*

---

## 📜 Academic Integrity and Certification
I hereby certify that this project represents my original work developed for the **Project-Based Assessment Activity** in the Department of Information Technology at **Velalar College of Engineering and Technology**.

* **Kishor K** (Register No: 732925ITR051)  
* Class: 25IT3A
