
import json
import os
import re

FILE_NAME = "students.json"


def load_students():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            if not isinstance(data, list):
                print("Error: Invalid student data format.")
                return []
            return data
    except (json.JSONDecodeError, OSError):
        print("Error reading the file. Starting with an empty list.")
        return []


def save_students(students):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError:
        print("Error: Could not save student records.")
        return False


def add_student():
    students = load_students()

    roll = input("Enter Roll Number: ").strip()

    if not roll:
        print("Roll number cannot be empty.")
        return

    if any(s["roll"].lower() == roll.lower() for s in students):
        print("Roll number already exists!")
        return

    name = input("Enter Student Name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    email = input("Enter Email: ").strip()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        print("Invalid email address!")
        return

    try:
        gpa = float(input("Enter GPA (0-10): "))

        if not 0 <= gpa <= 10:
            print("GPA must be between 0 and 10.")
            return
    except ValueError:
        print("Please enter a valid number for GPA.")
        return

    student = {
        "roll": roll,
        "name": name,
        "email": email,
        "gpa": gpa
    }

    students.append(student)
    if not save_students(students):
        return
    print("Student added successfully!")


def view_students():
    students = load_students()

    if not students:
        print("No student records found.")
        return

    for s in students:
        print("--------------------")
        print("Roll Number:", s["roll"])
        print("Name:", s["name"])
        print("Email:", s["email"])
        print("GPA:", s["gpa"])


def search_student():
    students = load_students()
    query = input("Enter Roll Number or Name to search: ").strip().lower()

    if not query:
        print("Search input cannot be empty.")
        return

    found = False

    for s in students:
        if (query in s["roll"].lower()
                or query in s["name"].lower()):
            print(s)
            found = True

    if not found:
        print("Student not found.")


def update_student():
    students = load_students()
    roll = input("Enter Roll Number to update: ").strip().lower()

    for s in students:
        if s["roll"].lower() == roll:
            name = input("Enter new name (press Enter to keep old): ").strip()
            email = input("Enter new email (press Enter to keep old): ").strip()
            gpa_text = input("Enter new GPA (press Enter to keep old): ").strip()

            if name:
                s["name"] = name

            if email:
                if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                    print("Invalid email. Update cancelled.")
                    return
                s["email"] = email

            if gpa_text:
                try:
                    gpa = float(gpa_text)
                    if not 0 <= gpa <= 10:
                        print("GPA must be between 0 and 10.")
                        return
                    s["gpa"] = gpa
                except ValueError:
                    print("Invalid GPA. Update cancelled.")
                    return

            if not save_students(students):
                return
            print("Student updated successfully!")
            return

    print("Student not found.")


def delete_student():
    students = load_students()
    roll = input("Enter Roll Number to delete: ").strip().lower()

    for s in students:
        if s["roll"].lower() == roll:
            students.remove(s)
            if not save_students(students):
                return
            print("Student deleted successfully!")
            return

    print("Student not found.")


while True:
    print("\n===== STUDENT RECORD MANAGEMENT =====")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        add_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        print("Thank you!")
        break
    else:
        print("Invalid choice. Please select 1-6.")