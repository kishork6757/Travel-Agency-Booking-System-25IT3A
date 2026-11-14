# Database Normalization Document
## Travel Agency Booking and Tourism Trend Analysis System
**Course Code & Title:** 25ITT31 - Database Management Systems (Unit 3: Normalization and Query Optimization)  
**Student:** Kishor K (RegNo: 732925ITR051)  
**Class:** 25IT3A  

---

## 1. Overview of Normalization

Normalization is the systematic process of organizing data in a relational database to minimize data redundancy, prevent insertion, update, and deletion anomalies, and guarantee data consistency.

---

## 2. Unnormalized Form (UNF)

In an unnormalized legacy spreadsheet or manual log, all booking, package, customer, and payment information might be lumped into a single bloated relation:

$$\text{AGENCY\_RECORD}(\text{customer\_id}, \text{name}, \text{email}, \text{phone}, \text{package\_id}, \text{destination}, \text{duration}, \text{price}, \text{capacity}, \text{booking\_id}, \text{booking\_date}, \text{travel\_date}, \text{num\_travelers}, \text{payment\_id}, \text{amount}, \text{payment\_status})$$

### Anomalies in UNF:
1. **Insertion Anomaly:** A new travel package cannot be created without registering a dummy customer booking.
2. **Deletion Anomaly:** If a customer cancels their booking, package information might be completely lost if no other customer is booked.
3. **Update Anomaly:** Updating a package's price requires modifying hundreds of redundant booking rows, risking inconsistent pricing records.

---

## 3. Step-by-Step Normalization Process

### Step 1: First Normal Form (1NF)
* **Definition:** A relation is in 1NF if and only if all attribute domains are atomic (indivisible) and there are no repeating groups or multi-valued attributes.
* **Transformation:**
  * Multi-valued contact numbers or multi-traveler arrays are decoupled.
  * A composite primary key is identified: `(customer_id, package_id, booking_id)`.
  * Every cell contains a single scalar value.
* **Status:** The schema meets **1NF**.

---

### Step 2: Second Normal Form (2NF)
* **Definition:** A relation is in 2NF if it is in 1NF and **no non-prime attribute is partially dependent on any proper subset of any candidate key**. (Elimination of Partial Dependencies).
* **Identification of Functional Dependencies (FDs):**
  * \(FD_1: \text{customer\_id} \rightarrow \text{name}, \text{email}, \text{phone}, \text{city}\)
  * \(FD_2: \text{package\_id} \rightarrow \text{destination}, \text{duration\_days}, \text{price\_per\_person}, \text{max\_capacity}, \text{category}, \text{season}\)
  * \(FD_3: \text{booking\_id} \rightarrow \text{customer\_id}, \text{package\_id}, \text{booking\_date}, \text{travel\_date}, \text{num\_travelers}, \text{total\_amount}, \text{booking\_status}\)
* **Problem in UNF:** Attributes like `name` and `email` depend solely on `customer_id`, not the entire composite key `(customer_id, package_id, booking_id)`.
* **Decomposition to 2NF:**
  * Decompose into dedicated relations:
    1. `CUSTOMERS` (Key: `customer_id`)
    2. `TRAVEL_PACKAGES` (Key: `package_id`)
    3. `BOOKINGS` (Key: `booking_id`)
* **Status:** All partial dependencies are eliminated; schema is in **2NF**.

---

### Step 3: Third Normal Form (3NF)
* **Definition:** A relation is in 3NF if it is in 2NF and **no non-prime attribute is transitively dependent on the primary key**. That is, for every non-trivial functional dependency \(X \rightarrow Y\), either:
  1. \(X\) is a super key, OR
  2. \(Y\) is a prime attribute.
* **Transitive Dependency Analysis:**
  * In `BOOKINGS`, if payment details and cancellation details are stored directly:
    $$\text{booking\_id} \rightarrow \text{payment\_id} \rightarrow \text{payment\_method}, \text{payment\_status}$$
    $$\text{booking\_id} \rightarrow \text{cancellation\_id} \rightarrow \text{reason}, \text{refund\_amount}$$
  * `payment_status` is transitively dependent on `booking_id` through `payment_id`.
  * `refund_amount` is transitively dependent on `booking_id` through `cancellation_id`.
* **Decomposition to 3NF:**
  * Extract payment entities into `PAYMENTS`:
    $$\text{payment\_id} \rightarrow \text{booking\_id}, \text{payment\_date}, \text{amount}, \text{payment\_method}, \text{payment\_status}$$
  * Extract cancellation entities into `CANCELLATIONS`:
    $$\text{cancellation\_id} \rightarrow \text{booking\_id}, \text{cancellation\_date}, \text{reason}, \text{refund\_amount}$$
* **Status:** All transitive dependencies eliminated; schema is in **3NF**.

---

### Step 4: Boyce-Codd Normal Form (BCNF)
* **Definition:** A relation is in BCNF if for every functional dependency \(X \rightarrow Y\), \(X\) is a **super key**.
* **Evaluation:**
  * In `CUSTOMERS`: `customer_id` is a super key; `email` is also an alternate candidate key.
  * In `TRAVEL_PACKAGES`: `package_id` is a super key.
  * In `BOOKINGS`: `booking_id` is the primary and super key.
  * In `PAYMENTS`: `payment_id` is the primary and super key.
  * In `CANCELLATIONS`: `cancellation_id` is the primary and super key.
* **Conclusion:** There are no overlapping candidate keys or dependencies where the determinant is not a super key. The database is strictly in **BCNF**.

---

## 4. Properties of the Final Decomposition
1. **Lossless Join Guarantee:** Re-joining tables on foreign keys (`bookings.customer_id = customers.customer_id`, etc.) reconstructs the original dataset without generating spurious tuples.
2. **Dependency Preservation:** All original functional dependencies \(FD_1, FD_2, FD_3, FD_4, FD_5\) are enforced locally within their respective tables.
3. **Storage Efficiency & Integrity:** Eliminates redundancy, optimizes memory caching, and ensures referential constraints are maintained natively by the database engine.
