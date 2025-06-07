import streamlit as st
import subprocess
import os

def app():
    st.title("Folder Content Uploader (Multiple Files)")
    st.write("This app allows you to upload multiple files from a folder.")
    st.write("Due to browser security limitations, you cannot directly upload an entire folder. "
             "Instead, please select all the files you wish to upload from your chosen folder.")

    uploaded_files = st.file_uploader("Choose files from your folder", accept_multiple_files=True)

    if uploaded_files:
        st.subheader("Uploaded Files:")
        for uploaded_file in uploaded_files:
            st.write(f"- {uploaded_file.name} (Type: {uploaded_file.type}, Size: {uploaded_file.size} bytes)")

            # Option to save the files (example: saving to a 'temp_uploads' directory)
            save_path = "temp_uploads"
            os.makedirs(save_path, exist_ok=True) # Create directory if it doesn't exist

            try:
                with open(os.path.join(save_path, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Saved '{uploaded_file.name}' to '{save_path}'")
            except Exception as e:
                st.error(f"Error saving '{uploaded_file.name}': {e}")

        st.success(f"Successfully uploaded {len(uploaded_files)} file(s).")
    else:
        st.info("Please upload files to see the details.")

    ---

    st.header("Dependency Management")
    st.write("Click the button below to install dependencies from `requirements.txt`.")
    st.warning("Warning: Executing shell commands from a web app can have security implications. Use with caution.")

    if st.button("Install Dependencies (pip3 install -r requirements.txt)"):
        st.info("Attempting to install dependencies...")
        try:
            # Use subprocess to run the pip command
            # capture_output=True to get stdout/stderr
            # text=True to decode output as text
            # check=True to raise an exception for non-zero exit codes (errors)
            process = subprocess.run(
                ["pip3", "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True,
                check=True
            )
            st.success("Dependencies installed successfully!")
            st.code(process.stdout) # Show successful output
            if process.stderr:
                st.warning("Warnings during installation:")
                st.code(process.stderr)
        except subprocess.CalledProcessError as e:
            st.error(f"Error installing dependencies: {e}")
            st.code(e.stderr) # Show error output
        except FileNotFoundError:
            st.error("Error: 'pip3' command not found. Make sure Python and pip are in your PATH.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    app()
