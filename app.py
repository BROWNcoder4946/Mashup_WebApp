import streamlit as st
from mymashup import main
import zipfile
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64
import os
os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg"

def send_email(attachment_path, to_email , singer):
    # Set your email and password
    email = "avashishta_be21@thapar.edu"
    password = "zxkz bifc ravy bqam"

    # Create the MIME object
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = to_email
    message['Subject'] = f"Mashup: {singer}"

    # Attach the zip file
    with open(attachment_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=f"{attachment_path}")
        part['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
        message.attach(part)

    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email, password)
        server.sendmail(email, to_email, message.as_string())

def main_2():
    st.title("Let's Mashup")
    st.subheader("Create Mashups from your favorite singer's most famous songs :)")

    singer = st.text_input("Enter Singer's Name:")
    nov = st.number_input("Enter number of videos to extract:", min_value=1)
    nos = st.number_input("Enter number of seconds of audio to extract from each song:", min_value=10)
    #output_file = st.text_input("Enter output file name:")
    user_email = st.text_input("Enter your email:")

    output_file = "final.mp3"

    if st.button("Process Audio"):
        try:
            main(singer, nov, nos * 1000, output_file)
            st.success(f'The final audio file {output_file} has been created successfully.')

            # Create a zip file
            zip_file_name = f"{output_file}.zip"
            with zipfile.ZipFile(zip_file_name, 'w') as zip_file:
                zip_file.write(output_file)

            # Send the zip file via email
            send_email(zip_file_name , user_email , singer)
            st.success(f'Mashup file has been sent to {user_email}')

        except Exception as e:
            st.error(f'An error occurred: {e}')

if __name__ == "__main__":
    main_2()
