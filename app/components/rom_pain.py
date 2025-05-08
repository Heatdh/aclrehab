import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from db_utils import remove_rom_pain_entry

def show_rom_pain():
    st.title("Range of Motion & Pain Tracker")
    
    # Create tabs for logging new data and viewing history
    tab1, tab2 = st.tabs(["Log ROM & Pain", "History"])
    
    with tab1:
        with st.form("rom_pain_form"):
            st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
            
            # Date picker defaulted to today
            log_date = st.date_input("Date", value=datetime.today())
            
            # ROM section with better styling
            st.markdown("""
            <div style="margin: 20px 0 10px 0;">
                <h3 style="color: #36d1dc; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;">
                    Range of Motion
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
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
            
            # Visual representation of ROM using modern gauges
            col1, col2 = st.columns(2)
            with col1:
                # Extension visualization with better styling
                ext_percent = ((extension_angle + 15) / 45) * 100  # Convert to percentage (from -15 to 30)
                ext_color = "#36d1dc" if extension_angle <= 0 else "#5b86e5" if extension_angle <= 10 else "#ff6b6b"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 5px;">Extension Power</div>
                    <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; width: 100%; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, {ext_color}, {ext_color}99); width: {max(5, 100-ext_percent)}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {ext_color}; margin-top: 10px;">{extension_power}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">POWER POINTS</div>
                </div>
                
                <div style="text-align: center; background: rgba(255,255,255,0.05); border-radius: 12px; padding: 10px; margin-top: 15px;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: {ext_color};">{extension_angle}°</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                        {get_extension_status(extension_angle)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                # Flexion visualization with better styling
                flex_percent = (flexion_angle / 160) * 100  # Convert to percentage (from 0 to 160)
                flex_color = "#ff6b6b" if flexion_angle < 90 else "#5b86e5" if flexion_angle < 120 else "#36d1dc"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 5px;">Flexion Power</div>
                    <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; width: 100%; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, {flex_color}99, {flex_color}); width: {max(5, flex_percent)}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {flex_color}; margin-top: 10px;">{flexion_power}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">POWER POINTS</div>
                </div>
                
                <div style="text-align: center; background: rgba(255,255,255,0.05); border-radius: 12px; padding: 10px; margin-top: 15px;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: {flex_color};">{flexion_angle}°</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                        {get_flexion_status(flexion_angle)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Pain & Swelling section with better styling
            st.markdown("""
            <div style="margin: 30px 0 10px 0;">
                <h3 style="color: #36d1dc; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;">
                    Pain & Swelling
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
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
            
            # Visual representation of pain/swelling with better design
            col1, col2 = st.columns(2)
            with col1:
                # Pain visualization
                pain_color = "#36d1dc" if pain_level <= 3 else "#5b86e5" if pain_level <= 6 else "#ff6b6b"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 5px;">Pain Resistance</div>
                    <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; width: 100%; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, {pain_color}, {pain_color}99); width: {max(5, 100-(pain_level*10))}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {pain_color}; margin-top: 10px;">{pain_power}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">POWER POINTS</div>
                </div>
                
                <div style="text-align: center; background: rgba(255,255,255,0.05); border-radius: 12px; padding: 10px; margin-top: 15px;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: {pain_color};">{pain_level}/10</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                        {get_pain_status(pain_level)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                # Swelling visualization
                swell_color = "#36d1dc" if swelling_value <= 1 else "#5b86e5" if swelling_value <= 2 else "#ff6b6b"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 5px;">Swelling Control</div>
                    <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 10px; width: 100%; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, {swell_color}, {swell_color}99); width: {max(5, 100-(swelling_value*33))}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {swell_color}; margin-top: 10px;">{swelling_power}</div>
                    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5);">POWER POINTS</div>
                </div>
                
                <div style="text-align: center; background: rgba(255,255,255,0.05); border-radius: 12px; padding: 10px; margin-top: 15px;">
                    <div style="font-size: 2.5rem; font-weight: 700; color: {swell_color};">{swelling}</div>
                    <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">
                        {get_swelling_status(swelling_value)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            notes = st.text_area("Notes", height=100, 
                                help="Record any additional observations, what you did before measurement, etc.")
            
            # Total power calculation
            total_power_gain = extension_power + flexion_power + pain_power + swelling_power
            
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0; padding: 20px; background: linear-gradient(135deg, rgba(54, 209, 220, 0.2), rgba(91, 134, 229, 0.2)); border-radius: 16px;">
                <div style="font-size: 1rem; color: rgba(255,255,255,0.7); margin-bottom: 5px;">TOTAL POWER GAIN</div>
                <div style="font-size: 3rem; font-weight: 700; color: #36d1dc; text-shadow: 0 0 10px rgba(54, 209, 220, 0.5);">
                    {total_power_gain:,}
                </div>
                <div style="font-size: 0.9rem; color: rgba(255,255,255,0.7);">POINTS</div>
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
                # Convert columns in existing dataframe to match new entry
                for col in new_entry.columns:
                    if col in st.session_state.rom_pain_log.columns:
                        # Get the dtype from the new entry
                        new_dtype = new_entry[col].dtype
                        # Convert the column in the existing dataframe
                        st.session_state.rom_pain_log[col] = st.session_state.rom_pain_log[col].astype(new_dtype)
                
                # Now concatenate with matching dtypes
                st.session_state.rom_pain_log = pd.concat([st.session_state.rom_pain_log, new_entry], ignore_index=True)
            
            # Update power level
            st.session_state.power_level += total_power_gain
            st.session_state.show_power_up = True
            
            # Modern achievement box with animation
            st.markdown(f"""
            <div class="achievement-box">
                <h3 style="color: #36d1dc;">MEASUREMENTS LOGGED!</h3>
                <p>Your knee's power level increased by <span style="color: #36d1dc; font-weight: bold;">{total_power_gain:,}</span> points!</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Special messages based on achievement
            if extension_angle <= 0 and flexion_angle >= 130:
                st.markdown("""
                <div class="achievement-box" style="background: linear-gradient(135deg, rgba(54, 209, 220, 0.2), rgba(54, 209, 220, 0.05));">
                    <h3 style="color: #36d1dc;">ACHIEVEMENT UNLOCKED: NORMAL ROM!</h3>
                    <p>You've achieved normal knee range of motion! This is a significant milestone in your recovery!</p>
                </div>
                """, unsafe_allow_html=True)
            
            if pain_level <= 2 and swelling_value == 0:
                st.markdown("""
                <div class="achievement-box" style="background: linear-gradient(135deg, rgba(91, 134, 229, 0.2), rgba(91, 134, 229, 0.05));">
                    <h3 style="color: #5b86e5;">PAIN RESISTANCE MASTERED!</h3>
                    <p>Your knee is showing incredible recovery potential with minimal pain and swelling!</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Success message
            st.success(f"Measurements logged successfully! Power level is now {st.session_state.power_level:,}!")
    
    with tab2:
        # Filter out empty dataframes
        if not hasattr(st.session_state, 'rom_pain_log') or st.session_state.rom_pain_log.empty:
            st.info("No ROM or pain data recorded yet. Use the 'Log ROM & Pain' tab to start tracking.")
        else:
            st.markdown("""
            <div style="margin: 20px 0 10px 0;">
                <h3 style="color: #36d1dc; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;">
                    ROM & Pain History
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Sort dataframe by date (most recent first)
            history_df = st.session_state.rom_pain_log.copy()
            # Convert date column to datetime if it's not already
            history_df['date'] = pd.to_datetime(history_df['date'])
            history_df = history_df.sort_values(by='date', ascending=False)
            
            # Prepare for charts
            if len(history_df) >= 2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                # Create charts row
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    # ROM progression chart
                    fig_rom = go.Figure()
                    
                    # Convert dates for proper timeline
                    history_df['date'] = pd.to_datetime(history_df['date'])
                    plot_df = history_df.sort_values('date')
                    
                    # Add traces for extension and flexion
                    fig_rom.add_trace(go.Scatter(
                        x=plot_df['date'], 
                        y=plot_df['extension_angle'],
                        name='Extension',
                        line=dict(color='#36d1dc', width=3),
                        mode='lines+markers',
                    ))
                    
                    fig_rom.add_trace(go.Scatter(
                        x=plot_df['date'], 
                        y=plot_df['flexion_angle'],
                        name='Flexion',
                        line=dict(color='#5b86e5', width=3),
                        mode='lines+markers',
                        yaxis="y2"
                    ))
                    
                    # Create dual y-axis layout
                    fig_rom.update_layout(
                        title="ROM Progression",
                        title_font_color="#36d1dc",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=10, r=10, t=40, b=10),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            font=dict(color='rgba(255,255,255,0.7)')
                        ),
                        xaxis=dict(
                            showgrid=False,
                            zeroline=False,
                            title="Date",
                            color='rgba(255,255,255,0.5)'
                        ),
                        yaxis=dict(
                            title="Extension (°)",
                            showgrid=True,
                            gridcolor='rgba(255,255,255,0.1)',
                            zeroline=False,
                            color='rgba(255,255,255,0.5)'
                        ),
                        yaxis2=dict(
                            title="Flexion (°)",
                            overlaying="y",
                            side="right",
                            showgrid=False,
                            zeroline=False,
                            color='rgba(255,255,255,0.5)'
                        ),
                        font=dict(color='rgba(255,255,255,0.7)'),
                    )
                    
                    st.plotly_chart(fig_rom, use_container_width=True)
                
                with chart_col2:
                    # Pain & Swelling chart
                    fig_pain = go.Figure()
                    
                    # Add traces for pain and swelling
                    fig_pain.add_trace(go.Scatter(
                        x=plot_df['date'],
                        y=plot_df['pain_level'],
                        name='Pain Level',
                        line=dict(color='#ff6b6b', width=3),
                        mode='lines+markers',
                    ))
                    
                    fig_pain.add_trace(go.Scatter(
                        x=plot_df['date'],
                        y=plot_df['swelling'],
                        name='Swelling',
                        line=dict(color='#ffab00', width=3),
                        mode='lines+markers',
                    ))
                    
                    # Format the chart
                    fig_pain.update_layout(
                        title="Pain & Swelling Trends",
                        title_font_color="#36d1dc",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=10, r=10, t=40, b=10),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                            font=dict(color='rgba(255,255,255,0.7)')
                        ),
                        xaxis=dict(
                            showgrid=False,
                            zeroline=False,
                            title="Date",
                            color='rgba(255,255,255,0.5)'
                        ),
                        yaxis=dict(
                            title="Level",
                            showgrid=True,
                            gridcolor='rgba(255,255,255,0.1)',
                            zeroline=False,
                            color='rgba(255,255,255,0.5)'
                        ),
                        font=dict(color='rgba(255,255,255,0.7)'),
                    )
                    
                    st.plotly_chart(fig_pain, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Display history as cards instead of a table
            st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
            
            for _, row in history_df.iterrows():
                swelling_levels = {0: "None", 1: "Minimal (+1)", 2: "Moderate (+2)", 3: "Severe (+3)"}
                swelling_text = swelling_levels.get(row['swelling'], "Unknown")
                
                # Convert string date to datetime for formatting
                date_obj = pd.to_datetime(row['date']) if not isinstance(row['date'], pd.Timestamp) else row['date']
                formatted_date = date_obj.strftime("%B %d, %Y")
                
                # ROM status indicators
                ext_color = "#36d1dc" if row['extension_angle'] <= 0 else "#5b86e5" if row['extension_angle'] <= 10 else "#ff6b6b"
                flex_color = "#ff6b6b" if row['flexion_angle'] < 90 else "#5b86e5" if row['flexion_angle'] < 120 else "#36d1dc"
                pain_color = "#36d1dc" if row['pain_level'] <= 3 else "#5b86e5" if row['pain_level'] <= 6 else "#ff6b6b"
                swell_color = "#36d1dc" if row['swelling'] <= 1 else "#5b86e5" if row['swelling'] <= 2 else "#ff6b6b"
                
                # Card UI
                st.markdown(f"""
                <div class="fitness-card" style="margin-bottom: 15px; position: relative;">
                    <div style="position: absolute; right: 15px; top: 15px;">
                        <button onclick="alert('To delete this entry, use the delete button below.')" 
                                style="background: none; border: none; cursor: pointer; color: #ff6b6b; font-size: 18px;">
                            🗑️
                        </button>
                    </div>
                    
                    <div style="margin-bottom: 15px;">
                        <span style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">DATE</span>
                        <div style="font-weight: 600; color: #36d1dc; font-size: 1.2rem;">{formatted_date}</div>
                    </div>
                    
                    <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 15px;">
                        <div style="flex: 1; min-width: 120px;">
                            <span style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">EXTENSION</span>
                            <div style="font-weight: 600; color: {ext_color}; font-size: 1.5rem;">{row['extension_angle']}°</div>
                        </div>
                        
                        <div style="flex: 1; min-width: 120px;">
                            <span style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">FLEXION</span>
                            <div style="font-weight: 600; color: {flex_color}; font-size: 1.5rem;">{row['flexion_angle']}°</div>
                        </div>
                        
                        <div style="flex: 1; min-width: 120px;">
                            <span style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">PAIN</span>
                            <div style="font-weight: 600; color: {pain_color}; font-size: 1.5rem;">{row['pain_level']}/10</div>
                        </div>
                        
                        <div style="flex: 1; min-width: 120px;">
                            <span style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">SWELLING</span>
                            <div style="font-weight: 600; color: {swell_color}; font-size: 1.2rem;">{swelling_text}</div>
                        </div>
                    </div>
                    
                    {f'<div style="font-style: italic; color: rgba(255,255,255,0.7); border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px;">{row["notes"]}</div>' if row["notes"] else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # Add a real delete button below each card for functionality
                if st.button("Delete This Entry", key=f"delete_rom_{row['date']}"):
                    if st.session_state.current_username:
                        # Call MongoDB function to remove the entry
                        success = remove_rom_pain_entry(st.session_state.current_username, row['date'])
                        if success:
                            # Also update the session state dataframe
                            st.session_state.rom_pain_log = st.session_state.rom_pain_log[
                                st.session_state.rom_pain_log['date'] != row['date']
                            ]
                            st.success(f"Entry from {formatted_date} deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete entry. Please try again.")
            
            st.markdown('</div>', unsafe_allow_html=True)

# Helper functions for status text
def get_extension_status(angle):
    if angle < 0:
        return "Excellent (Hyperextension)"
    elif angle == 0:
        return "Full Extension"
    elif angle <= 5:
        return "Good"
    elif angle <= 10:
        return "Moderate"
    else:
        return "Needs Improvement"

def get_flexion_status(angle):
    if angle >= 135:
        return "Excellent"
    elif angle >= 120:
        return "Very Good"
    elif angle >= 100:
        return "Good"
    elif angle >= 90:
        return "Fair"
    else:
        return "Needs Improvement"

def get_pain_status(level):
    if level == 0:
        return "None"
    elif level <= 2:
        return "Minimal"
    elif level <= 4:
        return "Mild"
    elif level <= 6:
        return "Moderate"
    elif level <= 8:
        return "Severe"
    else:
        return "Extreme"

def get_swelling_status(level):
    if level == 0:
        return "None"
    elif level == 1:
        return "Minimal"
    elif level == 2:
        return "Moderate"
    else:
        return "Severe"
