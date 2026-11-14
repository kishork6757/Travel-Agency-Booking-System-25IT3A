# System Design and Architecture Document
## Travel Agency Booking and Tourism Trend Analysis System
**Student:** Kishor K (RegNo: 732925ITR051)  
**Class:** 25IT3A  
**Institution:** Velalar College of Engineering and Technology, Erode - 12  
**Department:** Information Technology  

---

## 1. System Architecture

The system utilizes a 3-Tier Layered Architecture engineered for separation of concerns, high cohesion, low coupling, and data consistency.

```mermaid
graph TD
    subgraph "Tier 1: Presentation & User Interface Layer"
        CLI["Java Console CLI Engine<br/>(Interactive Menus, Table Formatter, ANSI Badges)"]
        Dashboard["Python Visualization Dashboard<br/>(Seaborn / Matplotlib Charts)"]
    end

    subgraph "Tier 2: Business Logic & Service Layer"
        CS["CustomerService"]
        PS["PackageService"]
        BS["BookingService<br/>(Capacity Validation & Anti-Overbooking Engine)"]
        RS["ReportService"]
        PyPipeline["Python Data Pipeline<br/>(NumPy Wrangling, Pandas Aggregations)"]
    end

    subgraph "Tier 3: Data Access & Persistence Layer"
        DAO["DAO Layer<br/>(CustomerDAO, PackageDAO, BookingDAO, PaymentDAO)"]
        DBDriver["JDBC Connection Pool / Driver Adapter"]
        RDBMS[("Relational Database<br/>SQLite / MySQL Server<br/>(Tables, Indexes, Triggers, Views)")]
    end

    CLI --> CS
    CLI --> PS
    CLI --> BS
    CLI --> RS
    
    CS --> DAO
    PS --> DAO
    BS --> DAO
    RS --> DAO
    
    DAO --> DBDriver
    DBDriver --> RDBMS
    
    RDBMS -.->|Raw SQL Query / sqlite3| PyPipeline
    PyPipeline --> Dashboard
```

---

## 2. Use Case Diagram

The Use Case model defines the functional interactions between the system actors (**Customer**, **Booking Agent / Travel Desk**, and **Data Analyst / Administrator**) and the core application modules.

```mermaid
flowchart LR
    Customer((Customer / Client))
    Agent((Booking Agent))
    Admin((Agency Admin / Analyst))

    subgraph "Travel Agency Booking & Analysis System"
        UC1(["Register / Update Customer Profile"])
        UC2(["Search & View Travel Packages"])
        UC3(["Book Travel Package with Headcount"])
        UC4(["Check Live Availability & Prevent Overbooking"])
        UC5(["Record Payment & Manage Status"])
        UC6(["Cancel Booking & Release Seats"])
        UC7(["Generate Operational Revenue Reports"])
        UC8(["Execute Tourism Trend Analysis & Forecast"])
    end

    Customer --> UC1
    Customer --> UC2
    Customer --> UC3

    Agent --> UC1
    Agent --> UC2
    Agent --> UC3
    Agent --> UC4
    Agent --> UC5
    Agent --> UC6
    Agent --> UC7

    Admin --> UC2
    Admin --> UC7
    Admin --> UC8

    UC3 ..>|<<include>>| UC4
    UC3 ..>|<<include>>| UC5
    UC6 ..>|<<include>>| UC4
```

---

## 3. Class Diagram

The Class Diagram highlights the Object-Oriented Principles (Encapsulation, Inheritance, Polymorphism, Abstraction) implemented in the Java source codebase.

```mermaid
classDiagram
    class Customer {
        -int customerId
        -String name
        -String email
        -String phone
        -String city
        +getCustomerId() int
        +getName() String
        +getEmail() String
        +getPhone() String
        +getCity() String
        +toString() String
    }

    class TravelPackage {
        -int packageId
        -String destination
        -int durationDays
        -double pricePerPerson
        -int maxCapacity
        -String category
        +getPackageId() int
        +getDestination() String
        +getDurationDays() int
        +getPricePerPerson() double
        +getMaxCapacity() int
        +getCategory() String
    }

    class Booking {
        -int bookingId
        -int customerId
        -int packageId
        -String bookingDate
        -String travelDate
        -int numTravelers
        -double totalAmount
        -String bookingStatus
        +getBookingId() int
        +getNumTravelers() int
        +getTotalAmount() double
        +getBookingStatus() String
        +calculateTotal(double unitPrice) double
    }

    class Payment {
        -int paymentId
        -int bookingId
        -String paymentDate
        -double amount
        -String paymentMethod
        -String paymentStatus
        +getPaymentId() int
        +getPaymentStatus() String
    }

    class Cancellation {
        -int cancellationId
        -int bookingId
        -String cancellationDate
        -String reason
        -double refundAmount
        +getCancellationId() int
        +getRefundAmount() double
    }

    class BookingService {
        -BookingDAO bookingDAO
        -PackageDAO packageDAO
        +createBooking(Booking b) boolean
        +cancelBooking(int bookingId, String reason) boolean
        +getAvailableSeats(int packageId) int
        +checkCapacity(int packageId, int travelers) boolean
    }

    Customer "1" <-- "*" Booking : places
    TravelPackage "1" <-- "*" Booking : booked_for
    Booking "1" <-- "1" Payment : settled_via
    Booking "1" <-- "0..1" Cancellation : triggers
    BookingService ..> Booking : manages
    BookingService ..> TravelPackage : checks
```

---

## 4. Sequence Diagram: Booking Creation with Overbooking Guard

This Sequence Diagram depicts how the system evaluates capacity dynamically before committing any reservation.

```mermaid
sequenceDiagram
    autonumber
    actor User as Booking Agent
    participant Main as Main CLI UI
    participant Service as BookingService
    participant PkgDAO as PackageDAO
    participant BookDAO as BookingDAO
    participant DB as Relational Database

    User->>Main: Enter Package ID, Customer ID, Traveler Count
    Main->>Service: createBooking(bookingRequest)
    Service->>PkgDAO: getPackageById(packageId)
    PkgDAO->>DB: SELECT * FROM travel_packages WHERE package_id=?
    DB-->>PkgDAO: Return Package Record (Capacity = 20)
    PkgDAO-->>Service: TravelPackage Object

    Service->>BookDAO: getBookedSeats(packageId)
    BookDAO->>DB: SELECT SUM(num_travelers) FROM bookings WHERE package_id=? AND status='CONFIRMED'
    DB-->>BookDAO: Sum = 17
    BookDAO-->>Service: 17 Seats Booked

    alt Requested Seats (e.g. 5) > Available Seats (20 - 17 = 3)
        Service-->>Main: Throw CapacityExceededException("Only 3 seats available!")
        Main-->>User: Display Error: Booking Rejected (Capacity Exceeded)
    else Requested Seats (e.g. 2) <= Available Seats (3)
        Service->>BookDAO: insertBooking(Booking)
        BookDAO->>DB: INSERT INTO bookings VALUES (...)
        DB-->>BookDAO: Success (Generated Booking ID)
        Service-->>Main: Booking Confirmed Notification
        Main-->>User: Display Success Receipt & Updated Seats
    end
```

---

## 5. Architectural Quality Attributes & Design Patterns
- **Data Access Object (DAO) Pattern:** Isolates database operations behind uniform interfaces (`CustomerDAO`, `PackageDAO`, `BookingDAO`).
- **Service Layer Pattern:** Encapsulates business logic, transactional checks, and validations away from presentation code.
- **Fail-Safe Capacity Guard:** Ensures concurrency and consistency so that total confirmed travelers never exceed package capacity limits.
- **Loose Coupling:** The Python data visualization module acts independently on the shared database tables without depending on the Java runtime.
