"""
Smart Study Planner
A console-based Python programme that helps me to log, review and
analyse my study sessions across different subjects over the course
of a semester. Session data is saved to and reloaded from a text file
(study_log.txt) so that the programme keeps working correctly across
multiple runs.
"""
import os

DATA_FILE = "study_log.txt"


# (c) classify_session()

def classify_session(duration):
    """
    Classify a study session based on its duration in minutes.

    Short  : under 30 minutes
    Medium : 30 to 90 minutes (inclusive)
    Long   : over 90 minutes
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"

# (b) add_session()
def add_session(sessions):
    """
    Prompt the user for the details of a new study session and append
    it to the sessions list as a dictionary. The duration is validated
    to ensure it is a positive number, re-prompting on invalid input.
    """
    print("\n--- Add a Study Session ---")
    subject = input("Enter subject name: ").strip()
    while subject == "":
        subject = input("Subject name cannot be empty. Enter subject name: ").strip()

    topic = input("Enter topic covered: ").strip()
    while topic == "":
        topic = input("Topic cannot be empty. Enter topic covered: ").strip()

    date = input("Enter date or day label (e.g., 2026-09-03 or Monday): ").strip()
    while date == "":
        date = input("Date/day label cannot be empty. Enter date or day label: ").strip()

    # Validate duration: must be a positive number, re-prompt until valid
    duration = None
    while duration is None:
        raw_duration = input("Enter duration of session in minutes: ").strip()
        try:
            value = float(raw_duration)
            if value <= 0:
                print("Duration must be a positive number. Please try again.")
                continue
            # Store as int if it's a whole number, otherwise keep decimal
            duration = int(value) if value.is_integer() else value
        except ValueError:
            print("Invalid input. Please enter a numeric value for duration.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    }
    sessions.append(session)
    print(f"Session added: {subject} ({classify_session(duration)}, {duration} min)\n")



# (d) view_sessions()

def view_sessions(sessions):
    """
    Display every logged session in a neatly formatted table, showing
    the subject, topic, date, duration, and its Short/Medium/Long
    classification.
    """
    print("\n--- All Study Sessions ---")
    if not sessions:
        print("No sessions have been logged yet.\n")
        return

    _print_session_table(sessions)
    print()


def _print_session_table(sessions):
    """Helper that prints a list of sessions as a formatted table."""
    header = f"{'#':<4}{'Subject':<18}{'Topic':<22}{'Date':<15}{'Duration (min)':<16}{'Type':<8}"
    print(header)
    print("-" * len(header))
    for i, s in enumerate(sessions, start=1):
        classification = classify_session(s["duration"])
        row = (
            f"{i:<4}{s['subject']:<18}{s['topic']:<22}"
            f"{s['date']:<15}{s['duration']:<16}{classification:<8}"
        )
        print(row)


# (e) search_by_subject()

def search_by_subject(sessions):
    """
    Let the user type a subject name (case-insensitive match) and
    display only the sessions recorded for that subject, along with
    the total time spent on it. Shows a clear message if none found.
    """
    print("\n--- Search Sessions by Subject ---")
    if not sessions:
        print("No sessions have been logged yet.\n")
        return

    query = input("Enter subject name to search for: ").strip().lower()
    matches = [s for s in sessions if s["subject"].strip().lower() == query]

    if not matches:
        print(f"No sessions found for subject '{query}'.\n")
        return

    _print_session_table(matches)
    total_minutes = sum(s["duration"] for s in matches)
    print(f"\nTotal time spent on '{matches[0]['subject']}': "
          f"{total_minutes} minutes ({total_minutes / 60:.2f} hours)\n")

# (f) study_statistics()

def study_statistics(sessions):
    """
    Compute and display:
      - total hours studied overall
      - total hours studied per subject
      - the subject with the least total study time (weakest area)
      - the single longest session recorded
    """
    print("\n--- Study Statistics ---")
    if not sessions:
        print("No sessions have been logged yet.\n")
        return

    # Total hours overall
    total_minutes = sum(s["duration"] for s in sessions)
    print(f"Total time studied overall: {total_minutes} minutes "
          f"({total_minutes / 60:.2f} hours)\n")

    # Total hours per subject
    subject_totals = {}
    for s in sessions:
        subject_totals[s["subject"]] = subject_totals.get(s["subject"], 0) + s["duration"]

    print("Time studied per subject:")
    for subject, minutes in subject_totals.items():
        print(f"  {subject:<18} {minutes:>6} min  ({minutes / 60:.2f} hours)")

    # Weakest area: subject with least total study time
    weakest_subject = min(subject_totals, key=subject_totals.get)
    print(f"\nWeakest area (least total study time): {weakest_subject} "
          f"({subject_totals[weakest_subject]} min)")

    # Longest single session
    longest = max(sessions, key=lambda s: s["duration"])
    print(f"Longest single session: {longest['subject']} - {longest['topic']} "
          f"({longest['duration']} min, {classify_session(longest['duration'])})\n")

# (g) save_sessions() and load_sessions()

def save_sessions(sessions):
    """
    Save every logged session to study_log.txt. Each session is stored
    on its own line using '|' as a field separator so it can be easily
    parsed back on the next run.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for s in sessions:
            line = f"{s['subject']}|{s['topic']}|{s['date']}|{s['duration']}\n"
            f.write(line)
    print(f"Sessions saved to {DATA_FILE}. Goodbye!")


def load_sessions():
    """
    Load sessions from study_log.txt if it exists. Returns an empty
    list if the file is missing or a line is malformed, so the
    programme never crashes on startup (e.g., on the very first run).
    """
    sessions = []
    if not os.path.exists(DATA_FILE):
        return sessions

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 4:
                # Skip malformed lines rather than crashing
                continue
            subject, topic, date, duration_str = parts
            try:
                duration = float(duration_str)
                duration = int(duration) if duration.is_integer() else duration
            except ValueError:
                continue
            sessions.append({
                "subject": subject,
                "topic": topic,
                "date": date,
                "duration": duration,
            })
    return sessions

# (a) main() - menu-driven interface

def display_menu():
    """Print the main menu options."""
    print("=" * 40)
    print("        SMART STUDY PLANNER")
    print("=" * 40)
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("=" * 40)


def main():
    """Main programme loop: displays the menu and routes user choices."""
    sessions = load_sessions()

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.\n")


if __name__ == "__main__":
    main()
