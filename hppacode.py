import streamlit as st
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import datetime

# Function to authenticate and create a PyDrive client
def create_drive_client():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # This will open a browser for authentication
    return GoogleDrive(gauth)

# Function to find the user in the Excel sheet
def find_user_in_excel(reg_number, dob, excel_file_path):
    df = pd.read_excel(excel_file_path)
    # Assuming the Excel sheet has 'Registration Number' and 'DOB' columns
    df['DOB'] = pd.to_datetime(df['DOB']).dt.strftime('%m-%d-%Y')
    input_dob = dob.strftime('%m-%d-%Y')
    
    user_row = df[(df['Registration Number'] == reg_number) & (df['DOB'] == input_dob)]
    
    if not user_row.empty:
        return True
    else:
        return False

# Function to find the PDF file in Google Drive
def find_file_in_drive(drive, reg_number):
    file_list = drive.ListFile({'q': f"title contains '{reg_number}.pdf'"}).GetList()
    for file in file_list:
        if file['title'] == f"{reg_number}.pdf":
            return file['webContentLink']
    return None

# Streamlit app
def main():
    st.title("Admit Card Download Portal")
    
    reg_number = st.text_input("Enter your Registration Number")
    dob = st.date_input("Enter your Date of Birth", min_value=datetime.date(1900, 1, 1))
    
    if st.button("Find Admit Card"):
        if not reg_number or not dob:
            st.error("Please enter both Registration Number and Date of Birth")
        else:
            # Connect to Google Drive
            drive = create_drive_client()
            
            # Path to your Excel file
            excel_file_path = '/Untitled spreadsheet.xlsx'
            
            if find_user_in_excel(reg_number, dob, excel_file_path):
                file_url = find_file_in_drive(drive, reg_number)
                
                if file_url:
                    st.success(f"Admit Card found! [Download here]({file_url})")
                else:
                    st.error("Admit Card not found in Google Drive.")
            else:
                st.error("User not found in the Excel sheet.")
                
if __name__ == "__main__":
    main()
