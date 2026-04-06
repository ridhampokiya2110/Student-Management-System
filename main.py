import sqlite3
import pandas as pd

class StudentManagementApp:
    def __init__(self, db_name="college_records.db"):
        self.db_name = db_name
        self.db_connection = sqlite3.connect(self.db_name)
        self.cursor = self.db_connection.cursor()
        self._initialize_database()

    def _initialize_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                roll_no INTEGER PRIMARY KEY,
                full_name TEXT NOT NULL,
                age INTEGER,
                course TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS academic (
                roll_no INTEGER PRIMARY KEY,
                attendance_pct INTEGER DEFAULT 0,
                math_marks INTEGER DEFAULT 0,
                science_marks INTEGER DEFAULT 0,
                FOREIGN KEY(roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
            )
        ''')

        try:
            default_users = [
                ('admin', 'admin123', 'admin'),
                ('teacher', 'teacher123', 'teacher'),
                ('101', 'student123', 'student')
            ]
            self.cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", default_users)
            
            self.cursor.execute("INSERT INTO students VALUES (101, 'Rahul Sharma', 20, 'BCA')")
            self.cursor.execute("INSERT INTO academic VALUES (101, 85, 90, 88)")
            self.db_connection.commit()
        except sqlite3.IntegrityError:
            pass

    def authenticate_user(self):
        print("\n--- STUDENT MANAGEMENT SYSTEM ---")
        input_username = input("Username: ").strip()
        input_password = input("Password: ").strip()

        self.cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?", 
            (input_username, input_password)
        )
        user_record = self.cursor.fetchone()

        if user_record:
            role = user_record[0]
            print(f"\nLogin Successful: {input_username} ({role.upper()})")
            return role, input_username
        
        print("\nInvalid credentials.")
        return None, None

    def display_dataframe(self, query):
        try:
            df = pd.read_sql_query(query, self.db_connection)
            if df.empty:
                print("No records found.")
            else:
                print("\n" + df.to_string(index=False) + "\n")
        except Exception as error:
            print(f"Error fetching data: {error}")

    def run_admin_dashboard(self):
        while True:
            print("\n--- ADMIN DASHBOARD ---")
            print("1. Enroll New Student")
            print("2. View All Student Records")
            print("3. Log Out")
            
            choice = input("Select an option (1-3): ").strip()

            if choice == '1':
                self._enroll_new_student()
            elif choice == '2':
                self.display_dataframe("SELECT * FROM students")
            elif choice == '3':
                break
            else:
                print("Invalid choice.")

    def _enroll_new_student(self):
        roll_no = input("Enter Roll Number: ").strip()
        name = input("Enter Full Name: ").strip()
        age = input("Enter Age: ").strip()
        course = input("Enter Course: ").strip()
        temp_password = input("Set temporary password: ").strip()
        
        try:
            self.cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?)", (roll_no, name, age, course))
            self.cursor.execute("INSERT INTO academic (roll_no) VALUES (?)", (roll_no,))
            self.cursor.execute("INSERT INTO users VALUES (?, ?, 'student')", (roll_no, temp_password))
            
            self.db_connection.commit()
            print("Student enrolled successfully.")
        except sqlite3.IntegrityError:
            print("Error: Roll Number already exists.")
        except Exception as e:
            print(f"Error: {e}")

    def run_teacher_dashboard(self):
        while True:
            print("\n--- TEACHER DASHBOARD ---")
            print("1. View Class Roster & Grades")
            print("2. Mark/Update Attendance")
            print("3. Grade a Student (Update Marks)")
            print("4. Log Out")
            
            choice = input("Select an option (1-4): ").strip()

            if choice == '1':
                query = '''
                    SELECT s.roll_no AS 'Roll No', s.full_name AS 'Name', 
                           a.attendance_pct AS 'Attendance %', a.math_marks AS 'Math', a.science_marks AS 'Science'
                    FROM students s 
                    JOIN academic a ON s.roll_no = a.roll_no
                '''
                self.display_dataframe(query)
            elif choice == '2':
                self._update_attendance()
            elif choice == '3':
                self._update_student_marks()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")

    def _update_attendance(self):
        roll_no = input("Enter Student Roll No: ").strip()
        attendance = input("Enter New Attendance Percentage (0-100): ").strip()
        
        if not attendance.isdigit() or not (0 <= int(attendance) <= 100):
            print("Invalid input! Attendance must be a number between 0 and 100.")
            return

        try:
            self.cursor.execute(
                "UPDATE academic SET attendance_pct=? WHERE roll_no=?", 
                (attendance, roll_no)
            )
            
            if self.cursor.rowcount == 0:
                print("Student not found.")
            else:
                self.db_connection.commit()
                print("Attendance updated successfully.")
        except Exception as e:
            print(f"Error updating attendance: {e}")

    def _update_student_marks(self):
        roll_no = input("Enter Student Roll No: ").strip()
        math = input("Enter Math Marks: ").strip()
        science = input("Enter Science Marks: ").strip()
        
        if not (math.isdigit() and science.isdigit()):
            print("Marks must be numeric.")
            return

        try:
            self.cursor.execute(
                "UPDATE academic SET math_marks=?, science_marks=? WHERE roll_no=?", 
                (math, science, roll_no)
            )
            
            if self.cursor.rowcount == 0:
                print("Student not found.")
            else:
                self.db_connection.commit()
                print("Grades updated successfully.")
        except Exception as e:
            print(f"Error updating grades: {e}")

    def run_student_dashboard(self, active_roll_no):
        while True:
            print("\n--- STUDENT DASHBOARD ---")
            print("1. View My Report Card")
            print("2. Log Out")
            
            choice = input("Select an option (1-2): ").strip()

            if choice == '1':
                query = f'''
                    SELECT s.roll_no AS 'Roll No', s.full_name AS 'Name', s.course AS 'Course',
                           a.attendance_pct AS 'Attendance %', a.math_marks AS 'Math', a.science_marks AS 'Science'
                    FROM students s 
                    JOIN academic a ON s.roll_no = a.roll_no 
                    WHERE s.roll_no = {active_roll_no}
                '''
                self.display_dataframe(query)
            elif choice == '2':
                break
            else:
                print("Invalid choice.")

    def start_application(self):
        try:
            while True:
                role, username = self.authenticate_user()
                
                if role == 'admin':
                    self.run_admin_dashboard()
                elif role == 'teacher':
                    self.run_teacher_dashboard()
                elif role == 'student':
                    self.run_student_dashboard(active_roll_no=username) 
                
                exit_prompt = input("\nPress Enter to login again, or type 'q' to quit: ").strip().lower()
                if exit_prompt == 'q':
                    break
        except KeyboardInterrupt:
            print("\nApplication closed.")
        finally:
            self.db_connection.close()


if __name__ == "__main__":
    app = StudentManagementApp()
    app.start_application()