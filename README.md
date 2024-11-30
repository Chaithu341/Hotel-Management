# Hotel-Management
This project is a Hotel Management System built using Python and MySQL, featuring a GUI for managing rooms, bookings, and checkouts. It allows users to create rooms, book available ones, and process checkouts with bill calculation.
### **Instructions to Run the Hotel Management System Project**

1. **Install Python**: Ensure that Python 3.x is installed on your system. You can download it from [here](https://www.python.org/downloads/).

2. **Install MySQL**: Install MySQL and ensure the MySQL server is running on your machine. You can download it from [here](https://dev.mysql.com/downloads/installer/).

3. **Install Required Python Libraries**: Install the necessary Python libraries, particularly `mysql-connector` for MySQL interaction and `tkinter` for GUI. You can install them using `pip`:
   ```bash
   pip install mysql-connector tkinter
   ```

4. **Set Up the Database**:
   - Create a MySQL database by running the `hotel_db.py` script.
   - Open a terminal or command prompt and navigate to the folder containing the `hotel_db.py` file.
   - Run the script:
     ```bash
     python hotel_db.py
     ```
   - This will set up the database `hotel` and create the necessary tables (`rooms` and `booking`).

5. **Run the Main Application**:
   - Run the `smart_hotel.py` script to launch the Hotel Management System GUI.
   - In the terminal, navigate to the folder containing the `smart_hotel.py` file and run:
     ```bash
     python smart_hotel.py
     ```

6. **Interacting with the Application**:
   - After running the `smart_hotel.py` script, the Hotel Management System will open.
   - It provides three main tabs:
     - **Rooms**: Manage room creation, view all rooms, vacant rooms, and occupied rooms.
     - **Book Room**: Book a room by entering customer details and room number.
     - **Check Out**: Process checkout for a booked room, including bill calculation.

---

### **Project Description**

The **Hotel Management System** is a software application designed to manage the operations of a hotel, including room management, room booking, and guest checkout. The system is built using **Python** for the backend logic and **MySQL** for database management. The graphical user interface (GUI) is created using **Tkinter**, making it user-friendly and easy to interact with.

#### **Core Features**:
1. **Room Management**:
   - Admins can create rooms by providing room details such as room number, type, location, max guests, rent, and status.
   - Users can view all rooms, see vacant or occupied rooms, and manage room statuses.

2. **Booking System**:
   - Users can book a room by entering guest details (name, ID type, address, phone number, etc.).
   - The system checks if the selected room is available and books it, marking the room as occupied.

3. **Checkout System**:
   - Users can check out after completing their stay. The system calculates the total bill based on the number of days stayed and the room rent.
   - After checkout, the room status is updated to vacant, and the booking record is deleted.

#### **Technical Components**:
- **Backend**: Uses Python with MySQL to manage database interactions (room and booking data).
- **Frontend**: Built using Tkinter, providing an interactive, tabbed interface with buttons and entry forms for easy room management, booking, and checkout.
- **Database**: The project uses a MySQL database to store room and booking details. Tables include `rooms` (for storing room details) and `booking` (for storing customer bookings).

#### **Database Structure**:
- **rooms table**: Contains information about room number, type, location, number of guests, rent, and status (vacant/occupied).
- **booking table**: Stores customer details, room number, check-in date, and links to the `rooms` table.

This project is aimed at automating hotel operations and simplifying room management, bookings, and checkout processes for hotel staff, making it easier for them to maintain guest records and room statuses in real-time.
