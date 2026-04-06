# 🎓 College Student Management System (CLI)

A robust, console-based Student Management System built using **Python**, **SQLite3**, and **Pandas**. It features Role-Based Access Control (RBAC) providing dedicated, secure dashboards for Admins, Teachers, and Students.

## 🚀 Features

* **Role-Based Access Control (RBAC):** Separate login flows and menus for Admin, Teacher, and Student.
* **Persistent Database:** Uses `sqlite3` to store users, student profiles, and academic records locally without needing a separate server.
* **Clean Data Formatting:** Integrates `pandas` to display complex SQL queries (like JOINs) as clean, readable tables in the terminal.
* **Relational Data Mapping:** Links student personal data with academic performance using Primary and Foreign Keys.
* **Error Handling & Data Validation:** Graceful error catching for invalid inputs (e.g., entering text instead of numbers for marks) and safe application exits (`KeyboardInterrupt` handling).

## 💻 Tech Stack

* **Language:** Python 3.x
* **Database:** SQLite3 (Built-in standard library)
* **Data Handling/Display:** Pandas

