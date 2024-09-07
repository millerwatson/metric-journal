import os
import datetime

def load_settings():
    settings_file = open("settings.json", "r")
    settings = json.load(settings_file)
    settings_file.close()
    return settings

def setup_directory():
    os.mkdir("/entries")
    os.mkdir("/settings")

    name = input("What is your name? ")
    start_date = datetime.datetime.now().strftime("%d-%m-%Y")

    settings_dict = {
        "name": name,
        "start_date": start_date,
    }

    json_output = json.dumps(settings_dict, indent=4, sort_keys=True)

    with open("settings.json", "w") as settings_file:
        settings_file.write(json_output)

def main():
    used_before = input("Have you used this journal before? Y or N: ")
    if (used_before == "Y"):
        print("Great! Fetching your previous data...")

    else:
        print("First time for everything! I'll set up your directory for you.")
        setup_directory()
        print("Your directory has been set up.")

    what_to_do = input("What would you like to do?\n"
                       "1. Add a new entry\n"
                       "2. View/Update an entry\n")

    if (what_to_do == "1"):
        entry = input("Write your entry down.")



main()