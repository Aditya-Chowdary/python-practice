import time

task = input("What should I remind you to do? ")
minutes = int(input("In how many minutes? "))

print(f"Okay! I will remind you to '{task}' in {minutes} minute(s).")
time.sleep(minutes * 60)

# Reminder
print(f"⏰ Reminder: {task}")
