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
    get_user_list,
    init_connection
)

# Set page config
st.set_page_config(
    page_title="ACL Rehab Tracker",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check MongoDB connection early
mongodb_connected = init_connection() is not None
if not mongodb_connected:
    st.warning("⚠️ Not connected to MongoDB. Using local file storage as fallback.")
else:
    st.success("✅ Connected to MongoDB successfully!")

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
    # Add modern fitness-themed animation via HTML
    power_up_html = """
    <div class="power-up-container">
        <div class="power-up-animation"></div>
        <img src="data:image/gif;base64,{0}" style="max-width: 300px; margin: 0 auto; display: block; border-radius: 12px; box-shadow: 0 10px 30px rgba(54, 209, 220, 0.4);">
        <h3 style="text-align:center; color:#36d1dc; text-shadow:0 0 10px #36d1dc;">POWER LEVEL INCREASED!</h3>
    </div>
    <style>
    .power-up-container {{
        position: relative;
        width: 100%;
        height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        overflow: hidden;
        margin: 20px 0;
    }}
    .power-up-animation {{
        position: absolute;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(54, 209, 220, 0.8) 0%, rgba(91, 134, 229, 0) 70%);
        border-radius: 50%;
        animation: power-pulse 2s ease-out forwards;
        z-index: -1;
    }}
    @keyframes power-pulse {{
        0% {{
            transform: scale(0.1);
            opacity: 0;
        }}
        50% {{
            opacity: 1;
        }}
        100% {{
            transform: scale(3);
            opacity: 0;
        }}
    }}
    </style>
    """
    
    # Try to load the GIF file and convert to base64
    try:
        gif_base64 = get_base64_of_bin_file("app/images/power_app_animation.gif")
        return power_up_html.format(gif_base64)
    except Exception as e:
        # If file load fails, return the HTML without the image
        return power_up_html.format("")

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

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_username' not in st.session_state:
    st.session_state.current_username = None
if 'power_level' not in st.session_state:
    st.session_state.power_level = 0
if 'show_power_up' not in st.session_state:
    st.session_state.show_power_up = False
if 'rom_pain_log' not in st.session_state:
    st.session_state.rom_pain_log = pd.DataFrame()
if 'exercise_log' not in st.session_state:
    st.session_state.exercise_log = pd.DataFrame()
if 'user_data' not in st.session_state:
    st.session_state.user_data = pd.DataFrame()

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
        styles={
            "container": {"padding": "0!important", "background-color": "rgba(25, 30, 40, 0.3)", "border-radius": "10px"},
            "icon": {"color": "rgba(255, 255, 255, 0.7)", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "center", "margin":"0px", "padding": "10px", "border-radius": "5px"},
            "nav-link-selected": {"background-color": "rgba(54, 209, 220, 0.2)", "color": "#36d1dc", "font-weight": "600"},
        }
    )

    # App title with modern theme
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1>ACL REHABILITATION TRACKER</h1>
        <p style="font-style: italic; color: #aaa; letter-spacing: 1px;">Beyond Limits: Achieve Your Ultimate Recovery</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards on first page visit
    if 'last_page' not in st.session_state:
        st.session_state.last_page = None
    
    if st.session_state.last_page != selected:
        # Create visual feature cards for the first visit to a page
        if selected in ["Profile", "Rehab Plan", "Equipment Exercises", "Exercise Tracker", "ROM & Pain", "Progress Dashboard"]:
            # Feature highlights
            features = {
                "Profile": {
                    "icon": "person-circle",
                    "title": "User Profile",
                    "description": "Manage your personal details, surgery information, and recovery goals.",
                    "color": "#36d1dc"
                },
                "Rehab Plan": {
                    "icon": "journal-check",
                    "title": "Rehabilitation Plan",
                    "description": "Follow a structured phase-by-phase recovery protocol tailored for ACL recovery.",
                    "color": "#5b86e5"
                },
                "Equipment Exercises": {
                    "icon": "tools",
                    "title": "Exercise Database",
                    "description": "Browse exercises by category with detailed instructions for proper form.",
                    "color": "#41c7b9"
                },
                "Exercise Tracker": {
                    "icon": "activity",
                    "title": "Exercise Logger",
                    "description": "Track your workouts with sets, reps, and weights to monitor your progress.",
                    "color": "#4d8af0"
                },
                "ROM & Pain": {
                    "icon": "thermometer-half",
                    "title": "ROM & Pain Tracker",
                    "description": "Monitor your range of motion and track pain levels throughout recovery.",
                    "color": "#5c9ce6"
                },
                "Progress Dashboard": {
                    "icon": "graph-up",
                    "title": "Analytics Dashboard",
                    "description": "Visualize your recovery metrics and see your progress over time.",
                    "color": "#6e94f2"
                }
            }
            
            feature = features[selected]
            
            # Display feature card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {feature['color']}22, {feature['color']}11); 
                        border-radius: 16px; 
                        padding: 20px; 
                        margin-bottom: 30px;
                        border-left: 5px solid {feature['color']};
                        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                        backdrop-filter: blur(5px);
                        -webkit-backdrop-filter: blur(5px);">
                <div style="display: flex; align-items: center;">
                    <i class="bi bi-{feature['icon']}" style="font-size: 40px; color: {feature['color']}; margin-right: 20px;"></i>
                    <div>
                        <h2 style="margin: 0; color: {feature['color']};">{feature['title']}</h2>
                        <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.8);">{feature['description']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Update last page
    st.session_state.last_page = selected

    # Show current user in a nicer format
    st.sidebar.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
    <div class="fitness-card" style="padding: 15px; margin-bottom: 20px;">
        <div style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">LOGGED IN AS</div>
        <div style="font-size: 1.2rem; font-weight: 600; color: #36d1dc; margin-top: 5px;">{}</div>
    </div>
    """.format(st.session_state.current_username), unsafe_allow_html=True)
    
    if st.sidebar.button("Logout"):
        # Clear session state
        st.session_state.authenticated = False
        st.session_state.current_username = None
        st.session_state.user_data = None
        st.session_state.exercise_log = None
        st.session_state.rom_pain_log = None
        st.rerun()

    # Power level display with modern styling
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.session_state.power_level > 0:
            st.markdown(f"""
            <div class="metric-container" style="text-align: center; margin-bottom: 20px;">
                <div class="metric-label">POWER LEVEL</div>
                <div class="metric-value">{st.session_state.power_level:,}</div>
                <div style="background-color: rgba(25, 30, 40, 0.5); border-radius: 50px; height: 10px; width: 100%; margin-top: 10px; overflow: hidden;">
                    <div style="background-image: linear-gradient(90deg, #36d1dc, #5b86e5); 
                              width: {min(100, st.session_state.power_level/100)}%; 
                              height: 100%; 
                              border-radius: 50px;
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

    # Footer with modern styling
    st.markdown("""
    <div style="text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="color: rgba(255, 255, 255, 0.5);">Stay consistent. Every day is progress. 💪</p>
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
