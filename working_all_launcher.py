import os
from pathlib import Path

LOCK_FILE = Path(r"C:\gh\oomlout_base\lock\working_all.lock")
QUEUE_FILE = Path(r"C:\gh\oomlout_base\lock\working_all_queue.bat")

#launch command with full directory to batch file
directory_current = Path(__file__).parent.resolve()
LAUNCH_CMD = f'call "{directory_current}\\run_working_all_launcher.bat"\n'

# Check for lock file
if LOCK_FILE.exists():
    print("working_all is already running. Queuing request...")
    # Read queue file if it exists
    queue_content = ""
    if QUEUE_FILE.exists():
        with QUEUE_FILE.open("r", encoding="utf-8") as f:
            queue_content = f.read()
    # Add launch command if not already present
    if LAUNCH_CMD.strip() not in queue_content:
        with QUEUE_FILE.open("a", encoding="utf-8") as f:
            f.write(LAUNCH_CMD)
        print("Added to queue.")
    else:
        print("Already in queue.")
else:
    print("No lock file found. Proceeding to run working all.")
    # Create lock file
    with LOCK_FILE.open("w", encoding="utf-8") as f:
        f.write("locked")
    #check if in queue if so remove it
    if QUEUE_FILE.exists():
        with QUEUE_FILE.open("r", encoding="utf-8") as f:
            queue_content = f.readlines()
        # Remove the all occurrences of the launch command and print a message when removed
        with QUEUE_FILE.open("w", encoding="utf-8") as f:
            for line in queue_content:
                if line.strip() != LAUNCH_CMD.strip():
                    f.write(line)
                else:
                    print("Removed from queue before running.")
    import working_all
    working_all.main()

    # Delete lock file before running the queue
    if LOCK_FILE.exists():
        LOCK_FILE.unlink()
        print("Lock file deleted.")

    # Run the queue file if it exists
    if QUEUE_FILE.exists():
        print("Running queue file...")
        os.system(f'start "Working All Queue" "{QUEUE_FILE}"')
    else:
        print("No queue file to run.")
