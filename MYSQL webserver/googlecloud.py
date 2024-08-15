#!/usr/bin/python3
import pymysql

# Google Cloud Connection
db = pymysql.connect(host='35.234.77.213',
                     user='root',
                     password='123456789',
                     cursorclass=pymysql.cursors.DictCursor)

try:
    with db.cursor() as cursor:
        # Create 'patients' database if it doesn't exist
        create_db_query = "CREATE DATABASE IF NOT EXISTS patients"
        cursor.execute(create_db_query)

        # Select the 'patients' database
        use_db_query = "USE patients"
        cursor.execute(use_db_query)

        # Create patients table if it doesn't exist
        create_patients_table = """
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patientname VARCHAR(100),
            patientinfo TEXT
        )
        """
        cursor.execute(create_patients_table)

        # Wipe everything from the 'patients' table
        truncate_table_query = "TRUNCATE TABLE patients"
        cursor.execute(truncate_table_query)

    with db.cursor() as cursor:
        # Inserting dummy data into the 'patients' table
        insert_data_query = """
        INSERT INTO patients (patientname, patientinfo)
        VALUES
            ('John Doe', 'Age: 35, Blood Type: A+, Allergies: None'),
            ('Jane Smith', 'Age: 28, Blood Type: B-, Allergies: Pollen'),
            ('Alice Johnson', 'Age: 45, Blood Type: O-, Allergies: Peanuts')
        """
        cursor.execute(insert_data_query)

    # Commit changes
    db.commit()
    print("Table 'patients' wiped and dummy data inserted successfully!")

except pymysql.Error as e:
    print(f"Error: {e}")

finally:
    db.close()
