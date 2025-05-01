import streamlit as st
import pandas as pd
from datetime import datetime

def show_profile():
    st.title("User Profile")
    
    # Get default values safely
    try:
        default_name = st.session_state.user_data['name'].values[0] if not pd.isna(st.session_state.user_data['name'].values[0]) else ""
        default_age = int(st.session_state.user_data['age'].values[0]) if not pd.isna(st.session_state.user_data['age'].values[0]) else 30
        default_weight = float(st.session_state.user_data['weight'].values[0]) if not pd.isna(st.session_state.user_data['weight'].values[0]) else 70.0
        default_height = float(st.session_state.user_data['height'].values[0]) if not pd.isna(st.session_state.user_data['height'].values[0]) else 170.0
        
        # Safely handle surgery date
        surgery_date_str = st.session_state.user_data['surgery_date'].values[0]
        if surgery_date_str and not pd.isna(surgery_date_str) and surgery_date_str.strip():
            try:
                default_surgery_date = datetime.strptime(surgery_date_str, '%Y-%m-%d')
            except:
                default_surgery_date = datetime.today()
        else:
            default_surgery_date = datetime.today()
            
        # Safely handle injury type
        injury_options = ["ACL Tear", "ACL + Meniscus", "ACL + MCL", "ACL + PCL", "Other"]
        default_injury = st.session_state.user_data['injury_type'].values[0]
        if pd.isna(default_injury) or default_injury == '':
            default_injury_index = 0
        else:
            try:
                default_injury_index = injury_options.index(default_injury)
            except:
                default_injury_index = 0
    except Exception as e:
        # If any error occurs, use defaults
        st.warning(f"Using default values due to data initialization: {e}")
        default_name = ""
        default_age = 30
        default_weight = 70.0
        default_height = 170.0
        default_surgery_date = datetime.today()
        default_injury_index = 0
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value=default_name)
            age = st.number_input("Age", min_value=0, max_value=120, value=default_age)
            weight = st.number_input("Weight (kg)", min_value=0.0, max_value=200.0, value=default_weight, format="%.1f")
            height = st.number_input("Height (cm)", min_value=0.0, max_value=250.0, value=default_height, format="%.1f")
        
        with col2:
            surgery_date = st.date_input("Surgery Date", value=default_surgery_date)
            injury_type = st.selectbox(
                "Injury Type",
                options=["ACL Tear", "ACL + Meniscus", "ACL + MCL", "ACL + PCL", "Other"],
                index=default_injury_index
            )
            
            additional_notes = st.text_area("Additional Notes", height=100)
        
        save_button = st.form_submit_button("Save Profile")
        
        if save_button:
            # Update session state with new values
            st.session_state.user_data['name'] = [name]
            st.session_state.user_data['age'] = [age]
            st.session_state.user_data['weight'] = [weight]
            st.session_state.user_data['height'] = [height]
            st.session_state.user_data['surgery_date'] = [surgery_date.strftime('%Y-%m-%d')]
            st.session_state.user_data['injury_type'] = [injury_type]
            
            # Save to CSV
            try:
                st.session_state.user_data.to_csv('data/user_profile.csv', index=False)
                st.success("Profile saved successfully!")
            except Exception as e:
                st.error(f"Error saving profile: {e}")
    
    # Display rehabilitation timeline based on surgery date
    if 'surgery_date' in st.session_state.user_data and not pd.isna(st.session_state.user_data['surgery_date'].values[0]) and st.session_state.user_data['surgery_date'].values[0]:
        st.subheader("Rehabilitation Timeline")
        try:
            surgery_date = datetime.strptime(st.session_state.user_data['surgery_date'].values[0], '%Y-%m-%d')
            current_date = datetime.today()
            days_since_surgery = (current_date - surgery_date).days
            
            st.info(f"Days since surgery: {days_since_surgery}")
            
            # Create timeline
            timeline_data = [
                {"week": "Pre-op", "description": "Complete pre-op exercises and prepare for surgery."},
                {"week": "Week 0-2", "description": "Focus on swelling control, early ROM, and quad activation."},
                {"week": "Week 3-6", "description": "Progress ROM and begin early strength training."},
                {"week": "Week 7-12", "description": "Increase strength training and introduce light functional exercises."},
                {"week": "Week 13-20", "description": "Add plyometrics and sport-specific training."},
                {"week": "Week 21+", "description": "Gradual return to sport and maintenance."}
            ]
            
            current_phase = ""
            if days_since_surgery < 0:
                current_phase = "Pre-op"
            elif 0 <= days_since_surgery <= 14:
                current_phase = "Week 0-2"
            elif 15 <= days_since_surgery <= 42:
                current_phase = "Week 3-6"
            elif 43 <= days_since_surgery <= 84:
                current_phase = "Week 7-12"
            elif 85 <= days_since_surgery <= 140:
                current_phase = "Week 13-20"
            else:
                current_phase = "Week 21+"
            
            for phase in timeline_data:
                if phase["week"] == current_phase:
                    st.markdown(f"### 🔴 {phase['week']} (Current Phase)")
                    st.markdown(f"**{phase['description']}**")
                else:
                    st.markdown(f"### ⚪ {phase['week']}")
                    st.markdown(phase['description'])
        except Exception as e:
            st.error(f"Error displaying timeline: {e}")
