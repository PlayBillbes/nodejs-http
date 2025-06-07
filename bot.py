import streamlit as st
import subprocess # Import the subprocess module to run shell commands

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



### Command Execution Example

# Add a button to execute the 'ls' command
if st.button("Execute `ls`"):
    st.write("Executing `ls -l`...")
    try:
        # Run the 'ls -l' command
        # capture_output=True captures stdout and stderr
        # text=True decodes output as text
        result = subprocess.run(['curl'], capture_output=True, text=True, check=True)

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
