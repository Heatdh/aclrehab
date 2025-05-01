# Local Deployment Guide with Remote Access

This guide will help you run your ACL rehab app locally and access it remotely when needed.

## Part 1: Local Setup

### Prerequisites
- Python installed on your computer
- Your Streamlit app code
- Terminal/Command Prompt access

### Steps for Local Deployment

1. **Install Required Packages**
   
   Open a terminal/command prompt and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create Necessary Data Directories**
   
   Add this code at the beginning of your `app.py` file to ensure data directories exist:
   ```python
   import os
   if not os.path.exists('data'):
       os.makedirs('data')
   ```

3. **Run the App Locally**
   
   ```bash
   streamlit run app.py
   ```
   
   This will start your app and open it in your default browser at `http://localhost:8501`

4. **Keep the App Running**
   
   As long as your terminal/command prompt window stays open, your app will continue running

## Part 2: Remote Access with Ngrok

When you want to access your app from another device or share it temporarily:

### One-Time Setup

1. **Create a Free Ngrok Account**
   
   Go to [ngrok.com](https://ngrok.com/) and sign up for a free account

2. **Install Ngrok**
   
   ```bash
   pip install pyngrok
   ```

3. **Get Your Auth Token**
   
   After signing up, get your auth token from the ngrok dashboard

4. **Configure Ngrok**
   
   Run this once to authenticate:
   ```bash
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

### Accessing Remotely (When Needed)

1. **Make Sure Your App is Running**
   
   Your Streamlit app should be running locally (`streamlit run app.py`)

2. **Start Ngrok Tunnel in a New Terminal Window**
   
   ```bash
   ngrok http 8501
   ```

3. **Get Your Temporary URL**
   
   Ngrok will display a forwarding URL like `https://a1b2c3d4.ngrok.io`
   
   ![Ngrok URL example](https://ngrok.com/static/img/docs/ngrok_url_forwarding_to_port.png)

4. **Access Your App**
   
   Use this URL to access your app from any device with internet access
   
   The URL is temporary and will change each time you restart ngrok

5. **End Remote Access**
   
   When you're done with remote access, simply press `Ctrl+C` in the ngrok terminal window
   Your app will still be running locally

## Notes and Limitations

1. **Free Tier Limitations**
   - Ngrok free tier provides 1 concurrent tunnel
   - Sessions expire after 2 hours (just restart ngrok to get a new URL)
   - 40 connections per minute

2. **Security Considerations**
   - Anyone with the ngrok URL can access your app during the session
   - For added security, add password protection to your app:

   ```python
   # Add this to the beginning of your app.py
   import streamlit as st

   def check_password():
       """Returns `True` if the user had the correct password."""
       if "password_correct" not in st.session_state:
           st.session_state["password_correct"] = False

       if st.session_state["password_correct"]:
           return True

       password = st.text_input("Enter the password:", type="password")
       if password == "your-secret-password":  # Replace with your chosen password
           st.session_state["password_correct"] = True
           return True
       else:
           if password:
               st.error("Incorrect password")
           return False

   if not check_password():
       st.stop()  # Don't run the rest of the app
   ```

3. **Data Management**
   - All data is stored locally on your computer
   - This method provides excellent privacy for your health data
   - Consider regular backups of your data folder

4. **Keeping Your Computer Running**
   - Your computer needs to be on and the app running for remote access
   - For Windows, consider using the Task Scheduler to auto-start the app 