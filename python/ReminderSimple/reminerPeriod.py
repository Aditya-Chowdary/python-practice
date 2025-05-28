import time
import schedule
from datetime import datetime

def notify(task):
    print(f"\n🔔 Reminder: {task} — {datetime.now().strftime('%H:%M:%S')}")

def setup_repeating_reminder():
    task = input("What do you want to be reminded about? ")
    interval = int(input("Repeat every how many minutes? "))

    schedule.every(interval).minutes.do(notify, task=task)
    print(f"✅ Reminder set every {interval} minutes.")

def setup_daily_reminder():
    task = input("What do you want to be reminded about? ")
    time_str = input("At what time daily? (HH:MM 24-hour format): ")

    try:
        schedule.every().day.at(time_str).do(notify, task=task)
        print(f"✅ Daily reminder set at {time_str}.")
    except:
        print("❌ Invalid time format. Use HH:MM (e.g., 09:30).")

def main():
    print("🔔 Task Reminder Options:")
    print("1. Remind every X minutes")
    print("2. Remind daily at specific time")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        setup_repeating_reminder()
    elif choice == '2':
        setup_daily_reminder()
    else:
        print("❌ Invalid choice")
        return

    print("⏳ Reminder started. Press Ctrl+C to stop.\n")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
