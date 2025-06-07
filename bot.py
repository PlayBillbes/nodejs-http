import streamlit as st
import subprocess
import os

def app():
    st.title("Folder Content Uploader & Shell Command Executor")
    st.write("This app allows you to upload multiple files from a folder and execute shell commands.")
    st.warning("⚠️ **SECURITY WARNING:** Executing arbitrary shell commands from a web application is highly dangerous and should be used with extreme caution, ideally only in a controlled, local environment. Do not deploy this with public access.")

    # --- File Uploader Section ---
    st.header("1. Folder Content Uploader (Multiple Files)")
    st.write("Due to browser security limitations, you cannot directly upload an entire folder. "
             "Instead, please select all the files you wish to upload from your chosen folder.")

    uploaded_files = st.file_uploader("Choose files from your folder", accept_multiple_files=True)

    if uploaded_files:
        st.subheader("Uploaded Files:")
        for uploaded_file in uploaded_files:
            st.write(f"- {uploaded_file.name} (Type: {uploaded_file.type}, Size: {uploaded_file.size} bytes)")

            save_path = "temp_uploads"
            os.makedirs(save_path, exist_ok=True)

            try:
                with open(os.path.join(save_path, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Saved '{uploaded_file.name}' to '{save_path}'")
            except Exception as e:
                st.error(f"Error saving '{uploaded_file.name}': {e}")

        st.success(f"Successfully uploaded {len(uploaded_files)} file(s).")
    else:
        st.info("Please upload files to see the details.")

    # --- Dependency Management Button ---
    st.header("2. Dependency Management")
    st.write("Click the button below to install dependencies from `requirements.txt`.")
    st.warning("Warning: Executing shell commands from a web app can have security implications. Use with caution.")

    if st.button("Install Dependencies (pip3 install -r requirements.txt)"):
        st.info("Attempting to install dependencies...")
        try:
            process = subprocess.run(
                ["pip3", "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True,
                check=True,
                shell=False # Explicitly set to False for security
            )
            st.success("Dependencies installed successfully!")
            st.code(process.stdout, language='bash')
            if process.stderr:
                st.warning("Warnings during installation:")
                st.code(process.stderr, language='bash')
        except subprocess.CalledProcessError as e:
            st.error(f"Error installing dependencies: {e}")
            st.code(e.stderr, language='bash')
        except FileNotFoundError:
            st.error("Error: 'pip3' command not found. Make sure Python and pip are in your PATH.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    # --- Shell Command Execution Box ---
    st.header("3. Execute Custom Shell Command")
    st.write("Enter a command to execute. The output will be displayed below.")
