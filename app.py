import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import base64
from streamlit_option_menu import option_menu
from PIL import Image
import sys
sys.path.append(os.path.abspath('app/components'))
from db_utils import (
    authenticate_user, 
    create_user, 
    get_user_profile, 
    save_user_profile, 
    get_exercise_log,
    save_exercise_log,
    get_rom_pain_log,
    save_rom_pain_log,
    get_user_list
)

# Set page config
st.set_page_config(
    page_title="ACL Rehab Tracker",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    with open('app/styles.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css()
except:
    st.warning("Custom styling not loaded. Make sure app/styles.css exists.")

# Helper function for Super Saiyan transformation
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def power_up_animation():
    # Add Super Saiyan GIF or power-up animation effect via HTML
    power_up_html = """
    <div class="power-up-container">
        <div class="power-up-animation"></div>
        <img src="app/images/power_app_animation.gif" style="max-width: 300px; margin: 0 auto; display: block;">
        <h3 style="text-align:center; color:#ffcc00; text-shadow:0 0 10px #ffcc00;">POWER LEVEL INCREASED!</h3>
    </div>
    <style>
    .power-up-container {
        position: relative;
        width: 100%;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }
    .power-up-animation {
        position: absolute;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255,204,0,0.8) 0%, rgba(255,204,0,0) 70%);
        border-radius: 50%;
        animation: power-pulse 2s ease-out forwards;
        z-index: -1;
    }
    @keyframes power-pulse {
        0% {
            transform: scale(0.1);
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
        100% {
            transform: scale(3);
            opacity: 0;
        }
    }
    </style>
    """
    return power_up_html

# Create necessary data directories
if not os.path.exists('data'):
    os.makedirs('data')

# Create .streamlit directory if it doesn't exist 
if not os.path.exists('.streamlit'):
    os.makedirs('.streamlit')
    # Create a template secrets.toml file if it doesn't exist
    if not os.path.exists('.streamlit/secrets.toml'):
        with open('.streamlit/secrets.toml', 'w') as f:
            f.write('# .streamlit/secrets.toml\n\n')
            f.write('# Store your passwords or API keys here\n')
            f.write('app_password = "aclrehab"\n')
            f.write('\n# Add MongoDB connection string\n')
            f.write('mongo_uri = "mongodb://localhost:27017"\n')
            f.write('\n# Add other secrets below as needed\n')

# Initialize session state variables if they don't exist
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_username' not in st.session_state:
    st.session_state.current_username = None

if 'power_level' not in st.session_state:
    st.session_state.power_level = 9000  # Starting power level reference to "It's over 9000!"
    st.session_state.show_power_up = False

# Initialize data in session state
if 'user_data' not in st.session_state and st.session_state.current_username:
    st.session_state.user_data = get_user_profile(st.session_state.current_username)

if 'exercise_log' not in st.session_state and st.session_state.current_username:
    st.session_state.exercise_log = get_exercise_log(st.session_state.current_username)

if 'rom_pain_log' not in st.session_state and st.session_state.current_username:
    st.session_state.rom_pain_log = get_rom_pain_log(st.session_state.current_username)

# Authentication function
def login_form():
    st.title("ACL Rehab Tracker - Login")
    
    # Login/Register tabs
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Use Existing Profile"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                success, result = authenticate_user(username, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.current_username = username
                    
                    # Initialize/load user data
                    st.session_state.user_data = get_user_profile(username)
                    st.session_state.exercise_log = get_exercise_log(username)
                    st.session_state.rom_pain_log = get_rom_pain_log(username)
                    
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error(result)
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            email = st.text_input("Email (optional)")
            
            submitted = st.form_submit_button("Register")
            
            if submitted:
                if not new_username or not new_password:
                    st.error("Username and password are required.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = create_user(new_username, new_password, email)
                    if success:
                        st.success(f"{message} You can now log in.")
                    else:
                        st.error(message)
    
    with tab3:
        # Get list of existing users
        users = get_user_list()
        if users:
            with st.form("select_profile_form"):
                # Create a dictionary of username:name for display
                user_options = {}
                for user in users:
                    display_name = f"{user['name']} ({user['username']})" if user['name'] else user['username']
                    user_options[user['username']] = display_name
                
                selected_username = st.selectbox("Select Profile", 
                                              options=list(user_options.keys()),
                                              format_func=lambda x: user_options[x])
                
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                
                if submitted:
                    success, result = authenticate_user(selected_username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.current_username = selected_username
                        
                        # Initialize/load user data
                        st.session_state.user_data = get_user_profile(selected_username)
                        st.session_state.exercise_log = get_exercise_log(selected_username)
                        st.session_state.rom_pain_log = get_rom_pain_log(selected_username)
                        
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error(result)
        else:
            st.info("No existing profiles found. Please register a new account.")

# Main app function
def main_app():
    # App navigation
    selected = option_menu(
        menu_title=None,
        options=["Profile", "Rehab Plan", "Equipment Exercises", "Exercise Tracker", "ROM & Pain", "Progress Dashboard"],
        icons=["person-circle", "journal-check", "tools", "activity", "thermometer-half", "graph-up"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )

    # App title with anime theme
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>SUPER SAIYAN ACL REHAB</h1>
        <p style="font-style: italic; color: #aaa;">Beyond your limiter... Plus Ultra Recovery!</p>
    </div>
    """, unsafe_allow_html=True)

    # Show current user
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.current_username}")
    if st.sidebar.button("Logout"):
        # Clear session state
        st.session_state.authenticated = False
        st.session_state.current_username = None
        st.session_state.user_data = None
        st.session_state.exercise_log = None
        st.session_state.rom_pain_log = None
        st.rerun()

    # Power level display
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.session_state.power_level > 0:
            st.markdown(f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <h4>POWER LEVEL: {st.session_state.power_level:,}</h4>
                <div style="background-color: rgba(0,0,0,0.3); border-radius: 10px; height: 30px; width: 100%; margin-top: 10px;">
                    <div style="background-image: linear-gradient(90deg, #ff4500, #ffcc00, #fff700); 
                              width: {min(100, st.session_state.power_level/100)}%; 
                              height: 100%; 
                              border-radius: 10px;
                              transition: width 1s ease-in-out;">
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show power-up animation if triggered
        if st.session_state.show_power_up:
            st.markdown(power_up_animation(), unsafe_allow_html=True)
            st.session_state.show_power_up = False

    # Import components
    from user_profile import show_profile
    from exercise_tracker import show_exercise_tracker
    from rom_pain import show_rom_pain
    from dashboard import show_dashboard
    from rehab_plan import show_rehab_plan
    from equipment_exercises import show_equipment_exercises

    # Show selected page
    if selected == "Profile":
        show_profile()
    elif selected == "Rehab Plan":
        show_rehab_plan()
    elif selected == "Equipment Exercises":
        show_equipment_exercises()
    elif selected == "Exercise Tracker":
        show_exercise_tracker()
    elif selected == "ROM & Pain":
        show_rom_pain()
    elif selected == "Progress Dashboard":
        show_dashboard()

    # Footer with anime reference
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #444;">
        <p>"This isn't even my final form" - Your Knee</p>
    </div>
    """, unsafe_allow_html=True)

# Save data function
def save_data():
    if st.session_state.current_username:
        try:
            # Save user data to MongoDB
            if 'user_data' in st.session_state and st.session_state.user_data is not None:
                save_user_profile(st.session_state.current_username, st.session_state.user_data)
            
            # Save exercise log to MongoDB
            if 'exercise_log' in st.session_state and st.session_state.exercise_log is not None:
                save_exercise_log(st.session_state.current_username, st.session_state.exercise_log)
            
            # Save ROM and pain log to MongoDB
            if 'rom_pain_log' in st.session_state and st.session_state.rom_pain_log is not None:
                save_rom_pain_log(st.session_state.current_username, st.session_state.rom_pain_log)
            
            # Save power level to session state only (not in MongoDB yet)
            st.session_state.power_level = st.session_state.get('power_level', 9000)
        except Exception as e:
            st.error(f"Error saving data: {e}")

# Run the app
if st.session_state.authenticated:
    main_app()
else:
    login_form()

# Register the save_data function to run when app stops
import atexit
atexit.register(save_data)

# Also save on session cache clear
st.cache_data.clear()

# Save data periodically (on each rerun)
if st.session_state.authenticated:
    save_data()
