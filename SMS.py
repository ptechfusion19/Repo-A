# Student Management System (CRUD Operations)
# Data stored in a list, not in a dictionary

students = []  # Each student = [ID, Name, CGPA]

# ------------------ CREATE ------------------
def insert_student():
    student_id = input("Enter Student ID: ")
    
    # Check if ID already exists
    for student in students:
        if student[0] == student_id:
            print("❌ Student ID already exists!")
            return

    name = input("Enter Student Name: ")
    cgpa = float(input("Enter Student CGPA: "))
    students.append([student_id, name, cgpa])
    print("✅ Student added successfully!\n")

# ------------------ READ ------------------
def read_students():
    if not students:
        print("⚠️ No student records found.\n")
        return
    print("\n📘 Student Records:")
    print("-" * 40)
    for s in students:
        print(f"ID: {s[0]} | Name: {s[1]} | CGPA: {s[2]}")
    print("-" * 40 + "\n")

# ------------------ UPDATE ------------------
def update_student():
    student_id = input("Enter Student ID to update: ")
    for s in students:
        if s[0] == student_id:
            print(f"Current Record → ID: {s[0]}, Name: {s[1]}, CGPA: {s[2]}")
            new_name = input("Enter new name (leave blank to keep same): ")
            new_cgpa = input("Enter new CGPA (leave blank to keep same): ")

            if new_name:
                s[1] = new_name
            if new_cgpa:
                s[2] = float(new_cgpa)
            
            print("✅ Student record updated!\n")
            return
    print("❌ Student not found!\n")

# ------------------ DELETE ------------------
def delete_student():
    student_id = input("Enter Student ID to delete: ")
    for s in students:
        if s[0] == student_id:
            students.remove(s)
            print("✅ Student deleted successfully!\n")
            return
    print("❌ Student not found!\n")

# ------------------ MAIN PROGRAM ------------------
def main():
    while True:
        print("===== Student Management System =====")
        print("1. Insert Student")
        print("2. Read Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            insert_student()
        elif choice == '2':
            read_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            print("👋 Exiting program...")
            break
        else:
            print("❌ Invalid choice. Please try again!\n")

# Run the program
if __name__ == "__main__":
    main()