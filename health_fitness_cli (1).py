import json
import os
from datetime import datetime
from tabulate import tabulate
import statistics

def load_data(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([], f)
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

def generate_id(data, key):
    return max([item[key] for item in data], default=0) + 1

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Fitness Plan")
        print("2. View Plans")
        print("3. View Users")
        print("4. View User Logs")
        print("5. Generate Health Report")
        print("6. Logout")
        ch = input("Enter choice: ")
        if ch == '1':
            add_plan()
        elif ch == '2':
            view_plans()
        elif ch == '3':
            view_users()
        elif ch == '4':
            view_user_logs()
        elif ch == '5':
            generate_report()
        elif ch == '6':
            break
        else:
            print("Invalid option")

def user_menu(uid):
    while True:
        print("\n--- User Menu ---")
        print("1. View Fitness Plans")
        print("2. Log Daily Activity")
        print("3. Update Profile (Height/Weight)")
        print("4. View My Progress")
        print("5. Logout")
        ch = input("Enter choice: ")
        if ch == '1':
            view_plans()
        elif ch == '2':
            log_activity(uid)
        elif ch == '3':
            update_profile(uid)
        elif ch == '4':
            view_progress(uid)
        elif ch == '5':
            break
        else:
            print("Invalid option")

def add_plan():
    plans = load_data('plans.json')
    pid = generate_id(plans, 'plan_id')
    ptype = input("Type (Workout/Diet): ")
    desc = input("Description: ")
    plans.append({"plan_id": pid, "type": ptype, "description": desc})
    save_data('plans.json', plans)
    print("Plan added successfully")

def view_plans():
    plans = load_data('plans.json')
    if not plans:
        print("No plans found")
    else:
        print(tabulate(plans, headers="keys", tablefmt="grid"))

def register_user():
    users = load_data('users.json')
    uid = generate_id(users, 'user_id')
    name = input("Name: ")
    age = int(input("Age: "))
    height = float(input("Height (m): "))
    weight = float(input("Weight (kg): "))
    contact = input("Contact: ")
    users.append({"user_id": uid, "name": name, "age": age, "height": height, "weight": weight, "contact": contact})
    save_data('users.json', users)
    print(f"Registration successful! Your User ID is {uid}")

def view_users():
    users = load_data('users.json')
    if not users:
        print("No users found")
    else:
        print(tabulate(users, headers="keys", tablefmt="grid"))

def log_activity(uid):
    logs = load_data('logs.json')
    steps = int(input("Steps: "))
    calories_burned = int(input("Calories Burned: "))
    calories_consumed = int(input("Calories Consumed: "))
    exercise_time = float(input("Exercise Time (min): "))
    lid = generate_id(logs, 'log_id')
    date = datetime.now().strftime("%Y-%m-%d")
    logs.append({
        "log_id": lid, "user_id": uid, "date": date,
        "steps": steps, "calories_burned": calories_burned,
        "calories_consumed": calories_consumed, "exercise_time": exercise_time
    })
    save_data('logs.json', logs)
    print("Activity logged successfully")

def update_profile(uid):
    users = load_data('users.json')
    for u in users:
        if u['user_id'] == uid:
            u['height'] = float(input("New Height (m): "))
            u['weight'] = float(input("New Weight (kg): "))
            save_data('users.json', users)
            print("Profile updated successfully")
            return
    print("User not found")

def view_progress(uid):
    logs = load_data('logs.json')
    user_logs = [l for l in logs if l['user_id'] == uid]
    if not user_logs:
        print("No logs found")
    else:
        print(tabulate(user_logs, headers="keys", tablefmt="grid"))
        avg_steps = statistics.mean([l['steps'] for l in user_logs])
        avg_cal_burn = statistics.mean([l['calories_burned'] for l in user_logs])
        print(f"\nAverage Steps: {avg_steps:.2f}")
        print(f"Average Calories Burned: {avg_cal_burn:.2f}")

def view_user_logs():
    logs = load_data('logs.json')
    if not logs:
        print("No logs found")
    else:
        print(tabulate(logs, headers="keys", tablefmt="grid"))

def generate_report():
    logs = load_data('logs.json')
    if not logs:
        print("No logs found")
        return
    avg_steps = statistics.mean([l['steps'] for l in logs])
    avg_cal_burn = statistics.mean([l['calories_burned'] for l in logs])
    avg_cal_intake = statistics.mean([l['calories_consumed'] for l in logs])
    print("\n=== Health Report ===")
    print(f"Average Steps: {avg_steps:.2f}")
    print(f"Average Calories Burned: {avg_cal_burn:.2f}")
    print(f"Average Calories Consumed: {avg_cal_intake:.2f}")

def admin_login():
    aid = input("Enter Admin ID: ")
    pwd = input("Enter Password: ")
    if aid == "admin" and pwd == "admin123":
        admin_menu()
    else:
        print("Invalid credentials")

def user_login():
    users = load_data('users.json')
    uid = int(input("Enter User ID: "))
    for u in users:
        if u['user_id'] == uid:
            print(f"Welcome {u['name']}")
            user_menu(uid)
            return
    print("User not found")

def main():
    while True:
        print("\n=== Health & Fitness Tracking Portal ===")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Register as New User")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            admin_login()
        elif choice == '2':
            user_login()
        elif choice == '3':
            register_user()
        elif choice == '4':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()