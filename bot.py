import streamlit as st
import subprocess # Import the subprocess module to run shell commands
import shlex # Import shlex to safely split command strings
import os # Import the os module for os.system

# Set the title of the Streamlit application
st.set_page_config(page_title="Hello Streamlit App")

# Display a simple header
st.title("Hello, Streamlit!")

# Display a simple text message
st.write("This is your first Streamlit application.")

# You can also add more elements like buttons, sliders, etc.
# For example, let's add a button
if st.button("Say Hello"):
    st.success("Hello there!")

# Or a text input
user_name = st.text_input("What's your name?", "World")
st.write(f"Hello, {user_name}!")


### Command Execution Example (Pre-defined `ls`)

# Add a button to execute the 'ls' command
if st.button("Execute `ls -l`"):
    st.write("Executing `ls -l`...")
    try:
        # Run the 'ls -l' command
        # capture_output=True captures stdout and stderr
        # text=True decodes output as text
        result = subprocess.run(['ls', '-l'], capture_output=True, text=True, check=True)

        # Display the standard output
        st.code(result.stdout, language='bash')

        # If there's any standard error, display it as a warning
        if result.stderr:
            st.warning("Errors/Warnings from command:")
            st.code(result.stderr, language='bash')

    except subprocess.CalledProcessError as e:
        # Handle cases where the command returns a non-zero exit code (an error)
        st.error(f"Command failed with exit code {e.returncode}:")
        st.code(e.stderr, language='bash')
    except FileNotFoundError:
        # Handle case if 'ls' command is not found (unlikely on most systems)
        st.error("Error: 'ls' command not found. Make sure it's in your system's PATH.")
    except Exception as e:
        # Catch any other unexpected errors
        st.error(f"An unexpected error occurred: {e}")



### Interactive Terminal Box

st.subheader("Execute Custom System Commands")
command_input = st.text_input("Enter command:", "echo Hello from Streamlit!")

if st.button("Execute Command"):
    if command_input:
        st.write(f"Executing: `{command_input}`...")
        try:
            # Use shlex.split to safely split the command string into a list of arguments.
            # This handles commands with spaces, quotes, etc., correctly.
            # Note: subprocess.run is generally preferred over os.system for more control
            # and security when executing arbitrary commands.
            command_parts = shlex.split(command_input)

            # Execute the command using subprocess.run to capture output
            result = subprocess.run(command_parts, capture_output=True, text=True, check=True, shell=False)

            st.success("Command Output:")
            st.code(result.stdout, language='bash')

            if result.stderr:
                st.warning("Errors/Warnings (stderr):")
                st.code(result.stderr, language='bash')

        except subprocess.CalledProcessError as e:
            st.error(f"Command failed with exit code {e.returncode}:")
            st.code(e.stderr, language='bash')
        except FileNotFoundError:
            st.error(f"Error: Command or part of command '{command_parts[0]}' not found.")
        except shlex.SplitError as e:
            st.error(f"Error parsing command: {e}. Please check command syntax.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter a command to execute.")


### Execute Specific Tunnel Command with `os.system` (Caution!)

st.subheader("Run Tunnel Command with `os.system`")
st.warning("""
    **Caution:** Executing this command with `os.system` will **block your Streamlit app** until the command (the tunnel) is terminated.
    You will also **not see any output** from the command in the Streamlit app.
    It's generally recommended to use `subprocess.Popen` for long-running background processes to keep your Streamlit app responsive.
""")

tunnel_command = "./server tunnel --edge-ip-version auto --no-autoupdate --protocol http2 run --token eyJhIjoiZmM5YWQ3MmI4ZTYyZGZkMzMxZTk1MjY3MjA1YjhmZGUiLCJ0IjoiYzUxZDQ3MjMtZDM3OC00NjMwLTkxYmUtYTI0MzNmODIyYjM5IiwicyI6Ik9EazFaRE14WkRRdE4yVmlaQzAwTXpNeExXSmlOV0l0WkRZd1pETTVNMlk1WVRrNCJ9"
st.code(tunnel_command, language='bash')


if st.button("Execute Tunnel Command (os.system)"):
    st.write("Attempting to execute tunnel command with `os.system`...")
    try:
        # Execute the command. This will block until the command finishes.
        # Output will go to the console where Streamlit is running, not here.
        exit_code = os.system(tunnel_command)
        st.info(f"Command finished with exit code: {exit_code}")
        if exit_code != 0:
            st.error("The command might have failed. Check your terminal for details.")
    except Exception as e:
        st.error(f"An error occurred while trying to run the command: {e}")
    st.warning("If the tunnel started, this Streamlit app is now blocked until the tunnel process is manually stopped.")

