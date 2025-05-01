import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

def show_dashboard():
    # Helper functions for status text
    def get_rehab_phase(days):
        if days < 0:
            return "Pre-Op - Preparation"
        elif days < 7:
            return "Phase 0 - Early Motion"
        elif days < 21:
            return "Phase 1 - Initial Recovery"
        elif days < 42:
            return "Phase 2 - Progressive Loading"
        elif days < 90:
            return "Phase 3 - Strength Building"
        elif days < 180:
            return "Phase 4 - Power Development"
        else:
            return "Phase 5 - Return to Sport"
    
    def get_rom_status(extension, flexion):
        if extension <= 0 and flexion >= 135:
            return "Super Saiyan ROM Achieved!"
        elif extension <= 0 and flexion >= 120:
            return "Excellent ROM - Keep it up!"
        elif extension <= 5 and flexion >= 110:
            return "Good ROM - Getting stronger!"
        else:
            return "Continue your ROM training!"
    
    def get_pain_status(pain):
        if pain <= 1:
            return "Ultra Instinct Level Pain Control!"
        elif pain <= 3:
            return "Well-controlled - Great job!"
        elif pain <= 5:
            return "Moderate - Stay focused!"
        else:
            return "High - Review pain management!"
    
    st.title("Progress Dashboard")
    
    # Check if there's data to display
    if (st.session_state.rom_pain_log.empty and 
        st.session_state.exercise_log.empty):
        
        st.markdown("""
        <div style="text-align: center; padding: 30px; background-color: rgba(0,0,0,0.2); border-radius: 10px; margin: 20px 0;">
            <h3 style="color: #ffcc00;">No Training Data Yet!</h3>
            <p>Start tracking your exercises, ROM, and pain levels to unlock your power potential!</p>
            <div style="width: 100px; height: 100px; margin: 20px auto; border-radius: 50%; background: radial-gradient(circle, rgba(255,204,0,0.3) 0%, rgba(255,204,0,0) 70%); animation: pulse 2s infinite;">
            </div>
        </div>
        <style>
        @keyframes pulse {
            0% { transform: scale(0.8); opacity: 0.7; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.8); opacity: 0.7; }
        }
        </style>
        """, unsafe_allow_html=True)
        return
    
    # Get user information
    if 'name' in st.session_state.user_data.columns and st.session_state.user_data['name'].values[0]:
        user_name = st.session_state.user_data['name'].values[0]
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3 style="color: #ffcc00; text-shadow: 0 0 10px rgba(255, 204, 0, 0.5);">Welcome, {user_name}!</h3>
            <p>Your recovery journey is progressing at superhuman levels!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Calculate days since surgery
    days_since_surgery = None
    if 'surgery_date' in st.session_state.user_data.columns:
        surgery_date_str = st.session_state.user_data['surgery_date'].values[0]
        if surgery_date_str and surgery_date_str != '':
            try:
                surgery_date = datetime.strptime(surgery_date_str, '%Y-%m-%d')
                days_since_surgery = (datetime.today() - surgery_date).days
            except:
                pass
    
    # Display overall stats in a hero section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if days_since_surgery is not None:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background-color: rgba(0,0,0,0.2); border-radius: 10px; box-shadow: 0 0 10px rgba(255, 204, 0, 0.1);">
                <h4 style="margin: 0; color: #ffcc00;">Days Since Surgery</h4>
                <p style="font-size: 24px; margin: 10px 0;">{days_since_surgery}</p>
                <p style="font-size: 12px; margin: 0;">Phase: {get_rehab_phase(days_since_surgery)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        total_exercises = len(st.session_state.exercise_log)
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: rgba(0,0,0,0.2); border-radius: 10px; box-shadow: 0 0 10px rgba(255, 204, 0, 0.1);">
            <h4 style="margin: 0; color: #ffcc00;">Exercises Logged</h4>
            <p style="font-size: 24px; margin: 10px 0;">{total_exercises}</p>
            <p style="font-size: 12px; margin: 0;">Keep pushing your limits!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Calculate current ROM if data exists
        current_extension = None
        current_flexion = None
        if not st.session_state.rom_pain_log.empty:
            # Convert date column to datetime
            st.session_state.rom_pain_log['date'] = pd.to_datetime(st.session_state.rom_pain_log['date'])
            
            # Get the latest ROM measurement
            latest_rom = st.session_state.rom_pain_log.sort_values('date', ascending=False).iloc[0]
            current_extension = latest_rom['extension_angle']
            current_flexion = latest_rom['flexion_angle']
        
        if current_extension is not None and current_flexion is not None:
            rom_emoji = "🔥" if current_extension <= 0 and current_flexion >= 120 else "💪"
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background-color: rgba(0,0,0,0.2); border-radius: 10px; box-shadow: 0 0 10px rgba(255, 204, 0, 0.1);">
                <h4 style="margin: 0; color: #ffcc00;">Current ROM</h4>
                <p style="font-size: 18px; margin: 10px 0;">Ext: {current_extension}° / Flex: {current_flexion}° {rom_emoji}</p>
                <p style="font-size: 12px; margin: 0;">{get_rom_status(current_extension, current_flexion)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        # Calculate current pain level if data exists
        current_pain = None
        if not st.session_state.rom_pain_log.empty:
            # Get the latest pain measurement
            latest_pain = st.session_state.rom_pain_log.sort_values('date', ascending=False).iloc[0]
            current_pain = latest_pain['pain_level']
        
        if current_pain is not None:
            pain_emoji = "🌟" if current_pain <= 2 else "😐" if current_pain <= 5 else "😣"
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background-color: rgba(0,0,0,0.2); border-radius: 10px; box-shadow: 0 0 10px rgba(255, 204, 0, 0.1);">
                <h4 style="margin: 0; color: #ffcc00;">Current Pain</h4>
                <p style="font-size: 24px; margin: 10px 0;">{current_pain}/10 {pain_emoji}</p>
                <p style="font-size: 12px; margin: 0;">{get_pain_status(current_pain)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Add a progress timeline
    if days_since_surgery is not None:
        # Display timeline with anime-inspired styling
        timeline_stages = [
            {"days": 0, "name": "Surgery", "description": "Beginning of your journey", "color": "#ff4500"},
            {"days": 7, "name": "Phase 1", "description": "Early motion & pain control", "color": "#ff6a00"},
            {"days": 21, "name": "Phase 2", "description": "Progressive loading", "color": "#ff9900"},
            {"days": 42, "name": "Phase 3", "description": "Strength normalization", "color": "#ffcc00"},
            {"days": 90, "name": "Phase 4", "description": "Power & return to loading", "color": "#99cc00"},
            {"days": 180, "name": "Phase 5", "description": "Return to sport/impact", "color": "#00ccff"}
        ]
        
        # Create a simplified timeline visualization
        st.markdown("""
        <div style="margin: 30px 0;">
            <h3 style="color: #ffcc00; text-align: center;">Recovery Timeline</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate current phase based on days since surgery
        if days_since_surgery < 0:
            current_phase = "Pre-Op"
        else:
            current_phase = "Post-Op"
            for i, stage in enumerate(timeline_stages):
                if days_since_surgery >= stage["days"]:
                    if i < len(timeline_stages) - 1 and days_since_surgery < timeline_stages[i+1]["days"]:
                        current_phase = stage["name"]
                    elif i == len(timeline_stages) - 1:
                        current_phase = stage["name"]
        
        # Create a container for the timeline
        timeline_container = st.container()
        
        # Create a more reliable timeline display
        col1, col2 = st.columns([1, 5])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background-color: rgba(0,0,0,0.2); border-radius: 10px;">
                <h4 style="margin: 0; color: #ffcc00;">Current Phase</h4>
                <p style="font-size: 18px; margin: 10px 0; color: #ffcc00;">{current_phase}</p>
                <p style="font-size: 12px; margin: 0;">Day {days_since_surgery}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Create a simplified timeline using Streamlit's progress bar
            st.markdown("<p style='margin-bottom: 5px;'>Rehabilitation Progress</p>", unsafe_allow_html=True)
            
            # Calculate progress percentage (capped at 100% and minimum 0%)
            # Handle pre-surgery (negative days) by setting to 0
            if days_since_surgery < 0:
                progress_percent = 0.0
            else:
                progress_percent = min(1.0, max(0.0, days_since_surgery / timeline_stages[-1]["days"]))
            
            st.progress(progress_percent)
            
            # Create phase labels using Streamlit columns instead of HTML
            phase_cols = st.columns(len(timeline_stages))
            for i, (col, stage) in enumerate(zip(phase_cols, timeline_stages)):
                with col:
                    # Use Streamlit's native markdown with colors
                    if (days_since_surgery >= stage["days"] and 
                        (i == len(timeline_stages) - 1 or days_since_surgery < timeline_stages[i+1]["days"])):
                        # Current phase
                        st.markdown(f"<div style='text-align: center;'><div style='height: 10px; width: 2px; background-color: {stage['color']}; margin: 0 auto;'></div><p style='font-size: 10px; color: {stage['color']}; font-weight: bold;'>{stage['name']}</p></div>", unsafe_allow_html=True)
                    else:
                        # Other phases
                        st.markdown(f"<div style='text-align: center;'><div style='height: 10px; width: 2px; background-color: {stage['color']}; margin: 0 auto;'></div><p style='font-size: 10px; color: {stage['color']};'>{stage['name']}</p></div>", unsafe_allow_html=True)
        
        # Add phase descriptions
        st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Create phase description cards with expanders to save space
        st.subheader("Rehabilitation Phases", anchor=False)
        
        for i, stage in enumerate(timeline_stages):
            is_current = (days_since_surgery >= stage["days"] and 
                         (i == len(timeline_stages) - 1 or days_since_surgery < timeline_stages[i+1]["days"]))
            
            # Create a custom expander with color
            if is_current:
                st.markdown(f"""
                <div style="border-left: 4px solid {stage['color']}; padding-left: 10px; margin-bottom: 10px;">
                    <h4 style="color: {stage['color']}; margin-bottom: 5px;">{stage['name']} (Day {stage['days']}+) ← Current Phase</h4>
                    <p style="font-size: 14px; margin-top: 0;">{stage['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                with st.expander(f"{stage['name']} (Day {stage['days']}+)"):
                    st.markdown(f"""
                    <div style="border-left: 4px solid {stage['color']}; padding-left: 10px;">
                        <p style="font-size: 14px; margin-top: 0;">{stage['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
