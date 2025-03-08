# main.py
from scheduler import generate_schedule  # Import the function from scheduler.py

def main():
    schedule = generate_schedule()  # Call the function from scheduler.py
    print("Generated Schedule:")
    print(schedule)  # Print the generated schedule to the console

# Only run if this script is executed directly (not imported as a module)
if __name__ == "__main__":
    main()
