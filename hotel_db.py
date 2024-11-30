import mysql.connector


def setup_database():
    try:
        # Establish connection
        db1 = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )

        # Create cursor
        c1 = db1.cursor()

        # Drop existing database if needed (commented out for safety)
        # c1.execute("DROP DATABASE IF EXISTS hotel")

        # Create and set up database
        c1.execute("CREATE DATABASE IF NOT EXISTS hotel")
        c1.execute("USE hotel")

        # Create rooms table (fixed typo in previous version)
        c1.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            room_no INTEGER PRIMARY KEY,
            type VARCHAR(50),
            location VARCHAR(30),
            no_of_guest INTEGER,
            rent INTEGER, 
            status VARCHAR(20)
        )
        """)

        # Create booking table
        c1.execute("""
        CREATE TABLE IF NOT EXISTS booking (
            cname VARCHAR(50),
            idno VARCHAR(40),
            idtype VARCHAR(40), 
            address VARCHAR(100), 
            phone VARCHAR(15),
            gender VARCHAR(20), 
            dateofcheckin DATE,
            room_no INTEGER,
            FOREIGN KEY (room_no) REFERENCES rooms(room_no)
        )
        """)

        # Commit changes
        db1.commit()

        print("Database and tables created successfully!")

        # Close connections
        c1.close()
        db1.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Run the setup when the script is executed
if __name__ == "__main__":
    setup_database()