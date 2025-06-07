import streamlit as st
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
            # You would need to create this directory in your app's root or desired location
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

if __name__ == "__main__":
    app()
