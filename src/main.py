"""
Main Application Entry Point.
Provides an interactive command-line interface (CLI) for system management.
"""

import sys
from src.services.student_service import StudentService

def print_menu():
    print("\n" + "="*50)
    print("      STUDENT INFORMATION SYSTEM (Cloud-Ready)   ")
    print("="*50)
    print("1. Add New Student")
    print("2. View All Student Records")
    print("3. Search Student Records")
    print("4. Update Student Information")
    print("5. Delete Student Record")
    print("6. Export Student Records (XML/CSV)")
    print("7. Exit System")
    print("="*50)

def handle_add_student(service: StudentService):
    print("\n--- Add New Student ---")
    try:
        student_id = input("Enter Student ID: ").strip()
        name = input("Enter Full Name: ").strip()
        age = input("Enter Age: ").strip()
        email = input("Enter Email Address: ").strip()
        major = input("Enter Major/Course: ").strip()
        gpa = input("Enter GPA (0.0 - 4.0): ").strip()

        data = {
            "student_id": student_id,
            "name": name,
            "age": age,
            "email": email,
            "major": major,
            "gpa": gpa
        }
        student = service.create_student(data)
        print(f"\n SUCCESS: Student '{student.name}' added successfully!")
    except Exception as e:
        print(f"\n ERROR: Failed to add student. {e}")

def handle_view_students(service: StudentService):
    print("\n--- Student Records ---")
    students = service.get_all_students()
    if not students:
        print("No student records found.")
        return

    print(f"{'ID':<10} | {'Name':<20} | {'Age':<4} | {'Major':<15} | {'GPA':<5} | {'Email'}")
    print("-" * 80)
    for s in students:
        print(f"{s.student_id:<10} | {s.name:<20} | {s.age:<4} | {s.major:<15} | {s.gpa:<5.2f} | {s.email}")

def handle_search_students(service: StudentService):
    print("\n--- Search Students ---")
    query = input("Enter search query (ID, Name, or Major): ").strip()
    results = service.search_students(query)
    if not results:
        print(f"No matching student records found for query: '{query}'")
        return

    print(f"\nFound {len(results)} matching record(s):")
    print(f"{'ID':<10} | {'Name':<20} | {'Major':<15} | {'GPA':<5}")
    print("-" * 60)
    for s in results:
        print(f"{s.student_id:<10} | {s.name:<20} | {s.major:<15} | {s.gpa:<5.2f}")

def handle_update_student(service: StudentService):
    print("\n--- Update Student ---")
    student_id = input("Enter ID of student to update: ").strip()
    student = service.get_student_by_id(student_id)
    if not student:
        print(f"\n ERROR: Student ID '{student_id}' not found.")
        return

    print(f"Updating fields for {student.name}. (Press Enter to keep current value)")
    name = input(f"New Name [{student.name}]: ").strip() or student.name
    age = input(f"New Age [{student.age}]: ").strip() or student.age
    email = input(f"New Email [{student.email}]: ").strip() or student.email
    major = input(f"New Major [{student.major}]: ").strip() or student.major
    gpa = input(f"New GPA [{student.gpa}]: ").strip() or student.gpa

    updates = {"name": name, "age": age, "email": email, "major": major, "gpa": gpa}
    try:
        service.update_student(student_id, updates)
        print(f"\n SUCCESS: Student '{student_id}' updated successfully.")
    except Exception as e:
        print(f"\n ERROR: Update failed. {e}")

def handle_delete_student(service: StudentService):
    print("\n--- Delete Student Record ---")
    student_id = input("Enter Student ID to delete: ").strip()
    confirm = input(f"Are you sure you want to delete ID '{student_id}'? (y/N): ").strip().lower()
    if confirm == "y":
        try:
            service.delete_student(student_id)
            print(f"\n SUCCESS: Student record '{student_id}' deleted.")
        except Exception as e:
            print(f"\n ERROR: Deletion failed. {e}")

def handle_export(service: StudentService):
    print("\n--- Export Records ---")
    print("1. Export to XML")
    print("2. Export to CSV")
    choice = input("Select format (1-2): ").strip()
    try:
        if choice == "1":
            path = service.export_to_xml()
            print(f"\n SUCCESS: Exported to XML at '{path}'")
        elif choice == "2":
            path = service.export_to_csv()
            print(f"\n SUCCESS: Exported to CSV at '{path}'")
        else:
            print("\n Invalid export selection.")
    except Exception as e:
        print(f"\n ERROR: Export failed. {e}")

def main():
    service = StudentService()
    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()
        if choice == "1":
            handle_add_student(service)
        elif choice == "2":
            handle_view_students(service)
        elif choice == "3":
            handle_search_students(service)
        elif choice == "4":
            handle_update_student(service)
        elif choice == "5":
            handle_delete_student(service)
        elif choice == "6":
            handle_export(service)
        elif choice == "7":
            print("\nExiting Student Information System. Goodbye!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()