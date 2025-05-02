import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from db_utils import remove_rom_pain_entry

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
                    <h3 style="color: #ffcc00;">ACHIEVEMENT UNLOCKED: NORMAL ROM!</h3>
                    <p>You've achieved normal knee range of motion! This is a significant milestone in your recovery!</p>
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
        # Filter out empty dataframes
        if not hasattr(st.session_state, 'rom_pain_log') or st.session_state.rom_pain_log.empty:
            st.info("No ROM or pain data recorded yet. Use the 'Log ROM & Pain' tab to start tracking.")
        else:
            st.subheader("ROM & Pain History")
            
            # Sort dataframe by date (most recent first)
            history_df = st.session_state.rom_pain_log.sort_values(by='date', ascending=False).copy()
            
            # Display data table with delete buttons
            for index, row in history_df.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 3, 1])
                
                with col1:
                    st.markdown(f"**{row['date']}**")
                with col2:
                    st.markdown(f"Extension: **{row['extension_angle']}°**")
                with col3:
                    st.markdown(f"Flexion: **{row['flexion_angle']}°**")
                with col4:
                    st.markdown(f"Pain: **{row['pain_level']}/10**")
                with col5:
                    swelling_levels = {0: "None", 1: "Minimal (+1)", 2: "Moderate (+2)", 3: "Severe (+3)"}
                    swelling_text = swelling_levels.get(row['swelling'], "Unknown")
                    st.markdown(f"Swelling: **{swelling_text}**")
                with col6:
                    if st.button("🗑️", key=f"delete_rom_{row['date']}"):
                        if st.session_state.current_username:
                            # Call MongoDB function to remove the entry
                            success, message = remove_rom_pain_entry(st.session_state.current_username, row['date'])
                            if success:
                                # Also update the session state dataframe
                                st.session_state.rom_pain_log = st.session_state.rom_pain_log[
                                    st.session_state.rom_pain_log['date'] != row['date']
                                ]
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                
                # Display notes if available
                if row['notes'] and not pd.isna(row['notes']) and row['notes'].strip():
                    st.markdown(f"**Notes:** {row['notes']}")
                
                # Add a separator
                st.markdown("---")
            
            # ROM Progress Chart
            st.subheader("ROM Progress Chart")
            
            # Create a copy for plotting and ensure date is in datetime format
            plot_df = history_df.copy()
            plot_df['date'] = pd.to_datetime(plot_df['date'])
            plot_df = plot_df.sort_values('date')  # Sort by date for the chart
            
            # Create ROM chart
            fig_rom = px.line(
                plot_df, 
                x='date', 
                y=['extension_angle', 'flexion_angle'],
                labels={'value': 'Angle (degrees)', 'date': 'Date', 'variable': 'Measurement'},
                title='ROM Progress Over Time',
                markers=True,
                color_discrete_map={
                    'extension_angle': '#ff9900',  # Orange color for extension
                    'flexion_angle': '#00ccff'     # Blue color for flexion
                }
            )
            
            # Customize the ROM chart
            fig_rom.update_layout(
                xaxis_title='Date',
                yaxis_title='Angle (degrees)',
                legend_title='Measurement',
                hovermode='x unified',
                template='plotly_dark',
                height=500,
            )
            
            st.plotly_chart(fig_rom, use_container_width=True)
            
            # Pain & Swelling Progress Chart
            st.subheader("Pain & Swelling Progress Chart")
            
            # Create pain chart
            fig_pain = px.line(
                plot_df, 
                x='date', 
                y=['pain_level', 'swelling'],
                labels={'value': 'Level', 'date': 'Date', 'variable': 'Measurement'},
                title='Pain & Swelling Progress Over Time',
                markers=True,
                color_discrete_map={
                    'pain_level': '#ff4500',      # Red color for pain
                    'swelling': '#9966ff'        # Purple color for swelling
                }
            )
            
            # Customize the pain chart
            fig_pain.update_layout(
                xaxis_title='Date',
                yaxis_title='Level',
                legend_title='Measurement',
                hovermode='x unified',
                template='plotly_dark',
                height=500,
            )
            
            # For pain level, set y-axis range from 0 to 10
            fig_pain.update_yaxes(range=[0, 10])
            
            st.plotly_chart(fig_pain, use_container_width=True)
            
            # ROM Trends Analysis
            st.subheader("ROM Trends Analysis")
            
            if len(plot_df) >= 2:
                # Calculate ROM improvements
                first_extension = plot_df.iloc[0]['extension_angle']
                last_extension = plot_df.iloc[-1]['extension_angle']
                extension_improvement = first_extension - last_extension  # Lower is better for extension
                
                first_flexion = plot_df.iloc[0]['flexion_angle']
                last_flexion = plot_df.iloc[-1]['flexion_angle']
                flexion_improvement = last_flexion - first_flexion  # Higher is better for flexion
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        label="Extension Improvement", 
                        value=f"{last_extension:.1f}°", 
                        delta=f"{extension_improvement:.1f}°" if extension_improvement > 0 else f"{-extension_improvement:.1f}°",
                        delta_color="normal" if extension_improvement > 0 else "inverse"
                    )
                    
                with col2:
                    st.metric(
                        label="Flexion Improvement", 
                        value=f"{last_flexion:.1f}°", 
                        delta=f"{flexion_improvement:.1f}°",
                        delta_color="normal" if flexion_improvement > 0 else "inverse"
                    )
                
                # Calculate normal knee ROM achievement percentage
                normal_extension_target = 0  # 0 degrees is normal extension
                normal_flexion_target = 135  # 135 degrees is normal flexion
                
                extension_percentage = min(100, max(0, 100 - ((last_extension - normal_extension_target) / 5 * 100)))
                flexion_percentage = min(100, max(0, (last_flexion / normal_flexion_target) * 100))
                
                # Calculate overall ROM achievement
                overall_percentage = (extension_percentage + flexion_percentage) / 2
                
                st.markdown(f"""
                <div style="margin: 20px 0; padding: 20px; background-color: rgba(0,0,0,0.2); border-radius: 10px;">
                    <h4 style="text-align: center;">Overall ROM Achievement: {overall_percentage:.1f}%</h4>
                    <div style="background-color: rgba(0,0,0,0.3); border-radius: 5px; height: 30px; width: 100%; margin-top: 10px;">
                        <div style="background-image: linear-gradient(90deg, #ff4500, #ffcc00, #00cc00); 
                                  width: {overall_percentage}%; 
                                  height: 100%; 
                                  border-radius: 5px;">
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                        <span>0%</span>
                        <span>50%</span>
                        <span>100%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Recovery phase recommendations based on ROM
                st.subheader("Recovery Phase Recommendations")
                
                rehab_tips = []
                
                # Extension recommendations
                if last_extension > 10:
                    rehab_tips.append("❗ **Prioritize extension exercises** - Your extension is limited above 10°. Focus on achieving full extension with exercises like prone hangs and heel props.")
                elif last_extension > 5:
                    rehab_tips.append("⚠️ **Continue extension work** - You're progressing but still need to work on achieving full extension (0°). Try passive extension stretches.")
                elif last_extension > 0:
                    rehab_tips.append("✅ **Extension is good** - You're approaching normal extension. Keep maintaining with regular stretching.")
                else:
                    rehab_tips.append("🌟 **Extension is excellent** - You've achieved full or hyperextension. Keep maintaining this ROM.")
                
                # Flexion recommendations
                if last_flexion < 90:
                    rehab_tips.append("❗ **Focus on flexion exercises** - Your flexion is below 90°. This is a priority to improve function. Try heel slides, wall slides, and assisted flexion exercises.")
                elif last_flexion < 120:
                    rehab_tips.append("⚠️ **Continue flexion work** - You have functional flexion but need to keep improving. Try seated heel slides and gentle gym ball rolling.")
                elif last_flexion < 135:
                    rehab_tips.append("✅ **Flexion is good** - You're approaching normal flexion. Continue with regular stretching to achieve full ROM.")
                else:
                    rehab_tips.append("🌟 **Flexion is excellent** - You've achieved normal flexion. Focus on maintaining this ROM.")
                
                for tip in rehab_tips:
                    st.markdown(tip)
                
                # Show reference values
                st.info("📊 **Reference Values:** Normal knee ROM is 0° extension (or slight hyperextension) and 135-150° flexion.")
                
            else:
                st.info("Not enough data points to analyze trends. Log more ROM measurements to see your progress analysis.")
