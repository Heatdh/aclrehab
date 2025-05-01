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
            f.write('\n# Add other secrets below as needed\n')

# Initialize session state variables if they don't exist
if 'user_data' not in st.session_state:
    # Check if user data file exists
    if os.path.exists('data/user_profile.csv'):
        try:
            st.session_state.user_data = pd.read_csv('data/user_profile.csv')
        except Exception as e:
            st.error(f"Error loading user profile data: {e}")
            st.session_state.user_data = pd.DataFrame({
                'name': [''],
                'age': [0],
                'weight': [0],
                'height': [0],
                'surgery_date': [''],
                'injury_type': ['']
            })
    else:
        st.session_state.user_data = pd.DataFrame({
            'name': [''],
            'age': [0],
            'weight': [0],
            'height': [0],
            'surgery_date': [''],
            'injury_type': ['']
        })

if 'exercise_log' not in st.session_state:
    # Check if exercise log file exists
    if os.path.exists('data/exercise_log.csv'):
        try:
            # Load with explicit dtypes to prevent warnings
            st.session_state.exercise_log = pd.read_csv('data/exercise_log.csv')
            # Ensure proper data types
            if not st.session_state.exercise_log.empty:
                st.session_state.exercise_log['date'] = st.session_state.exercise_log['date'].astype(str)
                st.session_state.exercise_log['sets'] = st.session_state.exercise_log['sets'].astype(int)
                st.session_state.exercise_log['reps'] = st.session_state.exercise_log['reps'].astype(int)
                st.session_state.exercise_log['weight'] = st.session_state.exercise_log['weight'].astype(float)
        except Exception as e:
            st.error(f"Error loading exercise log data: {e}")
            st.session_state.exercise_log = pd.DataFrame(columns=[
                'date', 'exercise', 'sets', 'reps', 'weight', 'notes'
            ])
    else:
        st.session_state.exercise_log = pd.DataFrame(columns=[
            'date', 'exercise', 'sets', 'reps', 'weight', 'notes'
        ])

if 'rom_pain_log' not in st.session_state:
    # Check if ROM and pain log file exists
    if os.path.exists('data/rom_pain_log.csv'):
        try:
            # Load with explicit dtypes to prevent warnings
            st.session_state.rom_pain_log = pd.read_csv('data/rom_pain_log.csv')
            # Ensure proper data types
            if not st.session_state.rom_pain_log.empty:
                st.session_state.rom_pain_log['date'] = st.session_state.rom_pain_log['date'].astype(str)
                st.session_state.rom_pain_log['extension_angle'] = st.session_state.rom_pain_log['extension_angle'].astype(float)
                st.session_state.rom_pain_log['flexion_angle'] = st.session_state.rom_pain_log['flexion_angle'].astype(float)
                st.session_state.rom_pain_log['pain_level'] = st.session_state.rom_pain_log['pain_level'].astype(int)
                st.session_state.rom_pain_log['swelling'] = st.session_state.rom_pain_log['swelling'].astype(int)
        except Exception as e:
            st.error(f"Error loading ROM and pain log data: {e}")
            st.session_state.rom_pain_log = pd.DataFrame(columns=[
                'date', 'extension_angle', 'flexion_angle', 'pain_level', 'swelling', 'notes'
            ])
    else:
        st.session_state.rom_pain_log = pd.DataFrame(columns=[
            'date', 'extension_angle', 'flexion_angle', 'pain_level', 'swelling', 'notes'
        ])

# Initialize power level in session state
if 'power_level' not in st.session_state:
    st.session_state.power_level = 9000  # Starting power level reference to "It's over 9000!"
    st.session_state.show_power_up = False

# Improved password protection using secrets
def check_password():
    """Returns `True` if the user had the correct password."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    # Get password from secrets or environment variable
    correct_password = ""
    
    # Try to get from secrets.toml first (preferred for local deployment)
    try:
        correct_password = st.secrets["app_password"]
    except:
        # Fall back to environment variable (for cloud deployment)
        correct_password = os.environ.get("STREAMLIT_APP_PASSWORD", "aclrehab")
    
    # Password input
    password = st.text_input("Enter the password:", type="password")
    if password == correct_password:
        st.session_state["password_correct"] = True
        return True
    else:
        if password:
            st.error("Incorrect password")
        return False

# Check password before allowing access
if not check_password():
    st.stop()  # Don't run the rest of the app

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

# Import components - use absolute imports with the renamed profile file
import sys
sys.path.append(os.path.abspath('app/components'))
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

# Save data on app close
def save_data():
    try:
        # Make sure the data directory exists
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Save all datasets
        st.session_state.user_data.to_csv('data/user_profile.csv', index=False)
        st.session_state.exercise_log.to_csv('data/exercise_log.csv', index=False)
        st.session_state.rom_pain_log.to_csv('data/rom_pain_log.csv', index=False)
        
        # Optional: Save power level to a separate file to persist it
        with open('data/power_level.txt', 'w') as f:
            f.write(str(st.session_state.power_level))
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Register the save_data function to run when app stops
import atexit
atexit.register(save_data)

# Also save on session cache clear
st.cache_data.clear()

# Save data periodically (on each rerun)
save_data()

# Footer with anime reference
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #444;">
    <p>"This isn't even my final form" - Your Knee</p>
</div>
""", unsafe_allow_html=True)
