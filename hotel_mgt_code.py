import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import mysql.connector
import datetime


class HotelManagementSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x600")

        # Database connection
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="hotel"
            )
            self.cursor = self.con.cursor(dictionary=True)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to database: {e}")
            root.quit()

        # Create main menu
        self.create_menu()

    def create_menu(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create frames for different operations
        self.rooms_frame = ttk.Frame(self.notebook)
        self.booking_frame = ttk.Frame(self.notebook)
        self.checkout_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.rooms_frame, text='Rooms')
        self.notebook.add(self.booking_frame, text='Book Room')
        self.notebook.add(self.checkout_frame, text='Check Out')

        # Setup room management tab
        self.setup_rooms_tab()
        self.setup_booking_tab()
        self.setup_checkout_tab()

    def setup_rooms_tab(self):
        # Rooms Management Frame
        tk.Label(self.rooms_frame, text="Room Management", font=('Arial', 16)).pack(pady=10)

        # Buttons for room operations
        btn_frame = tk.Frame(self.rooms_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Create New Room", command=self.create_room_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Show All Rooms", command=self.show_all_rooms).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Show Vacant Rooms", command=self.show_vacant_rooms).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Show Occupied Rooms", command=self.show_occupied_rooms).pack(side=tk.LEFT, padx=5)

        # Treeview to display rooms
        self.rooms_tree = ttk.Treeview(self.rooms_frame,
                                       columns=('Room No', 'Type', 'Location', 'Max Guests', 'Rent', 'Status'),
                                       show='headings')
        for col in self.rooms_tree['columns']:
            self.rooms_tree.heading(col, text=col)
        self.rooms_tree.pack(expand=True, fill='both', padx=10, pady=10)

    def setup_booking_tab(self):
        # Booking Frame
        tk.Label(self.booking_frame, text="Room Booking", font=('Arial', 16)).pack(pady=10)

        # Booking Form
        form_frame = tk.Frame(self.booking_frame)
        form_frame.pack(pady=10)

        labels = ['Room Number', 'Customer Name', 'ID Type', 'ID Number', 'Address', 'Phone', 'Gender', 'Check-in Date']
        self.booking_entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=i, column=0, sticky='w', padx=5, pady=2)
            if label == 'Check-in Date':
                self.booking_entries[label] = tk.Entry(form_frame)
                self.booking_entries[label].insert(0, datetime.date.today().strftime('%Y-%m-%d'))
            else:
                self.booking_entries[label] = tk.Entry(form_frame)
            self.booking_entries[label].grid(row=i, column=1, padx=5, pady=2)

        # Book Room Button
        tk.Button(form_frame, text="Book Room", command=self.book_room).grid(row=len(labels), column=0, columnspan=2,
                                                                             pady=10)

    def setup_checkout_tab(self):
        # Checkout Frame
        tk.Label(self.checkout_frame, text="Room Checkout", font=('Arial', 16)).pack(pady=10)

        # Checkout Form
        checkout_frame = tk.Frame(self.checkout_frame)
        checkout_frame.pack(pady=10)

        tk.Label(checkout_frame, text="Room Number").pack()
        self.checkout_entry = tk.Entry(checkout_frame)
        self.checkout_entry.pack(pady=5)

        tk.Button(checkout_frame, text="Check Out", command=self.checkout_room).pack(pady=10)

        # Checkout Details Display
        self.checkout_details = tk.Text(self.checkout_frame, height=10, width=70)
        self.checkout_details.pack(pady=10)

    def create_room_dialog(self):
        # Create Room Dialog
        try:
            room_no = simpledialog.askinteger("Create Room", "Enter Room Number:")
            if not room_no:
                return

            # Check if room already exists
            self.cursor.execute("SELECT * FROM rooms WHERE room_no = %s", (room_no,))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "Room already exists!")
                return

            # Collect room details
            type = simpledialog.askstring("Room Type", "Enter Room Type (Simple/Delux/Super Delux):")
            guest = simpledialog.askinteger("Max Guests", "Enter maximum number of guests:")
            loc = simpledialog.askstring("Location", "Enter Location details:")
            rent = simpledialog.askinteger("Rent", "Enter Per Day Charges:")

            # Insert room
            query = "INSERT INTO rooms (room_no, type, location, no_of_guest, rent, status) VALUES (%s, %s, %s, %s, %s, %s)"
            data = (room_no, type, loc, guest, rent, "Vacant")

            self.cursor.execute(query, data)
            self.con.commit()
            messagebox.showinfo("Success", "Room Created Successfully")

            # Refresh rooms view
            self.show_all_rooms()

        except Exception as e:
            messagebox.showerror("Error", f"Error creating room: {e}")
            self.con.rollback()

    def show_all_rooms(self):
        # Clear existing items
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)

        # Fetch and display rooms
        try:
            self.cursor.execute("SELECT * FROM rooms")
            rooms = self.cursor.fetchall()

            for room in rooms:
                self.rooms_tree.insert('', 'end', values=(
                    room['room_no'], room['type'], room['location'],
                    room['no_of_guest'], room['rent'], room['status']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error showing rooms: {e}")

    def show_vacant_rooms(self):
        # Clear existing items
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)

        # Fetch and display vacant rooms
        try:
            self.cursor.execute("SELECT * FROM rooms WHERE status='Vacant'")
            rooms = self.cursor.fetchall()

            for room in rooms:
                self.rooms_tree.insert('', 'end', values=(
                    room['room_no'], room['type'], room['location'],
                    room['no_of_guest'], room['rent'], room['status']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error showing vacant rooms: {e}")

    def show_occupied_rooms(self):
        # Clear existing items
        for item in self.rooms_tree.get_children():
            self.rooms_tree.delete(item)

        # Fetch and display occupied rooms
        try:
            query = """
            SELECT r.room_no, b.cname, r.type, b.dateofcheckin, 
                   b.phone, r.status 
            FROM rooms r 
            JOIN booking b ON r.room_no = b.room_no 
            WHERE r.status='Occupied'
            """
            self.cursor.execute(query)
            rooms = self.cursor.fetchall()

            for room in rooms:
                self.rooms_tree.insert('', 'end', values=(
                    room['room_no'], room['type'],
                    f"Guest: {room['cname']}", '', '', room['status']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error showing occupied rooms: {e}")

    def book_room(self):
        # Collect booking details from entries
        try:
            room_no = int(self.booking_entries['Room Number'].get())

            # Check if room is vacant
            self.cursor.execute("SELECT * FROM rooms WHERE room_no = %s AND status = 'Vacant'", (room_no,))
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "Room is not available for booking!")
                return

            # Collect booking details
            booking_data = {
                'room_no': room_no,
                'cname': self.booking_entries['Customer Name'].get(),
                'idtype': self.booking_entries['ID Type'].get(),
                'idno': self.booking_entries['ID Number'].get(),
                'address': self.booking_entries['Address'].get(),
                'phone': self.booking_entries['Phone'].get(),
                'gender': self.booking_entries['Gender'].get(),
                'dateofcheckin': self.booking_entries['Check-in Date'].get()
            }

            # Insert booking details
            booking_query = """
            INSERT INTO booking 
            (cname, idno, idtype, address, phone, gender, dateofcheckin, room_no) 
            VALUES (%(cname)s, %(idno)s, %(idtype)s, %(address)s, %(phone)s, %(gender)s, %(dateofcheckin)s, %(room_no)s)
            """

            # Update room status
            update_room_query = "UPDATE rooms SET status='Occupied' WHERE room_no = %(room_no)s"

            self.cursor.execute(booking_query, booking_data)
            self.cursor.execute(update_room_query, booking_data)

            self.con.commit()
            messagebox.showinfo("Success", "Room Booked Successfully")

            # Refresh rooms view
            self.show_all_rooms()

            # Clear booking entries
            for entry in self.booking_entries.values():
                entry.delete(0, tk.END)
            self.booking_entries['Check-in Date'].insert(0, datetime.date.today().strftime('%Y-%m-%d'))

        except Exception as e:
            messagebox.showerror("Error", f"Error booking room: {e}")
            self.con.rollback()

    def checkout_room(self):
        try:
            room_no = int(self.checkout_entry.get())

            # Verify room is occupied
            self.cursor.execute("""
                SELECT b.*, r.type, r.rent 
                FROM booking b 
                JOIN rooms r ON b.room_no = r.room_no 
                WHERE r.room_no = %s AND r.status = 'Occupied'
            """, (room_no,))

            booking = self.cursor.fetchone()

            if not booking:
                messagebox.showerror("Error", "No active booking found for this room.")
                return

            # Calculate stay duration and bill
            checkin_date = booking['dateofcheckin']
            checkout_date = datetime.date.today()
            stay_duration = (checkout_date - checkin_date).days

            total_bill = stay_duration * booking['rent']

            # Display checkout details
            checkout_info = f"""
Checkout Details:
Customer Name: {booking['cname']}
Room Type: {booking['type']}
Room Number: {room_no}
Check-in Date: {booking['dateofcheckin']}
Check-out Date: {checkout_date}
Stay Duration: {stay_duration} days
Total Bill: ${total_bill}
            """

            self.checkout_details.delete(1.0, tk.END)
            self.checkout_details.insert(tk.END, checkout_info)

            # Update room status and remove booking
            update_room_query = "UPDATE rooms SET status='Vacant' WHERE room_no = %s"
            delete_booking_query = "DELETE FROM booking WHERE room_no = %s"

            self.cursor.execute(update_room_query, (room_no,))
            self.cursor.execute(delete_booking_query, (room_no,))

            self.con.commit()

            # Refresh rooms view
            self.show_all_rooms()

            messagebox.showinfo("Success", "Checkout Successful!")

        except Exception as e:
            messagebox.showerror("Error", f"Error during checkout: {e}")
            self.con.rollback()

    def __del__(self):
        if hasattr(self, 'con') and self.con.is_connected():
            self.cursor.close()
            self.con.close()


def main():
    root = tk.Tk()
    app = HotelManagementSystemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()