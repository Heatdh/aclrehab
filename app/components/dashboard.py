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
            <div class="metric-container">
                <div class="metric-label">DAYS SINCE SURGERY</div>
                <div class="metric-value">{days_since_surgery}</div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.7);">{get_rehab_phase(days_since_surgery)}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        total_exercises = len(st.session_state.exercise_log)
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">EXERCISES LOGGED</div>
            <div class="metric-value">{total_exercises}</div>
            <div style="font-size: 14px; color: rgba(255,255,255,0.7);">Keep pushing your limits!</div>
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
            <div class="metric-container">
                <div class="metric-label">CURRENT ROM</div>
                <div class="metric-value" style="font-size: 1.8rem;">Ext: {current_extension}° | Flex: {current_flexion}°</div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.7);">{get_rom_status(current_extension, current_flexion)}</div>
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
            pain_color = "#36d1dc" if current_pain <= 2 else "#ffab00" if current_pain <= 5 else "#ff6b6b"
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-label">PAIN LEVEL</div>
                <div class="metric-value" style="color: {pain_color};">{current_pain}/10</div>
                <div style="font-size: 14px; color: rgba(255,255,255,0.7);">{get_pain_status(current_pain)}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Create recovery insights section
    st.markdown("""
    <div style="margin: 30px 0 20px 0;">
        <h3 style="color: #36d1dc; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
            Recovery Insights
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a progress timeline
    if days_since_surgery is not None:
        # Timeline stages
        timeline_stages = [
            {"days": 0, "name": "Surgery", "description": "Beginning of your journey", "color": "#36d1dc"},
            {"days": 7, "name": "Phase 1", "description": "Early motion & pain control", "color": "#4cc4dc"},
            {"days": 21, "name": "Phase 2", "description": "Progressive loading", "color": "#5cacdc"},
            {"days": 42, "name": "Phase 3", "description": "Strength normalization", "color": "#5b86e5"},
            {"days": 90, "name": "Phase 4", "description": "Power & return to loading", "color": "#7b74e0"},
            {"days": 180, "name": "Phase 5", "description": "Return to sport/impact", "color": "#9370db"}
        ]
        
        # Calculate current phase
        current_phase_idx = 0
        for i, stage in enumerate(timeline_stages):
            if days_since_surgery >= stage["days"]:
                current_phase_idx = i
        
        current_phase = timeline_stages[current_phase_idx]
        
        # Create progress card
        progress_percent = min(100, max(0, int((days_since_surgery / timeline_stages[-1]["days"]) * 100)))
        
        # Use a completely different approach without relying on complex timeline CSS
        st.markdown(f"""
        <div class="chart-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="margin: 0; color: #36d1dc;">Rehabilitation Timeline</h4>
                <div style="background: rgba(54, 209, 220, 0.2); padding: 5px 12px; border-radius: 50px; font-size: 14px; color: #36d1dc;">
                    {progress_percent}% Complete
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Build simple timeline items individually
        for i, stage in enumerate(timeline_stages):
            if i <= current_phase_idx + 1:
                # Create a background color based on whether this is the current phase
                bg_color = "rgba(25, 30, 40, 0.3)"
                if i == current_phase_idx:
                    # Extract RGB components from hex color for rgba
                    r = int(stage['color'][1:3], 16)
                    g = int(stage['color'][3:5], 16)
                    b = int(stage['color'][5:7], 16)
                    bg_color = f"rgba({r}, {g}, {b}, 0.15)"
                
                # Render a simple card for each phase
                st.markdown(f"""
                <div style="padding: 15px; margin-bottom: 15px; border-radius: 8px; background: {bg_color}; border-left: 4px solid {stage['color']};">
                    <div style="font-weight: 600; color: {stage['color']};">
                        {stage['name']} {" ← Current" if i == current_phase_idx else ""}
                    </div>
                    <div style="margin-top: 5px; color: rgba(255,255,255,0.7);">
                        Day {stage['days']}+: {stage['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Add the progress bar and footer
        st.markdown(f"""
            <div style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin: 20px 0; overflow: hidden;">
                <div style="height: 100%; width: {progress_percent}%; 
                        background: linear-gradient(90deg, #36d1dc, #5b86e5); 
                        border-radius: 3px;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span style="font-size: 12px; color: rgba(255,255,255,0.5);">Surgery</span>
                <span style="font-size: 12px; color: rgba(255,255,255,0.5);">6 Months</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create charts section
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        if not st.session_state.rom_pain_log.empty:
            # Prepare ROM data for charting
            rom_df = st.session_state.rom_pain_log.copy()
            rom_df['date'] = pd.to_datetime(rom_df['date'])
            rom_df = rom_df.sort_values('date')
            
            # ROM progression chart
            st.markdown("""
            <div style="margin: 20px 0 10px 0;">
                <h4 style="color: #36d1dc; margin-bottom: 10px;">ROM Progression</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Create the ROM chart with Plotly
            fig_rom = go.Figure()
            fig_rom.add_trace(go.Scatter(
                x=rom_df['date'], 
                y=rom_df['extension_angle'],
                name='Extension',
                line=dict(color='#36d1dc', width=3),
                mode='lines+markers',
            ))
            fig_rom.add_trace(go.Scatter(
                x=rom_df['date'], 
                y=rom_df['flexion_angle'],
                name='Flexion',
                line=dict(color='#5b86e5', width=3),
                mode='lines+markers',
            ))
            
            # Format the chart
            fig_rom.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
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
                    color='rgba(255,255,255,0.5)'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(255,255,255,0.1)',
                    zeroline=False,
                    color='rgba(255,255,255,0.5)'
                ),
                font=dict(color='rgba(255,255,255,0.7)'),
                height=300
            )
            
            st.plotly_chart(fig_rom, use_container_width=True)
    
    with chart_col2:
        if not st.session_state.rom_pain_log.empty:
            # Prepare pain data for charting
            pain_df = st.session_state.rom_pain_log.copy()
            pain_df['date'] = pd.to_datetime(pain_df['date'])
            pain_df = pain_df.sort_values('date')
            
            # Pain progression chart
            st.markdown("""
            <div style="margin: 20px 0 10px 0;">
                <h4 style="color: #36d1dc; margin-bottom: 10px;">Pain & Swelling Trend</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Create the pain chart with Plotly
            fig_pain = go.Figure()
            fig_pain.add_trace(go.Scatter(
                x=pain_df['date'], 
                y=pain_df['pain_level'],
                name='Pain Level',
                line=dict(color='#ff6b6b', width=3),
                mode='lines+markers',
            ))
            
            if 'swelling' in pain_df.columns:
                fig_pain.add_trace(go.Scatter(
                    x=pain_df['date'], 
                    y=pain_df['swelling'],
                    name='Swelling',
                    line=dict(color='#ffab00', width=3),
                    mode='lines+markers',
                ))
            
            # Format the chart
            fig_pain.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
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
                    color='rgba(255,255,255,0.5)'
                ),
                yaxis=dict(
                    showgrid=True, 
                    gridcolor='rgba(255,255,255,0.1)',
                    zeroline=False,
                    color='rgba(255,255,255,0.5)'
                ),
                font=dict(color='rgba(255,255,255,0.7)'),
                height=300
            )
            
            st.plotly_chart(fig_pain, use_container_width=True)
    
    # Exercise activity section
    if not st.session_state.exercise_log.empty:
        st.markdown("""
        <div style="margin: 30px 0 20px 0;">
            <h3 style="color: #36d1dc; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
                Exercise Activity
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Prepare exercise data
        ex_df = st.session_state.exercise_log.copy()
        ex_df['date'] = pd.to_datetime(ex_df['date'])
        
        # Calculate exercise statistics
        try:
            # Count exercises by category
            category_counts = ex_df['category'].value_counts().reset_index()
            category_counts.columns = ['category', 'count']
            
            # Create a calendar heatmap of exercise frequency
            ex_by_date = ex_df.groupby(ex_df['date'].dt.strftime('%Y-%m-%d')).size().reset_index()
            ex_by_date.columns = ['date', 'count']
            ex_by_date['date'] = pd.to_datetime(ex_by_date['date'])
            
            # Create a date range for all days
            date_range = None
            if len(ex_by_date) > 0:
                start_date = ex_by_date['date'].min()
                end_date = ex_by_date['date'].max()
                date_range = pd.date_range(start=start_date, end=end_date)
                all_dates = pd.DataFrame({'date': date_range})
                
                # Merge with existing data
                ex_calendar = all_dates.merge(ex_by_date, on='date', how='left').fillna(0)
                
                # Charts row
                act_col1, act_col2 = st.columns(2)
                
                with act_col1:
                    st.markdown("""
                    <div style="margin-bottom: 10px;">
                        <h4 style="color: #36d1dc; margin-bottom: 10px;">Exercise Categories</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Category donut chart
                    fig_cat = px.pie(
                        category_counts, 
                        values='count', 
                        names='category',
                        hole=.4,
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    
                    fig_cat.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=10, r=10, t=10, b=10),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.2,
                            xanchor="center",
                            x=0.5,
                            font=dict(color='rgba(255,255,255,0.7)')
                        ),
                        font=dict(color='rgba(255,255,255,0.7)'),
                        height=300
                    )
                    
                    st.plotly_chart(fig_cat, use_container_width=True)
                
                with act_col2:
                    st.markdown("""
                    <div style="margin-bottom: 10px;">
                        <h4 style="color: #36d1dc; margin-bottom: 10px;">Exercise Frequency</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Calendar heatmap
                    fig_cal = px.bar(
                        ex_calendar, 
                        x='date', 
                        y='count',
                        color='count',
                        color_continuous_scale=['#1f2730', '#36d1dc', '#5b86e5']
                    )
                    
                    fig_cal.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=10, r=10, t=10, b=10),
                        xaxis=dict(
                            showgrid=False, 
                            zeroline=False,
                            color='rgba(255,255,255,0.5)'
                        ),
                        yaxis=dict(
                            showgrid=True, 
                            gridcolor='rgba(255,255,255,0.1)',
                            zeroline=False,
                            color='rgba(255,255,255,0.5)'
                        ),
                        font=dict(color='rgba(255,255,255,0.7)'),
                        height=300,
                        coloraxis_showscale=False
                    )
                    
                    st.plotly_chart(fig_cal, use_container_width=True)
                
                # Create recent activity cards
                st.markdown("""
                <div style="margin: 20px 0 10px 0;">
                    <h4 style="color: #36d1dc; margin-bottom: 10px;">Recent Activity</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Get recent exercises (last 5)
                recent_ex = ex_df.sort_values('date', ascending=False).head(5)
                
                # Display as cards
                for _, row in recent_ex.iterrows():
                    date_str = row['date'].strftime('%b %d, %Y')
                    st.markdown(f"""
                    <div class="exercise-card">
                        <h4>{row['exercise']}</h4>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div><span style="color: rgba(255,255,255,0.6);">Date:</span> {date_str}</div>
                            <div><span style="color: rgba(255,255,255,0.6);">Category:</span> {row['category']}</div>
                            <div><span style="color: rgba(255,255,255,0.6);">Sets:</span> {row['sets']}</div>
                            <div><span style="color: rgba(255,255,255,0.6);">Reps:</span> {row['reps']}</div>
                            <div><span style="color: rgba(255,255,255,0.6);">Weight:</span> {row['weight']} kg</div>
                        </div>
                        <div style="font-style: italic; color: rgba(255,255,255,0.8);">{row['notes'] if 'notes' in row and row['notes'] else "No notes"}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"Error generating exercise charts: {e}")
    
    # Wrap up with an encouragement card at the bottom
    st.markdown("""
    <div class="achievement-box" style="margin-top: 30px;">
        <h3 style="color: #36d1dc;">Keep Going Strong!</h3>
        <p style="max-width: 600px; margin: 10px auto;">
            Remember that consistent rehabilitation is key to a successful recovery. Track your progress, follow your plan, and celebrate each milestone!
        </p>
    </div>
    """, unsafe_allow_html=True)
