import os
from datetime import datetime
import argparse


# Check if the directory is a late submit
def check_late_submit(directory, deadline):
    # Check by the name of the directory
    name = directory.split("/")[-1]
    # name format: "LabX_pbxxxxxxxx_尝试_YYYY-MM-DD-HH-MM-SS.txt"

    # Extract the timestamp from the directory name
    try:
        timestamp_str = name.split("_")[3].split(".")[0]
        submit_time = datetime.strptime(timestamp_str, "%Y-%m-%d-%H-%M-%S")
    except (IndexError, ValueError) as e:
        print(f"Error parsing timestamp from directory name: {e}")
        return False

    # Compare the submit time with the deadline
    if submit_time > deadline:
        return True
    else:
        return False


# Find all late submits in the directory
def find_late_submits(directory, deadline):
    # List all directories in the directory
    dirs = os.listdir(directory)
    # Check only .txt files
    dirs = [d for d in dirs if d.endswith(".txt")]
    # Filter the directories that are late submits
    late_submits = [d for d in dirs if check_late_submit(d, deadline)]
    not_late_submits = [d for d in dirs if not check_late_submit(d, deadline)]
    # Find the students who have submitted the lab, but submitted again after the deadline
    both_submits = []
    for late_submit in late_submits:
        for not_late_submit in not_late_submits:
            if late_submit.split("_")[1] == not_late_submit.split("_")[1]:
                both_submits.append(late_submit)
                break

    return late_submits, both_submits


if __name__ == "__main__":
    # Set the deadline
    deadline = {
        "Lab1": datetime(2024, 10, 28, 4, 0, 0),
        "Lab2": datetime(2024, 11, 4, 4, 0, 0),
        "Lab3": datetime(2024, 12, 2, 4, 0, 0),
        "Lab4": datetime(2024, 12, 23, 4, 0, 0),
        "Lab5": datetime(2024, 12, 30, 4, 0, 0),
        "Lab6": datetime(2025, 1, 7, 4, 0, 0),
        "Lab7": datetime(2025, 1, 18, 4, 0, 0),
    }

    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    # -l, --lab: the lab number
    parser.add_argument("-l", "--lab", type=str, help="Lab number")
    # -d, --directory: the directory containing the submits
    parser.add_argument("-d", "--directory", type=str, help="Directory containing the submits")
    args = parser.parse_args()

    # Check if the lab number is valid
    lab = args.lab
    if lab not in deadline:
        print("Invalid lab number")
        exit()

    # Check if the directory is valid
    directory = args.directory
    if not os.path.isdir(directory):
        print("Invalid directory path")
        exit()

    # Find the late submits
    late_submits, both_submits = find_late_submits(directory, deadline[lab])
    print("Late submits:")
    for submit in late_submits:
        if submit not in both_submits:
            # red
            print("\033[31m" + submit + "\033[0m")
        else:
            print(submit)
    print("\nBoth submits:")
    for submit in both_submits:
        print(submit)
