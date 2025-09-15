import datetime
import csv
from datetime import timedelta

FILENAME = "attendance.txt"

# MARK ATTENDANCE
def mark_attendance(roll_no, name, status):
    date = datetime.date.today()
    with open(FILENAME, "a") as f:
        f.write(f"{roll_no},{name},{date},{status}\n")
    print(f"Attendance marked for {name} ({roll_no}) as {status} on {date}")

# VIEW ATTENDANCE BY ROLL NUMBER
def search_attendance(roll_no):
    found = False
    try:
        with open(FILENAME, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    continue
                rno, name, date, status = parts
                if rno == roll_no:
                    print(f"{date} - {name} - {status}")
                    found = True
        if not found:
            print("No records found for this roll number.")
    except FileNotFoundError:
        print("Attendance file not found.")

# CUMULATIVE REPORT
def generate_cumulative_report():
    students = {}
    try:
        with open(FILENAME, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    continue
                rno, name, date, status = parts
                if rno not in students:
                    students[rno] = {"name": name, "present": 0, "total": 0}
                students[rno]["total"] += 1
                if status.upper() == "P":
                    students[rno]["present"] += 1
        
        print("\nCumulative Attendance Report:")
        print("RollNo | Name | % Attendance | Status")
        for rno, data in students.items():
            percent = (data["present"] / data["total"]) * 100
            status = "Defaulter" if percent < 75 else "OK"
            # Highlight defaulters
            highlight = " <<< BELOW 75%" if percent < 75 else ""
            print(f"{rno} | {data['name']} | {percent:.2f}% | {status}{highlight}")
    except FileNotFoundError:
        print("Attendance file not found.")


# WEEKLY REPORT
def weekly_report():
    today = datetime.date.today()
    week_ago = today - timedelta(days=7)
    students = {}

    try:
        with open(FILENAME, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    continue
                rno, name, record_date, status = parts
                record_date_obj = datetime.datetime.strptime(record_date, "%Y-%m-%d").date()
                if week_ago <= record_date_obj <= today:
                    if rno not in students:
                        students[rno] = {"name": name, "present": 0, "total": 0}
                    students[rno]["total"] += 1
                    if status.upper() == "P":
                        students[rno]["present"] += 1
        
        print("\nWeekly Attendance Report:")
        print("RollNo | Name | % Attendance | Status")
        for rno, data in students.items():
            percent = (data["present"] / data["total"]) * 100
            status = "Defaulter" if percent < 75 else "OK"
            highlight = " <<< BELOW 75%" if percent < 75 else ""
            print(f"{rno} | {data['name']} | {percent:.2f}% | {status}{highlight}")
    except FileNotFoundError:
        print("Attendance file not found.")


# DAILY REPORT
def daily_report():
    date = input("Enter date for report (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = str(datetime.date.today())
    print(f"\nDaily Attendance Report for {date}:")
    found = False
    try:
        with open(FILENAME, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 4:
                    continue
                rno, name, record_date, status = parts
                if record_date == date:
                    # Highlight absent students
                    highlight = " <<< Absent" if status.upper() != "P" else ""
                    print(f"{rno} | {name} | {status}{highlight}")
                    found = True
        if not found:
            print("No records found for this date.")
    except FileNotFoundError:
        print("Attendance file not found.")


# BULK UPLOAD
def bulk_upload(source_file):
    try:
        with open(source_file, "r") as src, open(FILENAME, "a") as tgt:
            reader = csv.reader(src)
            for row in reader:
                if not row:
                    continue
                tgt.write(",".join(row) + "\n")
        print("Bulk upload completed.")
    except FileNotFoundError:
        print("Source file not found.")

# BULK DOWNLOAD
def bulk_download(export_file):
    try:
        with open(FILENAME, "r") as src, open(export_file, "w") as tgt:
            data = src.readlines()
            tgt.writelines(data)
        print(f"Data exported to {export_file}")
    except FileNotFoundError:
        print("Attendance file not found.")

# MAIN MENU
def main():
    while True:
        print("\n--- Attendance Tracker ---")
        print("1. Mark Attendance")
        print("2. Search by Roll Number")
        print("3. Generate Report")
        print("4. Bulk Upload")
        print("5. Bulk Download")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            roll_no = input("Enter Roll Number: ")
            name = input("Enter Name: ")
            status = input("Enter Status (P/A): ").upper()
            mark_attendance(roll_no, name, status)
        elif choice == "2":
            roll_no = input("Enter Roll Number to search: ")
            search_attendance(roll_no)
        elif choice == "3":
            print("\nSelect Report Type:")
            print("1. Cumulative Report")
            print("2. Daily Report")
            print("3. Weekly Report")
            report_choice = input("Enter choice: ")
            
            if report_choice == "1":
                generate_cumulative_report()
            elif report_choice == "2":
                daily_report()
            elif report_choice == "3":
                weekly_report()
            else:
                print("Invalid choice, returning to main menu.")
        elif choice == "4":
            file = input("Enter CSV file path for bulk upload: ")
            bulk_upload(file)
        elif choice == "5":
            file = input("Enter export file name (CSV/TXT): ")
            bulk_download(file)
        elif choice == "6":
            print("Exiting program.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
