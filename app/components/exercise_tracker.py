import streamlit as st
import pandas as pd
from datetime import datetime
from db_utils import remove_exercise_entry
import base64
import plotly.express as px

def show_exercise_tracker():
    st.title("Exercise Tracker")
    
    # Create tabs for logging new exercises and viewing history
    tab1, tab2 = st.tabs(["Log Exercise", "Exercise History"])
    
    # Exercise descriptions for guidance
    exercise_descriptions = {
        # ROM Exercises
        "Heel Slides": "Lie on your back with legs straight. Slowly slide your heel toward your buttocks, bending your knee as much as comfortable. Hold 3-5 seconds, then slide back.",
        "Wall Slides": "Sit with your back against a wall, affected leg straight. Slowly slide down the wall, bending the knee. Hold, then slide back up.",
        "Prone Hangs": "Lie face down with legs extended off the edge of a bed/table. Let gravity gently pull your knee into extension. Great for regaining terminal extension.",
        "Heel Props": "Place a rolled towel under your heel with leg extended. Relax and let gravity push the knee down. Excellent passive extension exercise.",
        "Stationary Bike": "Use minimal resistance initially. Focus on increasing range of motion rather than resistance. Great for improving flexion.",
        "Seated Knee Extensions": "Sit with knees bent, slowly extend one knee until leg is straight. Hold briefly, then lower. Start without weights.",
        "Patella Mobilizations": "Gently move kneecap in all directions with fingers. Helps prevent scar tissue adhesions around the patella.",
        "Band-Assisted Knee Flexion": "Loop a band around ankle and pull to assist knee bending. Helps regain flexion with support.",
        "Band-Assisted Terminal Knee Extension": "Anchor band behind knee, loop around foot. The band helps achieve full extension.",
        "Supine Active Knee Extension": "Lie on back, hip at 90°. Extend knee as far as possible while maintaining hip position.",
        "Seated Active Knee Flexion": "Sit with leg extended, actively bend knee as far as possible. Helps regain active flexion.",
        "Wall Knee Flexion": "Stand facing wall, bend knee to bring foot up behind you. Wall provides balance support.",
        "Standing Hamstring Stretch": "Place heel on low surface, lean forward at hips keeping back straight. Feel stretch in hamstring.",
        "Quad Stretch": "Stand on one leg, pull other foot toward buttocks. Feel stretch in front of thigh.",
        
        # Strength Exercises
        "Straight Leg Raises": "Lie on your back with one leg bent and the other straight. Raise the straight leg to the height of the opposite knee. Great for early quad activation.",
        "Quad Sets": "Sit with leg extended, tighten quad muscle to push back of knee down. Hold 5 seconds. Fundamental for reactivating quad control.",
        "Hamstring Curls": "Lie face down, bend knee to bring heel toward buttocks. Start without weights, progress as tolerated.",
        "Glute Bridges": "Lie on back, feet flat. Lift hips toward ceiling by squeezing glutes. Essential for posterior chain strengthening.",
        "Wall Squats": "Stand with back against wall, slide down until knees are at 45-60°. Hold position. Great controlled squat progression.",
        "Step-Ups": "Step up onto a platform leading with affected leg. Start with low step, progress height as tolerated.",
        "Leg Press": "Use machine with light weight initially. Focus on controlled movement through comfortable range.",
        "Lunges": "Step forward into lunge position. Ensure knee tracks over toes. Start with partial range, progress to full.",
        "Romanian Deadlifts": "Hold weights, hinge at hips keeping back straight. Excellent for hamstring and posterior chain strength.",
        "Calf Raises": "Rise onto toes, lower slowly. Can be done double or single leg. Essential for push-off strength.",
        "Terminal Knee Extensions": "Stand with resistance band around back of knee. Extend knee against resistance. Critical for quad control.",
        "Reverse Lunges": "Step backward into lunge position. Often better tolerated than forward lunges early in rehab.",
        "Bulgarian Split Squats": "Stand in lunge position with rear foot elevated. Lower into lunge. Excellent single-leg stability exercise with reduced knee load compared to regular lunges.",
        "Pistol Squat Progression": "Single leg squat progression. Start with partial range using support, progress to deeper range.",
        "Good Mornings": "Hinge at hips with slight knee bend. Targets hamstrings and low back. Start without weights.",
        "Hip Adduction": "Move leg inward against resistance. Works inner thigh muscles important for knee stability.",
        "Hip Abduction": "Move leg outward against resistance. Critical for hip stability which supports knee function.",
        "Hip Thrusts": "Similar to glute bridge but shoulders elevated on bench. Advanced glute strengthening.",
        "Nordic Hamstring Curls": "Kneel with ankles anchored, hands ready to catch yourself. Slowly lower your torso toward the floor, resisting with your hamstrings. Advanced exercise for hamstring strength.",
        "Lateral Step-Downs": "Stand on step, lower other foot toward floor with controlled knee bend. Excellent for knee stability and control.",
        "Single-Leg Calf Raises": "Rise onto toes of one foot, lower slowly. Advanced progression for calf strength.",
        "Walking Lunges": "Continuous lunges while walking forward. More dynamic progression of static lunges.",
        
        # Band Exercises
        "Band Terminal Knee Extensions": "Sit with a band around the ankle, anchored behind you. Start with knee bent, then extend fully against resistance. Crucial for quad control.",
        "Band Hip Abduction": "Stand with a band around ankles/thighs. Move leg sideways against resistance. Strengthens hip stabilizers important for knee control.",
        "Band Hip Adduction": "Stand with one end of band anchored, loop around the inside of ankle. Pull leg inward against resistance. Works inner thigh muscles.",
        "Band Lateral Walks": "Place band around ankles/thighs. Take sidesteps while maintaining tension. Great for hip stabilizers and preventing knee valgus.",
        "Band Monster Walks": "Place band around ankles/thighs. Walk forward with small steps, maintaining outward tension. Activates glutes and teaches proper knee alignment.",
        "Band Hamstring Curls": "Anchor band in front, loop around ankle. Bend knee against resistance to work hamstrings. Crucial for ACL protection.",
        "Band Glute Bridges": "Lie on back with band above knees. Perform bridge by lifting hips. Band adds resistance to glutes, essential for knee stability.",
        "Band Standing Leg Press": "Anchor band under foot, hold other end in hands. Press leg back against resistance. Modified leg press for early strength building.",
        "Band Hip Extensions": "Anchor band in front, loop around ankle. Extend leg behind you against resistance. Targets glutes and hamstrings.",
        "Band Squats": "Stand on band with feet shoulder-width, hold ends at shoulders. Squat against resistance. Adds variable resistance to the squat pattern.",
        "Band Seated Row": "Sit with legs extended, band around feet. Pull band toward torso. Improves upper body posture which affects lower body mechanics.",
        "Band Clamshells": "Lie on side with band around knees, open knees while keeping feet together. Excellent for gluteus medius activation.",
        "Band Pull-Aparts": "Hold band in both hands at chest height. Pull apart, keeping arms straight. Strengthens upper back which improves overall posture during leg exercises.",
        "Band Deadlifts": "Stand on middle of band, holding ends. Perform deadlift motion against resistance. Total-body exercise that teaches proper hip-hinge mechanics.",
        "Band Standing Leg Abduction": "Anchor band at ankle level, loop around ankle. Abduct leg against resistance while standing. More functional position than lying.",
        "Band Lateral Raises": "Stand on band, raise arms out to sides. Upper body strength to complement lower body rehabilitation.",
        
        # Balance & Neuromuscular
        "Single-Leg Balance": "Stand on affected leg, maintain balance. Progress by closing eyes or standing on unstable surface. Fundamental exercise for proprioception.",
        "Mini-Trampoline": "Gentle bouncing on trampoline. Good for proprioception and low-impact loading of knee.",
        "Wobble Board": "Stand on wobble board, maintain balance. Progress from double-leg to single-leg stance. Excellent for ankle and knee proprioception.",
        "Bosu Ball": "Balance on flat or rounded side. More challenging than wobble board. Great for advanced proprioception training.",
        "Y-Balance Training": "Balance on one leg while reaching other leg in three directions. Excellent functional assessment and training tool.",
        "Side Stepping with Band": "Place band around ankles or above knees. Take side steps while maintaining tension. Good for hip stabilizers.",
        "Tandem Walking": "Walk heel-to-toe as if on a tightrope. Great for balance and proprioception.",
        "Single-Leg Deadlift": "Balance on one leg, hinge at hips reaching toward floor. Combines balance and strength training.",
        "Single-Leg Squat": "Squat on one leg with other leg extended. Advanced exercise for knee stability and strength.",
        "Balance Reach Exercises": "Balance on one leg while reaching other leg in different directions. Progressive challenge to stability.",
        "Agility Ladder Drills": "Various foot patterns through ladder on ground. Good for neuromuscular control and agility.",
        "Ball Toss with Balance": "Stand on one leg while tossing/catching a ball. Adds cognitive challenge to balance task.",
        "Single-Leg Clock Tap": "Balance on one leg, tap foot to clock positions (12, 3, 6, 9) while maintaining balance. Great for controlled stability.",
        "STAR Excursion Balance": "Similar to Y-balance but with more reaching directions. Advanced proprioceptive challenge.",
        "Band-Resisted Balance Work": "Maintain balance while band creates perturbation forces. Advanced proprioceptive training.",
        
        # Plyometrics
        "Double-Leg Hops": "Start with small, controlled hops in place. Progress to forward/backward and side-to-side. Focus on soft landings with bent knees.",
        "Lateral Hops": "Jump side to side over line or small object. Start small, progress distance and height. Important for change of direction confidence.",
        "Box Jumps": "Jump onto raised platform, step down. Focus on soft, controlled landing. Height progressions based on control.",
        "Lunge Jumps": "Start in lunge position, jump and switch legs mid-air. Advanced plyometric for power development.",
        "Depth Jumps": "Step off box, land and immediately jump again. Advanced plyometric for reactive strength.",
        "Skater Jumps": "Lateral jumps landing on one leg, mimicking skating motion. Great for lateral stability and power.",
        "Broad Jumps": "Jump forward for distance with double-leg takeoff and landing. Power development with horizontal emphasis.",
        "Tuck Jumps": "Jump straight up, bringing knees toward chest. Advanced plyometric for vertical power.",
        "Split Jumps": "Similar to lunge jumps but with more vertical emphasis. Good progression before more intense plyometrics.",
        "Single-Leg Hops": "Hopping on one leg in different directions. Advanced progression requiring good stability and strength.",
        "Jump Rope": "Basic jumping or running in place with rope. Low-level plyometric with good endurance component.",
        "Reactive Squat Jumps": "Quickly transition from landing to jumping again. Tests and builds reactive strength.",
        "Lateral Bound": "Powerful lateral jumps emphasizing distance. More advanced than lateral hops.",
        "Forward/Backward Bound": "Powerful jumps forward or backward. Tests linear power development.",
        "Band-Resisted Jumps": "Place band around thighs. Perform small jumps against resistance. Teaches proper landing mechanics with external feedback.",
        "Drop Jumps": "More intense version of depth jumps focusing on minimal ground contact time. Advanced plyometric.",
        
        # Martial Arts Training
        "Shadow Boxing": "Practice punches and defensive movements without contact. Low-impact way to maintain conditioning.",
        "Front Kick Drills": "Practice front kicks with focus on control and gradually increasing height. Good for hip flexor strength and knee control.",
        "Roundhouse Kick": "Circular kick targeting side of opponent. Start with low height, progress as tolerated. Good for hip rotation and control.",
        "Side Kick": "Linear kick to side with blade of foot. Start low and controlled, progress height. Good for hip abductor strength.",
        "Defensive Footwork": "Practice movement patterns focusing on proper foot placement and weight shifting. Essential for safe return to sport.",
        "Speed Bag": "Quick rhythmic punching of suspended bag. Good hand-eye coordination and endurance.",
        "Heavy Bag": "Striking larger bag with punches and kicks. Progress intensity and techniques as knee tolerates.",
        "Technical Sparring": "Light contact practice with partner. Emphasize control rather than power during rehabilitation.",
        "Slow Motion Kicks": "Perform kicks at reduced speed focusing on perfect form. Great for regaining neuromuscular control.",
        "Stance Transitions": "Practice shifting between fighting stances smoothly. Builds lower body control and stability.",
        "Band-Resisted Kicks": "Perform kicks against band resistance. Builds strength in specific kicking patterns.",
        "Knee Strike Practice": "Practice knee strike techniques gradually. Direct knee strengthening in functional pattern.",
        "Focus Mitt Work": "Strike partner-held targets. Partner can adjust height and position based on rehabilitation stage.",
        "Agility Ladder": "Footwork drills through ladder on ground. Builds agility and foot coordination.",
        "Controlled Pivoting": "Practice pivot movements slowly with focus on technique. Critical for knee confidence in rotational movements.",
        "Slide Steps": "Practice sliding step techniques common in martial arts. Low-impact movement pattern training.",
        "Blocking Drills": "Practice defensive blocking techniques. May involve less knee stress than attacking techniques.",
        
        # Recovery
        "Foam Rolling": "Self-myofascial release using foam roller. Target quads, ITB, hamstrings, and calves to reduce muscle tension.",
        "Massage Gun": "Use percussion massage device on tight muscles. Effective for localized muscle tension relief.",
        "Ice": "Apply ice pack for 15-20 minutes. Helpful for acute pain or post-exercise inflammation management.",
        "Compression": "Use compression sleeve or wrap. Helps manage swelling and provides proprioceptive feedback.",
        "Stretching": "Gentle static stretching of all lower limb muscles. Hold each stretch 30-60 seconds without bouncing.",
        "EMS": "Electrical muscle stimulation. Useful for muscle reeducation and pain management.",
        "Contrast Bath": "Alternate hot and cold water immersion. Can help with circulation and pain management.",
        "Light Cycling": "Gentle cycling with minimal resistance. Active recovery that promotes circulation without stress.",
        "Pool Walking": "Walking in water for reduced weight-bearing. Excellent for early-stage loading within pain limits.",
        "Static Stretching": "Hold stretches for 30+ seconds. Most effective after activity when tissues are warm.",
        "Dynamic Stretching": "Moving stretches without holding. Good preparation before more intense activity.",
        "PNF Stretching": "Contract-relax stretching technique. Contract muscle for 5-6 seconds, then relax and stretch further. More effective than static stretching alone.",
        "Meditation": "Mind-body practice focusing on breathing and present moment. Can help with pain management and rehabilitation mindset.",
        "Deep Breathing": "Diaphragmatic breathing exercises. Reduces stress which can impact muscle tension and recovery.",
        "Self-Massage": "Manual massage techniques performed on yourself. Can target specific trigger points or tight areas.",
        "TENS Unit": "Transcutaneous electrical nerve stimulation. May help with pain management through different mechanism than EMS.",
        "Progressive Muscle Relaxation": "Systematically tense and release muscle groups. Helps identify and reduce chronic tension patterns.",
        "Band-Assisted Stretching": "Use a band to assist in stretching tight muscles, particularly hamstrings and calves. Provides control and leverage for effective stretching.",
        "Joint Mobilizations": "Gentle oscillation movements of the knee joint to improve mobility without strain. Can be self-performed or with physical therapist."
    }
    
    with tab1:
        # Exercise selection with common rehab exercises
        exercise_categories = {
            "🔥 ROM Exercises": [
                "Heel Slides", "Wall Slides", "Prone Hangs", "Heel Props", 
                "Stationary Bike", "Seated Knee Extensions", "Patella Mobilizations",
                "Band-Assisted Knee Flexion", "Band-Assisted Terminal Knee Extension",
                "Supine Active Knee Extension", "Seated Active Knee Flexion",
                "Wall Knee Flexion", "Standing Hamstring Stretch", "Quad Stretch"
            ],
            "💪 Strength Exercises": [
                "Straight Leg Raises", "Quad Sets", "Hamstring Curls", "Glute Bridges",
                "Wall Squats", "Step-Ups", "Leg Press", "Lunges", "Romanian Deadlifts",
                "Calf Raises", "Terminal Knee Extensions", "Reverse Lunges", 
                "Bulgarian Split Squats", "Pistol Squat Progression", "Good Mornings",
                "Hip Adduction", "Hip Abduction", "Hip Thrusts", "Nordic Hamstring Curls",
                "Lateral Step-Downs", "Single-Leg Calf Raises", "Walking Lunges"
            ],
            "🎯 Resistance Band Exercises": [
                "Band Terminal Knee Extensions", "Band Hip Abduction", "Band Hip Adduction",
                "Band Lateral Walks", "Band Monster Walks", "Band Hamstring Curls",
                "Band Glute Bridges", "Band Standing Leg Press", "Band Hip Extensions",
                "Band Squats", "Band Seated Row", "Band Clamshells", "Band Pull-Aparts",
                "Band Deadlifts", "Band Standing Leg Abduction", "Band Lateral Raises"
            ],
            "🧠 Balance & Neuromuscular": [
                "Single-Leg Balance", "Mini-Trampoline", "Wobble Board", "Bosu Ball",
                "Y-Balance Training", "Side Stepping with Band", "Tandem Walking",
                "Single-Leg Deadlift", "Single-Leg Squat", "Balance Reach Exercises",
                "Agility Ladder Drills", "Ball Toss with Balance", "Single-Leg Clock Tap",
                "STAR Excursion Balance", "Band-Resisted Balance Work"
            ],
            "⚡ Plyometrics": [
                "Double-Leg Hops", "Lateral Hops", "Box Jumps", "Lunge Jumps", "Depth Jumps",
                "Skater Jumps", "Broad Jumps", "Tuck Jumps", "Split Jumps",
                "Single-Leg Hops", "Jump Rope", "Reactive Squat Jumps", "Lateral Bound",
                "Forward/Backward Bound", "Band-Resisted Jumps", "Drop Jumps"
            ],
            "👊 Martial Arts Training": [
                "Shadow Boxing", "Front Kick Drills", "Roundhouse Kick", "Side Kick",
                "Defensive Footwork", "Speed Bag", "Heavy Bag", "Technical Sparring",
                "Slow Motion Kicks", "Stance Transitions", "Band-Resisted Kicks",
                "Knee Strike Practice", "Focus Mitt Work", "Agility Ladder",
                "Controlled Pivoting", "Slide Steps", "Blocking Drills"
            ],
            "🧘 Recovery": [
                "Foam Rolling", "Massage Gun", "Ice", "Compression", "Stretching", "EMS",
                "Contrast Bath", "Light Cycling", "Pool Walking", "Static Stretching",
                "Dynamic Stretching", "PNF Stretching", "Meditation", "Deep Breathing",
                "Self-Massage", "TENS Unit", "Progressive Muscle Relaxation",
                "Band-Assisted Stretching", "Joint Mobilizations"
            ]
        }
        
        # Add styling to the category selection
        st.markdown("""
        <style>
        .exercise-category {
            background: linear-gradient(90deg, rgba(54, 209, 220, 0.2) 0%, rgba(0,0,0,0) 100%);
            border-left: 3px solid #36d1dc;
            padding-left: 10px;
            margin: 5px 0;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='exercise-category'>SELECT YOUR TRAINING EXERCISE</div>", unsafe_allow_html=True)
        
        # Initialize session state for exercise category if it doesn't exist
        if 'selected_category' not in st.session_state:
            st.session_state.selected_category = list(exercise_categories.keys())[0]
        
        # Create a modern card layout for category selection
        with st.container():
            st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
            
            # Category selection outside the form
            selected_category = st.selectbox(
                "Exercise Category", 
                options=list(exercise_categories.keys()),
                index=list(exercise_categories.keys()).index(st.session_state.selected_category),
                key="category_selector"
            )
            
            # Update session state with the new category
            st.session_state.selected_category = selected_category
            
            # Get exercises for the selected category
            available_exercises = exercise_categories[selected_category]
            
            # Add a search box to filter exercises
            search_term = st.text_input("🔍 Search exercises", value="", placeholder="Type to search...", key="search_term")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Filter exercises based on search term
        if search_term:
            filtered_exercises = [ex for ex in available_exercises if search_term.lower() in ex.lower()]
            if filtered_exercises:
                available_exercises = filtered_exercises
            else:
                st.info(f"No exercises matching '{search_term}' found in {selected_category}. Showing all exercises.")
        
        # Use session state to keep track of selected exercise
        if 'selected_exercise' not in st.session_state or st.session_state.selected_exercise not in available_exercises:
            # Initialize or reset if not valid in current category
            st.session_state.selected_exercise = available_exercises[0] if available_exercises else ""
        
        # Exercise selection with modern card design
        with st.container():
            st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
            
            # Exercise selection outside of form
            selected_exercise = st.selectbox(
                "Select Exercise", 
                options=available_exercises,
                index=available_exercises.index(st.session_state.selected_exercise) if st.session_state.selected_exercise in available_exercises else 0,
                key=f"exercise_selector_{selected_category}_{search_term}"
            )
            
            # Update session state with selected exercise
            st.session_state.selected_exercise = selected_exercise
            
            # Display exercise description with modern styling
            if selected_exercise in exercise_descriptions:
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, rgba(54, 209, 220, 0.1), rgba(54, 209, 220, 0.02)); 
                            border-left: 3px solid #36d1dc; 
                            padding: 15px; 
                            margin: 15px 0; 
                            border-radius: 8px;">
                    <span style="font-weight: 600; color: #36d1dc;">How to perform:</span> {exercise_descriptions[selected_exercise]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, rgba(255, 171, 0, 0.1), rgba(255, 171, 0, 0.02)); 
                            border-left: 3px solid #ffab00; 
                            padding: 15px; 
                            margin: 15px 0; 
                            border-radius: 8px;">
                    <span style="font-weight: 600; color: #ffab00;">Exercise Description:</span> Perform this exercise with controlled movements focusing on proper form. If you're unsure how to perform it correctly, consult with your physical therapist.
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Now create the form with the pre-selected category and exercise
        with st.form("exercise_form"):
            st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
            
            # Date picker defaulted to today
            exercise_date = st.date_input("Date", value=datetime.today())
            
            # Display the selected category and exercise (hidden input field to get the values in the form submission)
            st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <span style="font-size: 0.9rem; color: rgba(255,255,255,0.6);">SELECTED EXERCISE</span>
                <div style="font-weight: 600; color: #36d1dc; font-size: 1.1rem;">{selected_category} - {selected_exercise}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Exercise details with better layout
            col1, col2 = st.columns(2)
            with col1:
                sets = st.number_input("Sets", min_value=1, max_value=10, value=3)
                reps = st.number_input("Reps", min_value=1, max_value=100, value=10)
            with col2:
                weight = st.number_input("Weight (kg, 0 if bodyweight)", min_value=0.0, value=0.0, step=0.5, format="%.1f")
                difficulty = st.slider("Difficulty Level", min_value=1, max_value=10, value=5, 
                                      help="How challenging was this exercise? (1=easy, 10=extremely difficult)")
            
            notes = st.text_area("Notes", placeholder="How did it feel? Any modifications?", height=100)
            
            # Calculate power level gain based on exercise complexity and sets/reps
            power_gain = int((sets * reps * (1 + weight/10) * difficulty) * 1.5)
            
            # Close the card
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Submit button
            submitted = st.form_submit_button("💪 Complete Exercise")
            
        if submitted:
            # Create a new entry - using selected_exercise from session state
            new_entry = pd.DataFrame({
                'date': [exercise_date.strftime("%Y-%m-%d")],
                'category': [selected_category],
                'exercise': [selected_exercise],  # Use the selected exercise from session state
                'sets': [int(sets)],
                'reps': [int(reps)],
                'weight': [float(weight)],
                'notes': [notes]
            })
            
            # Ensure data types match before concatenation
            if st.session_state.exercise_log.empty:
                st.session_state.exercise_log = new_entry
            else:
                # Fix for type conversion - avoid using dtypes.iloc[0]
                try:
                    # Convert columns in existing dataframe to match new entry types
                    # Using safer approach for type conversion
                    for col in new_entry.columns:
                        if col in st.session_state.exercise_log.columns:
                            if col == 'date':
                                st.session_state.exercise_log[col] = st.session_state.exercise_log[col].astype(str)
                            elif col == 'sets' or col == 'reps':
                                st.session_state.exercise_log[col] = st.session_state.exercise_log[col].astype(int)
                            elif col == 'weight':
                                st.session_state.exercise_log[col] = st.session_state.exercise_log[col].astype(float)
                            else:
                                st.session_state.exercise_log[col] = st.session_state.exercise_log[col].astype(str)
                    
                    # Now concatenate with matching dtypes
                    st.session_state.exercise_log = pd.concat([st.session_state.exercise_log, new_entry], ignore_index=True)
                except Exception as e:
                    st.error(f"Error adding exercise: {e}")
                    # Fallback method if the above fails
                    try:
                        st.session_state.exercise_log = pd.concat([st.session_state.exercise_log, new_entry], ignore_index=True)
                    except Exception as e2:
                        st.error(f"Critical error adding exercise: {e2}")
            
            # Ensure data is saved immediately
            try:
                # Update power level
                st.session_state.power_level += power_gain
                st.session_state.show_power_up = True
                
                # Get base64 encoded GIF image for inline display
                try:
                    with open("app/images/goku_pose.gif", "rb") as f:
                        gif_data = f.read()
                        encoded_gif = base64.b64encode(gif_data).decode()
                    
                    # Power-up animation with inline GIF
                    st.markdown(f"""
                    <div class="achievement-box">
                        <img src="data:image/gif;base64,{encoded_gif}" style="max-width: 200px; margin: 0 auto; display: block; border-radius: 12px; box-shadow: 0 0 20px rgba(54, 209, 220, 0.4);">
                        <h3 style="color: #36d1dc; margin-top: 15px;">EXERCISE COMPLETE!</h3>
                        <p>Power level increased by <span style="color: #36d1dc; font-weight: 600;">{power_gain}</span> points!</p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    # Fallback if GIF loading fails
                    st.markdown(f"""
                    <div class="achievement-box">
                        <h3 style="color: #36d1dc;">EXERCISE COMPLETE!</h3>
                        <p>Power level increased by <span style="color: #36d1dc; font-weight: 600;">{power_gain}</span> points!</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show success message
                st.success(f"Exercise logged successfully! Power level increased to {st.session_state.power_level:,}!")
            except Exception as e:
                st.error(f"Error updating power level: {e}")
            
            # Special messages based on power level milestones with base64 encoded GIFs
            try:
                with open("app/images/power_app_animation.gif", "rb") as f:
                    power_gif = base64.b64encode(f.read()).decode()
                
                with open("app/images/goku_pose.gif", "rb") as f:
                    goku_gif = base64.b64encode(f.read()).decode()
                    
                with open("app/images/goku_nobackground.gif", "rb") as f:
                    goku_blue_gif = base64.b64encode(f.read()).decode()
                
                if st.session_state.power_level > 9000:
                    st.markdown(f"""
                    <div class="achievement-box">
                        <img src="data:image/gif;base64,{power_gif}" style="max-width: 150px; margin: 0 auto; display: block; border-radius: 12px; box-shadow: 0 0 20px rgba(54, 209, 220, 0.4);">
                        <h3 style="color: #36d1dc;">OUTSTANDING PROGRESS!</h3>
                        <p>Your recovery is accelerating rapidly!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                if st.session_state.power_level > 20000:
                    st.markdown(f"""
                    <div class="achievement-box">
                        <img src="data:image/gif;base64,{goku_gif}" style="max-width: 150px; margin: 0 auto; display: block; border-radius: 12px; box-shadow: 0 0 20px rgba(54, 209, 220, 0.4);">
                        <h3 style="color: #36d1dc;">ADVANCED LEVEL ACHIEVED!</h3>
                        <p>Your knee rehabilitation has reached a new stage!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                if st.session_state.power_level > 50000:
                    st.markdown(f"""
                    <div class="achievement-box" style="background: linear-gradient(135deg, rgba(20, 30, 48, 0.6), rgba(20, 25, 35, 0.6));">
                        <img src="data:image/gif;base64,{goku_blue_gif}" style="max-width: 150px; margin: 0 auto; display: block; border-radius: 12px; box-shadow: 0 0 20px rgba(91, 134, 229, 0.4);">
                        <h3 style="color: #5b86e5;">ELITE LEVEL ACHIEVED!</h3>
                        <p>Your dedication has reached professional levels!</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                if st.session_state.power_level > 100000:
                    st.markdown(f"""
                    <div class="achievement-box" style="background: linear-gradient(135deg, rgba(25, 20, 45, 0.6), rgba(20, 15, 35, 0.6));">
                        <img src="data:image/gif;base64,{power_gif}" style="max-width: 150px; margin: 0 auto; display: block; border-radius: 12px; box-shadow: 0 0 20px rgba(147, 112, 219, 0.4);">
                        <h3 style="color: #9370db;">MASTER LEVEL ACHIEVED!</h3>
                        <p>You've reached the pinnacle of rehabilitation excellence!</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                # Fallback if GIF loading fails
                if st.session_state.power_level > 9000:
                    st.success("OUTSTANDING PROGRESS! Your recovery is accelerating rapidly!")
                if st.session_state.power_level > 20000:
                    st.success("ADVANCED LEVEL ACHIEVED! Your knee rehabilitation has reached a new stage!")
                if st.session_state.power_level > 50000:
                    st.success("ELITE LEVEL ACHIEVED! Your dedication has reached professional levels!")
                if st.session_state.power_level > 100000:
                    st.success("MASTER LEVEL ACHIEVED! You've reached the pinnacle of rehabilitation excellence!")
    
    with tab2:
        # Improve history display with modern card layout
        st.markdown('<div class="fitness-card">', unsafe_allow_html=True)
        st.subheader("Exercise History")
        
        # Additional filtering options
        col1, col2 = st.columns(2)
        with col1:
            filter_category = st.selectbox(
                "Filter by Category", 
                options=["All Categories"] + list(exercise_categories.keys()),
                key="filter_category"
            )
        with col2:
            filter_date = st.date_input(
                "Filter by Date", 
                value=None,
                key="filter_date"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Check if there's any exercise data
        if st.session_state.exercise_log is not None and not st.session_state.exercise_log.empty:
            # Convert to DataFrame if it's a dictionary
            if isinstance(st.session_state.exercise_log, dict):
                exercise_log_df = pd.DataFrame(st.session_state.exercise_log)
            else:
                exercise_log_df = st.session_state.exercise_log.copy()
            
            # Apply filters
            if filter_category != "All Categories":
                exercise_log_df = exercise_log_df[exercise_log_df['category'] == filter_category]
            
            if filter_date is not None:
                filter_date_str = filter_date.strftime("%Y-%m-%d")
                exercise_log_df = exercise_log_df[exercise_log_df['date'] == filter_date_str]
            
            # Sort by date (most recent first)
            if 'date' in exercise_log_df.columns and not exercise_log_df.empty:
                try:
                    exercise_log_df['date'] = pd.to_datetime(exercise_log_df['date'])
                    exercise_log_df = exercise_log_df.sort_values(by='date', ascending=False)
                    # Convert back to string for display
                    exercise_log_df['date'] = exercise_log_df['date'].dt.strftime("%Y-%m-%d")
                except Exception as e:
                    st.warning(f"Could not sort by date: {e}")
            
            # Show data in a modern format
            if not exercise_log_df.empty:
                # Display exercises in card format instead of table
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                # Group by date for better organization
                exercise_log_df['date'] = pd.to_datetime(exercise_log_df['date'])
                grouped = exercise_log_df.groupby(exercise_log_df['date'].dt.strftime('%Y-%m-%d'))
                
                for date, group in grouped:
                    st.markdown(f'<h4 style="color: #36d1dc; margin-top: 20px;">{date}</h4>', unsafe_allow_html=True)
                    
                    for _, row in group.iterrows():
                        st.markdown(f"""
                        <div class="exercise-card">
                            <h4>{row['exercise']}</h4>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                                <div><span style="color: rgba(255,255,255,0.6);">Category:</span> {row['category']}</div>
                                <div><span style="color: rgba(255,255,255,0.6);">Sets:</span> {row['sets']}</div>
                                <div><span style="color: rgba(255,255,255,0.6);">Reps:</span> {row['reps']}</div>
                                <div><span style="color: rgba(255,255,255,0.6);">Weight:</span> {row['weight']} kg</div>
                            </div>
                            <div style="font-style: italic; color: rgba(255,255,255,0.8);">{row['notes'] if 'notes' in row and row['notes'] else "No notes"}</div>
                            <div style="text-align: right; margin-top: 10px;">
                                <a style="color: #ff6b6b; cursor: pointer; text-decoration: none;" 
                                   onclick="this.closest('.exercise-card').style.display='none'; parent.postMessage({{'type': 'streamlit:deleteExercise', 'date': '{date}', 'exercise': '{row['exercise']}'}}, '*')">
                                   Delete
                                </a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add JavaScript to handle deletion (not directly functional, would need backend integration)
                st.markdown("""
                <script>
                // This is just a placeholder. Streamlit's sandboxed iframe prevents this from working directly.
                // Would need custom components for full functionality
                </script>
                """, unsafe_allow_html=True)
                
                # Add a delete button that uses Streamlit's state management instead
                with st.expander("Delete Exercise Entry"):
                    # Get unique dates and exercises for deletion options
                    dates = exercise_log_df['date'].dt.strftime('%Y-%m-%d').unique().tolist()
                    
                    delete_date = st.selectbox("Select Date", options=dates, key="delete_date")
                    
                    # Filter exercises by selected date
                    filtered_exercises = exercise_log_df[exercise_log_df['date'].dt.strftime('%Y-%m-%d') == delete_date]['exercise'].unique().tolist()
                    
                    delete_exercise = st.selectbox("Select Exercise", options=filtered_exercises, key="delete_exercise")
                    
                    if st.button("Delete Entry", key="delete_button"):
                        # Call the function to remove the exercise entry
                        success = remove_exercise_entry(st.session_state.current_username, delete_date, delete_exercise)
                        if success:
                            st.success(f"Deleted {delete_exercise} entry from {delete_date}")
                            # Update the session state exercise log
                            st.session_state.exercise_log = get_exercise_log(st.session_state.current_username)
                            st.rerun()
                        else:
                            st.error("Failed to delete exercise entry")
            else:
                st.info("No exercise records found matching your filters.")
        else:
            st.info("No exercise records found. Start logging your exercises to track your progress!")

        # Add summary metrics in card layout
        if st.session_state.exercise_log is not None and not st.session_state.exercise_log.empty:
            try:
                # Convert to DataFrame if it's a dictionary
                if isinstance(st.session_state.exercise_log, dict):
                    summary_df = pd.DataFrame(st.session_state.exercise_log)
                else:
                    summary_df = st.session_state.exercise_log.copy()
                
                # Create proper date column
                summary_df['date'] = pd.to_datetime(summary_df['date'])
                
                # Calculate metrics
                total_workouts = len(summary_df['date'].unique())
                total_exercises = len(summary_df)
                most_common_exercise = summary_df['exercise'].value_counts().idxmax() if not summary_df.empty else "None"
                most_recent_date = summary_df['date'].max().strftime("%Y-%m-%d") if not summary_df.empty else "None"
                
                # Create a summary metrics row
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-label">TOTAL WORKOUTS</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{total_workouts}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-label">TOTAL EXERCISES</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value">{total_exercises}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-label">FAVORITE EXERCISE</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value" style="font-size: 1.5rem;">{most_common_exercise}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-label">LAST WORKOUT</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-value" style="font-size: 1.5rem;">{most_recent_date}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Add workout frequency chart
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.subheader("Workout Frequency")
                
                # Create chart data
                workout_dates = summary_df['date'].dt.strftime('%Y-%m-%d').value_counts().reset_index()
                workout_dates.columns = ['date', 'count']
                workout_dates['date'] = pd.to_datetime(workout_dates['date'])
                workout_dates = workout_dates.sort_values('date')
                
                # Create a date range including all days
                if not workout_dates.empty:
                    date_range = pd.date_range(start=workout_dates['date'].min(), end=workout_dates['date'].max())
                    all_dates = pd.DataFrame({'date': date_range})
                    
                    # Merge with actual workout dates
                    merged_dates = all_dates.merge(workout_dates, on='date', how='left').fillna(0)
                    
                    # Plot
                    fig = px.bar(
                        merged_dates, 
                        x='date', 
                        y='count',
                        color_discrete_sequence=['#36d1dc'],
                        labels={'date': 'Date', 'count': 'Exercises'},
                        title='Your Workout Frequency'
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='rgba(255,255,255,0.8)',
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Not enough data to generate workout frequency chart.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error generating metrics: {e}")
