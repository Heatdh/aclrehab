import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def show_rom_pain():
    st.title("Range of Motion & Pain Tracker")
    
    # Create tabs for logging new data and viewing history
    tab1, tab2 = st.tabs(["Log ROM & Pain", "History"])
    
    with tab1:
        with st.form("rom_pain_form"):
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            
            # Date picker defaulted to today
            log_date = st.date_input("Date", value=datetime.today())
            
            st.subheader("Range of Motion")
            col1, col2 = st.columns(2)
            
            with col1:
                extension_angle = st.number_input(
                    "Extension Angle (°, negative for hyperextension)", 
                    min_value=-15.0, 
                    max_value=30.0, 
                    value=0.0, 
                    step=0.5, 
                    format="%.1f",
                    help="Full extension is 0°. Enter negative values for hyperextension."
                )
                
                # Calculate extension power level (better extension = more power)
                extension_power = int(max(0, (30 - extension_angle)) * 50)
                
            with col2:
                flexion_angle = st.number_input(
                    "Flexion Angle (°)", 
                    min_value=0.0, 
                    max_value=160.0, 
                    value=90.0, 
                    step=1.0, 
                    format="%.1f",
                    help="Normal knee flexion is approximately 135-150°."
                )
                
                # Calculate flexion power level (better flexion = more power)
                flexion_power = int(flexion_angle * 30)
            
            # Visual representation of ROM using anime theme
            col1, col2 = st.columns(2)
            with col1:
                # Extension visualization
                ext_percent = ((extension_angle + 15) / 45) * 100  # Convert to percentage (from -15 to 30)
                ext_color = "#ffcc00" if extension_angle <= 0 else "#ff9900" if extension_angle <= 10 else "#ff4500"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 10px;">
                    <p>Extension Power</p>
                    <div style="background-color: rgba(0,0,0,0.3); border-radius: 5px; height: 20px; width: 100%;">
                        <div style="background-color: {ext_color}; width: {max(5, 100-ext_percent)}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                    <p style="color: {ext_color};">{extension_power} Power Points</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                # Flexion visualization
                flex_percent = (flexion_angle / 160) * 100  # Convert to percentage (from 0 to 160)
                flex_color = "#ff4500" if flexion_angle < 90 else "#ff9900" if flexion_angle < 120 else "#ffcc00"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 10px;">
                    <p>Flexion Power</p>
                    <div style="background-color: rgba(0,0,0,0.3); border-radius: 5px; height: 20px; width: 100%;">
                        <div style="background-color: {flex_color}; width: {max(5, flex_percent)}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                    <p style="color: {flex_color};">{flexion_power} Power Points</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.subheader("Pain & Swelling")
            col1, col2 = st.columns(2)
            
            with col1:
                pain_level = st.slider(
                    "Pain Level (0-10)", 
                    min_value=0, 
                    max_value=10, 
                    value=3,
                    help="0 = No pain, 10 = Worst possible pain"
                )
                
                # Less pain = more power
                pain_power = int((10 - pain_level) * 80)
                
            with col2:
                swelling_options = {
                    "None": 0,
                    "Minimal (+1)": 1,
                    "Moderate (+2)": 2,
                    "Severe (+3)": 3
                }
                swelling = st.selectbox(
                    "Swelling Level", 
                    options=list(swelling_options.keys())
                )
                swelling_value = swelling_options[swelling]
                
                # Less swelling = more power
                swelling_power = int((3 - swelling_value) * 100)
            
            # Visual representation of pain/swelling
            col1, col2 = st.columns(2)
            with col1:
                # Pain visualization
                pain_color = "#ffcc00" if pain_level <= 3 else "#ff9900" if pain_level <= 6 else "#ff4500"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 10px;">
                    <p>Pain Resistance</p>
                    <div style="background-color: rgba(0,0,0,0.3); border-radius: 5px; height: 20px; width: 100%;">
                        <div style="background-color: {pain_color}; width: {max(5, 100-(pain_level*10))}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                    <p style="color: {pain_color};">{pain_power} Power Points</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                # Swelling visualization
                swell_color = "#ffcc00" if swelling_value <= 1 else "#ff9900" if swelling_value <= 2 else "#ff4500"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 10px;">
                    <p>Swelling Control</p>
                    <div style="background-color: rgba(0,0,0,0.3); border-radius: 5px; height: 20px; width: 100%;">
                        <div style="background-color: {swell_color}; width: {max(5, 100-(swelling_value*33))}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                    <p style="color: {swell_color};">{swelling_power} Power Points</p>
                </div>
                """, unsafe_allow_html=True)
            
            notes = st.text_area("Notes", height=100, 
                                help="Record any additional observations, what you did before measurement, etc.")
            
            # Total power calculation
            total_power_gain = extension_power + flexion_power + pain_power + swelling_power
            
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0; padding: 15px; background-color: rgba(255, 204, 0, 0.1); border-radius: 10px;">
                <h3>Total Power Gain: {total_power_gain:,} points</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🔥 Log Measurements")
            
        if submitted:
            # Create a new entry
            new_entry = pd.DataFrame({
                'date': [log_date.strftime("%Y-%m-%d")],
                'extension_angle': [float(extension_angle)],
                'flexion_angle': [float(flexion_angle)],
                'pain_level': [int(pain_level)],
                'swelling': [int(swelling_value)],
                'notes': [notes]
            })
            
            # Ensure data types match before concatenation
            if st.session_state.rom_pain_log.empty:
                st.session_state.rom_pain_log = new_entry
            else:
                # Convert columns in existing dataframe to match new entry types
                for col in new_entry.columns:
                    if col in st.session_state.rom_pain_log.columns:
                        st.session_state.rom_pain_log[col] = st.session_state.rom_pain_log[col].astype(new_entry[col].dtypes.iloc[0])
                
                # Now concatenate with matching dtypes
                st.session_state.rom_pain_log = pd.concat([st.session_state.rom_pain_log, new_entry], ignore_index=True)
            
            # Ensure data is saved immediately
            st.session_state.rom_pain_log.to_csv('data/rom_pain_log.csv', index=False)
            
            # Update power level
            st.session_state.power_level += total_power_gain
            st.session_state.show_power_up = True
            
            # Super Saiyan animation (part of the power-up effect)
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0; padding: 20px;">
                <h2 style="color: #ffcc00; text-shadow: 0 0 10px #ffcc00;">MEASUREMENTS LOGGED!</h2>
                <p>Your knee's power level increased by <span style="color: #ffcc00; font-weight: bold;">{total_power_gain:,}</span> points!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Special messages based on achievement
            if extension_angle <= 0 and flexion_angle >= 130:
                st.markdown("""
                <div style="text-align: center; padding: 15px; background-color: rgba(255, 204, 0, 0.1); border-radius: 10px; margin: 20px 0;">
                    <img src="app/images/goku_nobackground.gif" style="max-width: 120px; margin: 0 auto; display: block;">
                    <h3 style="color: #ffcc00;">Perfect ROM Achievement Unlocked!</h3>
                    <p>Your knee flexibility is reaching superhuman levels!</p>
                </div>
                """, unsafe_allow_html=True)
            
            if pain_level <= 2 and swelling_value == 0:
                st.markdown("""
                <div style="text-align: center; padding: 15px; background-color: rgba(0, 191, 255, 0.1); border-radius: 10px; margin: 20px 0; border: 1px solid #00bfff;">
                    <img src="app/images/goku_nobackground.gif" style="max-width: 120px; margin: 0 auto; display: block;">
                    <h3 style="color: #00bfff;">Pain Resistance Mastered!</h3>
                    <p>Your knee is showing incredible recovery potential!</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Success message
            st.success(f"Measurements logged successfully! Power level is now {st.session_state.power_level:,}!")
    
    with tab2:
        if st.session_state.rom_pain_log.empty:
            st.info("No ROM & pain data logged yet. Start tracking to see your progress!")
        else:
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            
            # Convert date strings to datetime
            st.session_state.rom_pain_log['date'] = pd.to_datetime(st.session_state.rom_pain_log['date'])
            
            # Date filter for history
            date_range = st.date_input(
                "Filter by date range",
                value=(
                    st.session_state.rom_pain_log['date'].min().date(),
                    st.session_state.rom_pain_log['date'].max().date()
                ),
                key="rom_date_filter"
            )
            
            # Filter dataframe by date range
            filtered_log = st.session_state.rom_pain_log
            if len(date_range) == 2:
                start_date, end_date = date_range
                mask = (filtered_log['date'].dt.date >= start_date) & (filtered_log['date'].dt.date <= end_date)
                filtered_log = filtered_log.loc[mask]
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ROM Progress
            st.subheader("ROM Progress Chart")
            
            # Plot extension and flexion trends
            fig1 = px.line(
                filtered_log, 
                x='date', 
                y=['extension_angle', 'flexion_angle'],
                labels={
                    'date': 'Date',
                    'value': 'Angle (°)',
                    'variable': 'Measurement'
                },
                title="Extension & Flexion Progress",
                color_discrete_map={
                    'extension_angle': '#ff9900',
                    'flexion_angle': '#00bfff'
                }
            )
            
            # Add target lines
            fig1.add_hline(y=0, line_dash="dash", line_color="#ffcc00", annotation_text="Extension Target")
            fig1.add_hline(y=130, line_dash="dash", line_color="#00bfff", annotation_text="Flexion Target")
            
            # Update layout for anime theme
            fig1.update_layout(
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(0,0,0,0.1)',
                font_color='#cccccc',
                title_font_color='#ffcc00',
                legend_title_font_color='#ffcc00',
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig1, use_container_width=True)
            
            # Pain & Swelling Trends
            st.subheader("Pain & Swelling Trends")
            
            fig2 = px.line(
                filtered_log, 
                x='date', 
                y=['pain_level', 'swelling'],
                labels={
                    'date': 'Date',
                    'value': 'Level',
                    'variable': 'Measurement'
                },
                title="Pain & Swelling Trends",
                color_discrete_map={
                    'pain_level': '#ff4500',
                    'swelling': '#9370db'
                }
            )
            
            # Add target line
            fig2.add_hline(y=3, line_dash="dash", line_color="#ffcc00", annotation_text="Pain Target")
            fig2.add_hline(y=1, line_dash="dash", line_color="#9370db", annotation_text="Swelling Target")
            
            # Update layout for anime theme
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0.1)',
                paper_bgcolor='rgba(0,0,0,0.1)',
                font_color='#cccccc',
                title_font_color='#ffcc00',
                legend_title_font_color='#ffcc00',
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            # Data Table
            st.subheader("Measurement History")
            
            # Calculate ROM ratio for display (flexion/extension - higher is better)
            display_df = filtered_log.copy()
            display_df['rom_ratio'] = display_df['flexion_angle'] / (display_df['extension_angle'] + 1)
            display_df['rom_ratio'] = display_df['rom_ratio'].round(1)
            
            # Format the date for display
            display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
            
            # Rename columns for display
            display_df = display_df.rename(columns={
                'date': 'Date',
                'extension_angle': 'Extension (°)',
                'flexion_angle': 'Flexion (°)',
                'pain_level': 'Pain (0-10)',
                'swelling': 'Swelling (0-3)',
                'rom_ratio': 'ROM Ratio',
                'notes': 'Notes'
            })
            
            # Sort by date (newest first) and display
            st.dataframe(
                display_df.sort_values('Date', ascending=False),
                hide_index=True,
                use_container_width=True
            )
