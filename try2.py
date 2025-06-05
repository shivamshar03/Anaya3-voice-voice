# main_program.py
import subprocess
import sys

def run_external_script(script_path, *args):
    """
    Runs an external Python script using subprocess.
    Args:
        script_path (str): The path to the Python script to run.
        *args: Any additional arguments to pass to the script.
    """
    try:
        # Use sys.executable to ensure the same Python interpreter is used
        command = [sys.executable, script_path] + list(args)
        print(f"Running command: {' '.join(command)}")

        # Run the script and capture its output
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        print("\n--- Output from external script ---")
        print(result.stdout)
        if result.stderr:
            print("--- Errors from external script ---")
            print(result.stderr)
        print("--- End of external script output ---\n")

        print(f"External script exited with code: {result.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"Error running script: {e}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print(f"Error: Script not found at {script_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    code_to_run = input("Enter the Python code to run: ")
    # Create the external script file for demonstration
    with open("my_script.py", "w") as f:
        f.write(code_to_run)
    print("Created 'my_script.py'")

    # Run the script without arguments
    print("\nAttempting to run my_script.py without arguments:")
    run_external_script("my_script.py")

    # Run the script with arguments
    print("\nAttempting to run my_script.py with arguments 'arg1' and 'arg2':")
    run_external_script("my_script.py", "arg1", "arg2")

    # Clean up the created script (optional)
    import os
    if os.path.exists("my_script.py"):
        os.remove("my_script.py")
        print("\nRemoved 'my_script.py'")