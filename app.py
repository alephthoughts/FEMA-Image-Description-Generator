import streamlit as st
import pandas as pd
from backend import process_images
from io import BytesIO

st.title("FEMA Image Description Generator")

api_key = st.text_input("Enter your OpenAI API key:", type="password")
folder_path = st.text_input("Enter the folder path containing images:")

if api_key and folder_path:
    if st.button("Process Images"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(progress, status):
            progress_bar.progress(progress)
            status_text.text(status)

        try:
            df = process_images(api_key, folder_path, update_progress)

            excel_file = BytesIO()
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Image Descriptions')
            
            st.download_button(
                label="Download Excel file",
                data=excel_file.getvalue(),
                file_name="fema_image_descriptions.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success("Processing complete! You can now download the Excel file.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.markdown("This app processes images in a specified folder, generates descriptions for FEMA using OpenAI's GPT-4 Vision model, and provides an Excel file with the results.")
