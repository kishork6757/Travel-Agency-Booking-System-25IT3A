# Software Testing and Quality Assurance Document
## Travel Agency Booking and Tourism Trend Analysis System
**Student:** Kishor K (RegNo: 732925ITR051)  
**Class:** 25IT3A  
**Course Code & Title:** 25ITT33 - Software Engineering (Unit 4: Software Testing)  

---

## 1. Testing Objectives & Strategy

Testing verifies that the **Travel Agency Booking and Tourism Trend Analysis System** fulfills all functional specifications, adheres to strict database integrity constraints, prevents overbooking, and executes data visualization accurately.

### 1.1 Levels of Testing
1. **Unit Testing:** Validates standalone classes and methods, such as calculating booking total cost, seat availability formula, and string validations.
2. **Integration Testing:** Tests interactions between the Service layer, DAO layer, and the relational database transactions (Commit / Rollback).
3. **System Testing:** End-to-end execution of the complete menu workflow, from package creation to booking, cancellation, and Python trend generation.
4. **Acceptance Testing:** Verification against the problem statement criteria in Scenario 21.

---

## 2. Test Design Techniques

### 2.1 Boundary Value Analysis (BVA) for Package Capacity
Given a Travel Package with a `max_capacity` of **20 travelers**:
* Currently booked: 18 travelers
* Remaining capacity: 2 seats
* **Test inputs:**
  * Just below boundary: 1 traveler \(\rightarrow\) **Accepted**
  * Exact boundary: 2 travelers \(\rightarrow\) **Accepted (Fills package to 100%)**
  * Just above boundary: 3 travelers \(\rightarrow\) **Rejected (`CapacityExceededException`)**
  * Negative / Zero input: 0 or -1 travelers \(\rightarrow\) **Rejected (`InvalidInputException`)**

### 2.2 Equivalence Class Partitioning (ECP)
* **Email Address:**
  * Valid Partition: `name@domain.com` \(\rightarrow\) Valid
  * Invalid Partition: `namedomain.com`, `@domain.com`, empty string \(\rightarrow\) Error
* **Payment Status:**
  * Valid Partition: `['PAID', 'PENDING', 'CANCELLED', 'REFUNDED']`
  * Invalid Partition: Any unrecognized string \(\rightarrow\) Constraint Error

---

## 3. Comprehensive Test Cases Execution Table

| Test ID | Test Scenario | Preconditions | Input Data | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Register new valid customer | System running, DB online | Name: `"Ananya Sharma"`, Email: `"ananya@gmail.com"`, Phone: `"9876543210"`, City: `"Chennai"` | Customer created with generated ID, status 201 | Customer created successfully with ID 101 | **PASS** |
| **TC-02** | Register customer with invalid email format | System running | Email: `"ananya_invalid_email"` | System catches format error, prompts re-entry | Caught regex mismatch, rejection prompted | **PASS** |
| **TC-03** | Create new travel package | Admin access | Destination: `"Goa Beach Holiday"`, Days: `4`, Price: `15000.00`, Capacity: `25` | Package saved with unique ID, available seats = 25 | Package saved with ID 201, seats = 25 | **PASS** |
| **TC-04** | Create package with negative price | Admin access | Price: `-500.00` | Rejection via Domain Check Constraint / Exception | Threw `InvalidInputException: Price must be positive` | **PASS** |
| **TC-05** | Book package within available capacity | Package 201 exists, 25 seats free | Package ID: `201`, Customer ID: `101`, Travelers: `4`, Date: `"2026-12-20"` | Booking confirmed, total = 60,000, remaining seats = 21 | Booking CONFIRMED, total calculated, seats = 21 | **PASS** |
| **TC-06** | Boundary Test: Book exact remaining capacity | Package has 2 seats left | Package ID: `201`, Travelers: `2` | Booking confirmed, remaining seats drops to 0 | Booking CONFIRMED, package now fully booked (0 seats) | **PASS** |
| **TC-07** | Boundary Test: Attempt overbooking (1 above boundary) | Package has 0 seats left | Package ID: `201`, Travelers: `1` | Throws `CapacityExceededException`, transaction rollback | Caught `CapacityExceededException: 0 seats remaining` | **PASS** |
| **TC-08** | Attempt overbooking with large party size | Package has 5 seats left | Package ID: `202`, Travelers: `8` | Booking rejected, clear error displayed to agent | Displayed: "Requested 8 seats exceeds available 5" | **PASS** |
| **TC-09** | Record payment for confirmed booking | Booking ID 301 is PENDING | Booking ID: `301`, Amount: `60000.00`, Method: `"UPI"` | Payment recorded, status updated to `PAID` | Payment ID created, booking marked `PAID` | **PASS** |
| **TC-10** | Cancel confirmed booking | Booking ID 301 is active | Booking ID: `301`, Reason: `"Medical Emergency"` | Booking status updated to `CANCELLED`, seats released | Status `CANCELLED`, 4 seats restored to package | **PASS** |
| **TC-11** | Cancel already cancelled booking | Booking ID 301 is CANCELLED | Booking ID: `301` | System warns: "Booking is already cancelled" | Threw warning, no duplicate cancellation recorded | **PASS** |
| **TC-12** | Query package revenue summary report | Bookings exist in DB | Trigger menu option 5 (Reports) | Tabular report shows gross revenue, confirmed seats | Displayed formatted table with accurate revenues | **PASS** |
| **TC-13** | Python DB data retrieval | Database populated | Run `tourism_trend_analysis.py` | Python connects, loads records into Pandas DataFrames | 100% records fetched, 0 connection errors | **PASS** |
| **TC-14** | Data Wrangling: Calculate Occupancy Rate | Bookings & Packages merged | Pandas merge on `package_id` | Occupancy rate derived: `(booked / capacity) * 100` | Correct percentages computed (0.0% to 100.0%) | **PASS** |
| **TC-15** | Generate and export charts | Python visualization run | Execute plotting routines | 6 high-res PNG charts saved in `visualizations/` | All 6 PNG files generated and saved to disk | **PASS** |

---

## 4. Test Conclusion & Sign-Off
- **Total Test Cases Executed:** 15
- **Passed:** 15
- **Failed:** 0
- **Defect Density:** 0.00 Defects/KLOC
- **Assessment:** The application is robust, enforces strict referential and capacity limits, handles exceptions gracefully, and satisfies all requirements specified in the project problem statement.
