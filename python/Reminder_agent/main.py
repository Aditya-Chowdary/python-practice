# main.py
import time
import schedule
from datetime import datetime
import sys
import traceback # For detailed error printing

import db_manager # Uses MySQL
import llm_utils  # Uses Ollama
import utils

# --- Reminder Checking Job ---
def check_reminders():
    # print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for due reminders...") # Verbose
    due_reminders = db_manager.get_due_reminders() # Returns list of dicts
    if not due_reminders:
        return

    for reminder_data in due_reminders:
        reminder_id = reminder_data['id']
        task = reminder_data['task']
        # MySQL connector returns DATETIME columns as Python datetime objects
        due_date_obj = reminder_data['due_date']

        try:
            fabulous_alert_prompt = (
                f"It's time for a scheduled reminder! The task is: '{task}'. "
                f"It was scheduled for {due_date_obj.strftime('%A, %B %d at %I:%M %p')}. "
                "Announce this reminder fabulously."
            )
            fabulous_alert = llm_utils.generate_fabulous_response(fabulous_alert_prompt)

            print("\n✨🔔 FABULOUS REMINDER ALERT! 🔔✨")
            print(fabulous_alert)
            # print(f"✨ Task: {task}") # LLM should include this
            # print(f"✨ Originally Due: {due_date_obj.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-------------------------------------\n")
            db_manager.mark_as_reminded(reminder_id)

        except Exception as e:
            print(f"Error processing reminder ID {reminder_id} ('{task}'): {e}")
            traceback.print_exc()


# --- Main Application Loop ---
def run_agent():
    # Attempt to initialize DB. If db_manager.py has critical errors due to .env, it might exit.
    db_manager.init_db()

    greeting_prompt = "You are FabuBot, a personal AI reminder assistant. Greet the user enthusiastically and tell them you're ready to help them shine today. Introduce yourself."
    print(llm_utils.generate_fabulous_response(greeting_prompt))
    print("Type 'exit' to quit, 'list' to see active reminders.")

    schedule.every(20).seconds.do(check_reminders) # Check frequently; adjust as needed

    last_input_prompt_time = 0

    while True:
        schedule.run_pending()
        current_time = time.time()
        if current_time - last_input_prompt_time > 5: # Show prompt if idle for 5s
             print("\nFabuBot is listening... (Type 'exit', 'list', or your reminder)")
             last_input_prompt_time = current_time

        try:
            user_input = input("> ").strip()
            if not user_input:
                time.sleep(0.1) # Allow schedule to run if input is empty
                continue
            last_input_prompt_time = time.time() # Reset timer after input

            if user_input.lower() == 'exit':
                farewell_prompt = "The user is exiting. Say goodbye in a fabulous and encouraging way."
                print(llm_utils.generate_fabulous_response(farewell_prompt))
                break
            elif user_input.lower() == 'list':
                reminders = db_manager.get_active_reminders() # Returns list of dicts
                if not reminders:
                    print(llm_utils.generate_fabulous_response("Your schedule is absolutely clear, darling! A perfect canvas for new adventures or a moment of fabulous rest!"))
                else:
                    print("\n🌟 Your Dazzling To-Do List, Sweetie: 🌟")
                    for r_data in reminders:
                        r_id = r_data['id']
                        task = r_data['task']
                        due_dt_obj = r_data['due_date'] # datetime object from MySQL
                        print(f"  - (ID: {r_id}) {task} (Due: {due_dt_obj.strftime('%Y-%m-%d %I:%M %p')})")
                    print("-------------------------------------\n")
                continue

            print("FabuBot is thinking with a sparkle...")
            task, datetime_str = llm_utils.extract_reminder_details(user_input)

            if task and datetime_str:
                parsed_due_date = utils.parse_datetime_string(datetime_str) # Returns naive datetime
                if parsed_due_date:
                    if parsed_due_date < datetime.now(): # Compare naive with naive
                        past_date_prompt = (
                            f"The user tried to set a reminder for '{task}' at '{datetime_str}', "
                            f"which I parsed as {parsed_due_date.strftime('%Y-%m-%d %H:%M:%S')}. This date is in the past. "
                            "Politely and fabulously point this out and ask them to try a future date."
                        )
                        print(llm_utils.generate_fabulous_response(past_date_prompt))
                        continue

                    reminder_id = db_manager.add_reminder(task, parsed_due_date)
                    if reminder_id:
                        confirmation_prompt = (
                            f"I've successfully scheduled a reminder for: '{task}' on "
                            f"{parsed_due_date.strftime('%A, %B %d, %Y at %I:%M %p')}. "
                            "Confirm this to the user in a marvelous and fabulous way."
                        )
                        print(llm_utils.generate_fabulous_response(confirmation_prompt))
                    else:
                        print(llm_utils.generate_fabulous_response("Oh no, my database circuits are having a moment! I couldn't save that reminder, sweetie. Perhaps try again?"))
                else:
                    cant_parse_date_prompt = (
                        f"The user asked to set a reminder for '{task}' but I couldn't understand the date/time: '{datetime_str}'. "
                        "Politely ask them to be more specific with the date or time in a fabulous way."
                    )
                    print(llm_utils.generate_fabulous_response(cant_parse_date_prompt))
            elif task and not datetime_str:
                 no_time_prompt = (
                    f"The user wants to remember '{task}', but didn't specify when. "
                    "Ask them for the time/date for this task in a fabulous and encouraging manner."
                 )
                 print(llm_utils.generate_fabulous_response(no_time_prompt))
            else: # Unrecognized command or general chat
                general_chat_prompt = (
                    f"The user said: '{user_input}'. This doesn't seem to be a reminder command. "
                    "Respond in a general, helpful, witty, and fabulous way as FabuBot."
                )
                print(llm_utils.generate_fabulous_response(general_chat_prompt))

        except KeyboardInterrupt:
            farewell_prompt = "The user pressed Ctrl+C to exit. Say a quick, fabulous goodbye."
            print(f"\n{llm_utils.generate_fabulous_response(farewell_prompt)}")
            sys.exit(0) # Clean exit
        except Exception as e:
            print(f"An unexpected oopsie daisy occurred in the main loop: {e}")
            traceback.print_exc()
            time.sleep(1) # Avoid rapid error loops

if __name__ == "__main__":
    run_agent()