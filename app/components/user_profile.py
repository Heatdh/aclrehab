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
    
    # Modern card-based profile form
    st.markdown("""
    <div style="margin: 20px 0;">
        <h3 style="color: #36d1dc; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
            Personal Information
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("profile_form"):
        st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
        
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
            
            bmi = round(weight / ((height / 100) ** 2), 1) if height > 0 else 0
            
            st.markdown(f"""
            <div style="margin-top: 20px; padding: 10px; background: rgba(54, 209, 220, 0.1); border-radius: 8px;">
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">BMI</div>
                <div style="font-size: 1.5rem; font-weight: 600; color: #36d1dc;">{bmi}</div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">
                    {get_bmi_category(bmi)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            additional_notes = st.text_area("Additional Notes", height=100)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
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
                
                # Show confirmation with animation
                st.markdown("""
                <div class="achievement-box" style="margin-top: 20px;">
                    <h3 style="color: #36d1dc;">Profile Updated!</h3>
                    <p>Your rehabilitation profile has been saved successfully.</p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error saving profile: {e}")
    
    # Display rehabilitation timeline based on surgery date
    if 'surgery_date' in st.session_state.user_data and not pd.isna(st.session_state.user_data['surgery_date'].values[0]) and st.session_state.user_data['surgery_date'].values[0]:
        st.markdown("""
        <div style="margin: 30px 0 20px 0;">
            <h3 style="color: #36d1dc; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
                Rehabilitation Journey
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            surgery_date = datetime.strptime(st.session_state.user_data['surgery_date'].values[0], '%Y-%m-%d')
            current_date = datetime.today()
            days_since_surgery = (current_date - surgery_date).days
            
            # Calculate percentage complete (assuming 6-month/180-day recovery)
            recovery_percent = min(100, max(0, int((days_since_surgery / 180) * 100)))
            
            # Fix the logic for pre vs post-op display
            # If surgery_date is in the future, show Until Surgery and positive days
            # If surgery_date is in the past or today, show Since Surgery and positive days
            status_text = "Since Surgery"
            days_display = days_since_surgery
            if surgery_date > current_date:  # Surgery is in the future
                status_text = "Until Surgery"
                days_display = (surgery_date - current_date).days  # This will be positive
            else:  # Surgery is today or in the past
                status_text = "Since Surgery"
                days_display = max(0, days_since_surgery)  # Ensure we don't show negative days
            
            # Use Streamlit columns and components instead of HTML where possible
            st.subheader("Rehabilitation Journey")
            
            # Create a container for the recovery progress
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown("**Recovery Progress**")
                    st.caption("Based on standard 6-month rehabilitation timeline")
                
                with col2:
                    st.markdown(f"<div style='text-align: right; background: rgba(54, 209, 220, 0.2); padding: 5px 12px; border-radius: 50px; font-size: 14px; color: #36d1dc;'>{recovery_percent}% Complete</div>", unsafe_allow_html=True)
            
                # Days counter and surgery date
                col_days, col_info = st.columns([1, 3])
                
                with col_days:
                    st.markdown(f"""
                    <div style="background: linear-gradient(90deg, #36d1dc, #5b86e5); color: white; padding: 15px; border-radius: 12px; text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700;">{days_display}</div>
                        <div style="font-size: 0.9rem;">days</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_info:
                    st.markdown(f"<div style='font-size: 1.2rem; font-weight: 600; color: #36d1dc;'>{status_text}</div>", unsafe_allow_html=True)
                    st.caption(f"Surgery Date: {surgery_date.strftime('%B %d, %Y')}")
                
                # Progress bar
                st.progress(recovery_percent/100)
            
            # Create timeline as separate cards instead of a complex HTML structure
            st.markdown("### Rehabilitation Phases")
            
            # Determine current phase
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
            
            # Create timeline data
            timeline_data = [
                {"week": "Pre-op", "description": "Complete pre-op exercises and prepare for surgery.", "color": "#36d1dc"},
                {"week": "Week 0-2", "description": "Focus on swelling control, early ROM, and quad activation.", "color": "#4cc4dc"},
                {"week": "Week 3-6", "description": "Progress ROM and begin early strength training.", "color": "#5cacdc"},
                {"week": "Week 7-12", "description": "Increase strength training and introduce light functional exercises.", "color": "#5b86e5"},
                {"week": "Week 13-20", "description": "Add plyometrics and sport-specific training.", "color": "#7b74e0"},
                {"week": "Week 21+", "description": "Gradual return to sport and maintenance.", "color": "#9370db"}
            ]
            
            # Create a card for each phase
            for phase in timeline_data:
                is_current = phase["week"] == current_phase
                bg_color = "rgba(25, 30, 40, 0.3)"
                text_color = "white"
                
                if is_current:
                    # Current phase gets highlighted
                    with st.container():
                        st.markdown(f"""
                        <div style="padding: 15px; background: linear-gradient(90deg, {phase['color']}22, rgba(25, 30, 40, 0.3)); 
                                   border-radius: 8px; border-left: 4px solid {phase['color']};">
                            <div style="font-weight: 600; color: {phase['color']};">
                                {phase['week']} ← Current Phase
                            </div>
                            <div style="color: rgba(255,255,255,0.8);">
                                {phase['description']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    # Non-current phases
                    st.markdown(f"""
                    <div style="padding: 15px; background: rgba(25, 30, 40, 0.3); 
                               border-radius: 8px; border-left: 4px solid {phase['color']};">
                        <div style="font-weight: 600; color: {phase['color']};">
                            {phase['week']}
                        </div>
                        <div style="color: rgba(255,255,255,0.8);">
                            {phase['description']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error displaying timeline: {e}")

    # Add injury information
    if injury_type:
        st.markdown("""
        <div style="margin: 30px 0 20px 0;">
            <h3 style="color: #36d1dc; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
                Injury Information
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        injury_info = get_injury_info(injury_type)
        
        # Use Streamlit components instead of complex HTML
        col1, col2 = st.columns([1, 5])
        
        with col1:
            st.markdown(f"""
            <div style="width: 60px; height: 60px; border-radius: 50%; background-color: rgba(54, 209, 220, 0.2); 
                      display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                <div style="font-size: 30px; text-align: center;">🩺</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"## {injury_type}")
            st.caption("Injury Details")
        
        # Description with proper spacing
        st.markdown(f"#### Description")
        st.write(injury_info['description'])
        
        # Key considerations as Streamlit bullet points
        st.markdown(f"#### Key Recovery Considerations")
        for item in injury_info['considerations']:
            st.markdown(f"- {item}")

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_injury_info(injury_type):
    info = {
        "ACL Tear": {
            "description": "An ACL tear is a rupture of the anterior cruciate ligament, one of the four main ligaments in the knee. It's commonly caused by sudden stops, changes in direction, or direct impact.",
            "considerations": [
                "Focus on regaining full extension early in recovery",
                "Gradually rebuild quadriceps and hamstring strength",
                "Ensure proper graft protection during initial healing phase",
                "Work on proprioception and balance exercises"
            ]
        },
        "ACL + Meniscus": {
            "description": "This combined injury involves both the ACL and the meniscus, which is the cartilage that cushions the knee joint. Meniscus injuries may affect weight-bearing and increase recovery complexity.",
            "considerations": [
                "Weight-bearing restrictions may be longer than with isolated ACL tears",
                "ROM progression may be more conservative",
                "May require specific modifications to protect the meniscus repair",
                "Longer timeframe before returning to pivoting sports"
            ]
        },
        "ACL + MCL": {
            "description": "This injury combines an ACL tear with damage to the medial collateral ligament (MCL), which provides stability to the inner knee. The MCL often heals without surgery.",
            "considerations": [
                "May require wearing a brace for additional stability",
                "Focus on medial knee stability exercises",
                "Often needs modified rehabilitation timeline",
                "Special attention to valgus stress protection"
            ]
        },
        "ACL + PCL": {
            "description": "This complex injury involves both the anterior and posterior cruciate ligaments, creating significant knee instability and requiring careful rehabilitation.",
            "considerations": [
                "More complex stability concerns due to multi-ligament injury",
                "More restrictive motion protocol initially",
                "Extended recovery timeline compared to isolated ACL tears",
                "Higher risk of complications and arthrofibrosis"
            ]
        },
        "Other": {
            "description": "Your knee injury has unique characteristics. Work closely with your surgeon and physical therapist to understand the specific requirements of your rehabilitation.",
            "considerations": [
                "Follow the specific protocols from your healthcare provider",
                "Report any unusual symptoms promptly",
                "Keep detailed notes on your progress and setbacks",
                "Be patient with your personal recovery timeline"
            ]
        }
    }
    
    return info.get(injury_type, info["Other"])
