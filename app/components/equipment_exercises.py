import streamlit as st
import pandas as pd

def show_equipment_exercises():
    st.title("Equipment-Based Rehabilitation Exercises")
    
    st.markdown("""
    This section provides detailed exercises using various rehabilitation equipment.
    These exercises are designed to complement your main rehab plan and can be 
    incorporated into your daily routine based on your current phase.
    """)
    
    # Create tabs for different equipment types
    tabs = st.tabs([
        "Foam Roller", 
        "Massage Gun", 
        "Pilates/Stability Ball",
        "Small Ball",
        "Plyometrics",
        "Daily Routines"
    ])
    
    # Foam Roller content
    with tabs[0]:
        st.subheader("Foam Roller Exercises")
        
        st.markdown("""
        Foam rolling helps improve tissue flexibility, reduces muscle tension, and promotes circulation.
        These self-myofascial release techniques can be performed daily to maintain tissue quality.
        """)
        
        foam_roller_data = {
            "Exercise": [
                "Quadriceps Roll",
                "IT Band Roll",
                "Hamstring Roll",
                "Calf Roll",
                "Adductor Roll",
                "Thoracic Spine Extension",
                "Latissimus Dorsi Roll"
            ],
            "Technique": [
                "Face down with roller under thighs, roll from hip to knee. Rotate slightly to target vastus lateralis and medialis.",
                "Lie on side with roller under lateral thigh, roll from hip to knee. Keep core engaged for stability.",
                "Sit with roller under thighs, roll from sit bones to knees. Cross one leg over to increase pressure.",
                "Sit with roller under lower leg, roll from ankle to knee. For deeper pressure, cross one leg over.",
                "Lie face down with roller positioned at inner thigh, roll along inner thigh from groin to knee.",
                "Lie with roller positioned at mid-back, hands behind head, gently extend over roller to improve thoracic mobility.",
                "Lie on side with roller under armpit, roll along side from armpit to mid-ribcage."
            ],
            "Prescription": [
                "2 minutes per leg, pause on tender spots for 20-30 seconds",
                "1-2 minutes per side, slowly roll through tender areas",
                "2 minutes per leg, can isolate medial and lateral hamstrings",
                "1-2 minutes per leg, can rotate leg to target all compartments",
                "1 minute per leg, can adjust angle for different fibers",
                "10 extensions, hold extended position for 5 seconds each",
                "1 minute per side, coordinate with breathing"
            ]
        }
        
        st.dataframe(foam_roller_data)
        
        st.markdown("""
        ### Foam Roller Progression By Phase

        **Early Phase (Weeks 0-2):**
        - Use light pressure only
        - Avoid rolling directly over the surgical site
        - Focus on non-operated leg and upper body
        - Keep sessions short (1-2 minutes per area)

        **Middle Phase (Weeks 3-6):**
        - Increase pressure gradually
        - Can roll closer to knee but still avoid incision sites
        - Add thoracic extension for improved posture
        - Increase duration to 2-3 minutes per muscle group

        **Late Phase (Weeks 7+):**
        - Full pressure as tolerated
        - Can address all areas including near surgical sites
        - Add dynamic movements (e.g., quad roll with knee bend)
        - Can use before workouts to improve mobility and after for recovery
        """)
    
    # Massage Gun content
    with tabs[1]:
        st.subheader("Massage Gun Protocols")
        
        st.markdown("""
        Percussion therapy with a massage gun helps reduce muscle tension, improve blood flow, and accelerate recovery.
        These protocols can be adjusted based on your tolerance and phase of rehabilitation.
        """)
        
        massage_gun_data = {
            "Area": [
                "Quadriceps",
                "Hamstrings",
                "Calves",
                "IT Band/TFL",
                "Gluteal Region",
                "Upper Trapezius",
                "Around Knee (Later Phases)"
            ],
            "Technique": [
                "Start at low speed, move slowly over entire muscle. Avoid bony prominences. Target vastus medialis oblique specifically.",
                "Focus on muscle belly, avoid directly on tendons. Move in vertical pattern along length of muscle.",
                "Float over gastrocnemius and soleus. Avoid direct pressure on Achilles tendon.",
                "Start at hip and work down lateral thigh. Use lightest pressure as this area is often sensitive.",
                "Work in circular pattern over gluteus maximus, medius, and minimus. Avoid sciatic nerve area.",
                "Use light pressure and slower speed settings for neck/upper back regions.",
                "Only after cleared by physician (typically 6+ weeks). Use lowest setting, focus on quadriceps tendon and patellar tendon attachments."
            ],
            "Protocol": [
                "60-90 seconds per quadriceps, 2-3 times daily",
                "60 seconds per hamstring group, 1-2 times daily",
                "30-60 seconds per calf, 1-2 times daily",
                "30-60 seconds per side, daily",
                "60-90 seconds per side, 1-2 times daily",
                "30-60 seconds, as needed for upper body tension",
                "30 seconds around knee, only after physician clearance"
            ]
        }
        
        st.dataframe(massage_gun_data)
        
        st.markdown("""
        ### Massage Gun Settings By Phase

        **Early Phase (Weeks 0-2):**
        - Use lightest setting (Level 1-2)
        - Avoid directly over surgical area or incisions
        - Keep sessions brief (30-60 seconds per area)
        - Focus on surrounding muscles, not directly on knee

        **Middle Phase (Weeks 3-6):**
        - May increase to medium settings as tolerated
        - Can work closer to knee but still avoid incisions until fully healed
        - Extend sessions to 1-2 minutes per muscle group
        - Target quadriceps and hamstrings specifically

        **Late Phase (Weeks 7+):**
        - Can use higher settings as tolerated
        - May carefully address tissue around knee (with physician clearance)
        - Use before workouts to activate muscles and after for recovery
        - Can combine with stretching for enhanced mobility
        """)
    
    # Pilates/Stability Ball content
    with tabs[2]:
        st.subheader("Pilates/Stability Ball Exercises")
        
        st.markdown("""
        Stability ball exercises challenge balance and core engagement while providing a safe environment for knee rehabilitation. 
        These exercises can be progressed as strength and stability improve.
        """)
        
        stability_ball_data = {
            "Exercise": [
                "Seated Balancing",
                "Wall Squats with Ball",
                "Hamstring Curls",
                "Bridge with Feet on Ball",
                "Hip Abduction Squeeze",
                "Single-Leg Balance on Ball",
                "Core Roll-Outs"
            ],
            "Technique": [
                "Sit on ball with feet flat on floor, find neutral spine. Progress by lifting one foot slightly.",
                "Place ball between wall and lower/mid back, feet shoulder-width apart, slowly bend knees to partial squat.",
                "Lie on back, heels on ball, lift hips and pull ball toward buttocks by bending knees.",
                "Lie on back with calves on ball, lift hips, maintain straight line from shoulders to heels.",
                "Place ball between knees in seated or supine position, squeeze and hold.",
                "Sit on ball, slowly lift non-surgical leg off floor while maintaining balance.",
                "Kneel in front of ball, place forearms on ball, slowly roll forward maintaining core engagement."
            ],
            "Prescription By Phase": [
                "Early: 3 × 30s holds; Middle: Add arm movements; Late: Close eyes for challenge",
                "Early: 3 × 8 (45° bend); Middle: 3 × 12 (60° bend); Late: 3 × 15 (90° bend)",
                "Middle phase only: 2 × 8; Late: 3 × 12 with single-leg progression",
                "Early: Double-leg bridge 2 × 10; Middle: 3 × 12; Late: Single-leg version 2 × 10",
                "All phases: 3 × 15 with 5s holds, progress pressure",
                "Middle: With support 3 × 20s; Late: Without support 3 × 30s",
                "Late phase only: 3 × 8 progressing to further reach as tolerated"
            ]
        }
        
        st.dataframe(stability_ball_data)
        
        st.markdown("""
        ### Pilates Ball Progression By Phase

        **Early Phase (Weeks 0-2):**
        - Seated balance only (with support nearby if needed)
        - Ball squeezes for isometric activation
        - Gentle seated mobility exercises
        - Focus on proper positioning and alignment

        **Middle Phase (Weeks 3-6):**
        - Wall squats with stability ball
        - Bridging with feet on ball
        - Gentle hamstring curls if ROM allows
        - Seated marching on ball

        **Late Phase (Weeks 7+):**
        - Single-leg exercises on ball
        - Dynamic movements with ball
        - Core roll-outs and advanced stability drills
        - Sport-specific balance challenges
        """)
    
    # Small Ball content
    with tabs[3]:
        st.subheader("Small Ball Exercises")
        
        st.markdown("""
        A small ball (tennis ball, lacrosse ball, or soft therapy ball) provides targeted pressure for trigger points 
        and can be used for specific strengthening and proprioception exercises.
        """)
        
        small_ball_data = {
            "Exercise": [
                "Inner Thigh Squeeze",
                "Calf Trigger Point Release",
                "Foot Arch Roll",
                "Terminal Knee Extension",
                "Patellar Mobilization",
                "Glute Med/Min Trigger Point",
                "Hamstring Curl with Ball"
            ],
            "Technique": [
                "Place small ball between knees, squeeze and hold. Can be done seated or lying down.",
                "Sit and place ball under calf, apply pressure on trigger points, can add ankle movements.",
                "Standing (with support) or seated, roll ball under arch of foot.",
                "Place ball behind knee, press knee down to squeeze ball (activates hamstrings isometrically).",
                "Seated with leg extended, place ball beside kneecap, use hands to roll kneecap over ball in different directions.",
                "Lie on side with ball under lateral hip, find tender spots and apply pressure.",
                "Lie on back, place heel on small ball, pull ball toward buttocks by bending knee."
            ],
            "Prescription": [
                "3 × 15 with 5s holds, multiple times daily",
                "60-90 seconds per spot of tension",
                "1-2 minutes per foot, daily",
                "3 × 15 with 5s holds, 3-4 times daily for extension reinforcement",
                "5 directions, 30s each direction (physician clearance needed)",
                "Target 3-4 trigger points, 30s each",
                "Late phase only: 3 × 10 progressing to single-leg as tolerated"
            ]
        }
        
        st.dataframe(small_ball_data)
        
        st.markdown("""
        ### Small Ball Applications By Phase

        **Early Phase (Weeks 0-2):**
        - Terminal knee extension with ball
        - Inner thigh isometrics
        - Foot arch rolling for circulation
        - Gentle calf release (avoiding surgical leg)

        **Middle Phase (Weeks 3-6):**
        - Add patellar mobilization (if approved)
        - More focused trigger point work for quads, hamstrings
        - Gentle hamstring activation with ball
        - Progress pressure on trigger points

        **Late Phase (Weeks 7+):**
        - Dynamic exercises with ball
        - Hamstring curls with ball resistance
        - Balance exercises standing on ball
        - Sport-specific coordination drills
        """)
    
    # Plyometrics content
    with tabs[4]:
        st.subheader("Plyometric Training Progression")
        
        st.markdown("""
        Plyometric training is essential for developing power and preparing for return to martial arts. 
        These exercises should only be started once you have sufficient strength and control.
        """)
        
        plyometric_data = {
            "Stage & Timing": [
                "Stage 1: Weeks 6-9",
                "Stage 2: Weeks 10-14",
                "Stage 3: Weeks 15-18",
                "Stage 4: Weeks 19+"
            ],
            "Exercise Examples": [
                "Double-leg hops in place, Mini squat jumps, Box jumps (up only, step down), Forward/backward line hops",
                "Low depth jumps, Lateral line hops, Alternating lunge jumps, Forward continuous hops, Lateral shuffle jumps",
                "Single-leg hop series, Lateral single-leg hops, Bounding, Multi-directional hops, 90° cutting drills",
                "Depth jumps with reactive jumps, Single-leg hurdle hops, Rotational jumps, Sport-specific reactive drills"
            ],
            "Guidelines": [
                "Low intensity, bilateral, longer ground contact, 30-40 foot contacts/session, 1-2x/week",
                "Medium intensity, transition from bilateral to unilateral, 40-60 foot contacts/session, 2x/week",
                "High intensity, mixed bilateral/unilateral, 60-80 foot contacts/session, 2-3x/week",
                "Maximal intensity, unpredictable movements, 80-100 foot contacts/session, 2-3x/week with 48h recovery"
            ]
        }
        
        st.dataframe(plyometric_data)
        
        st.markdown("""
        ### Martial Arts-Specific Plyometrics (Weeks 16+)

        **Footwork Drills:**
        - Ladder drills with fighting stance
        - Shadow boxing with explosive directional changes
        - Reactive partner mirror drills
        
        **Kicking Progression:**
        - Slow technical kicks → Speed kicks → Power kicks → Combination kicks
        - Front kick progression: Chamber only → Partial extension → Full extension → Multiple kicks
        - Roundhouse kick progression: Chamber only → Low kicks → Mid-level kicks → High kicks
        
        **Sparring Preparation:**
        - Defensive shuffling drills with partner pressure
        - Sprawl to fighting stance (wrestling defense)
        - Jump in-out fighting range drills
        
        **Recovery Protocol:**
        - Always follow plyometric sessions with thorough cool-down
        - Use foam roller and massage gun after plyometric training
        - Monitor knee for 24h after introducing new plyometric exercises
        """)
    
    # Daily Routines content
    with tabs[5]:
        st.subheader("Daily Rehab Routines by Phase")
        
        st.markdown("""
        These sample daily routines incorporate all the equipment-based exercises into structured protocols based on your rehabilitation phase.
        """)
        
        st.markdown("""
        ### Early Phase (Weeks 0-2) Daily Routine

        **Morning Routine (20-30 min):**
        - Terminal knee extension with small ball, 3 × 30s
        - Heel prop for extension, 3 × 30s
        - Gentle quad sets, 3 × 10
        - Ankle pumps and circles, 2 × 15
        - Patellar mobilization (5 directions, as cleared by surgeon)

        **Mid-Day Session (15-20 min):**
        - Seated stability ball balance, 3 × 30s
        - Light massage gun on quads/hamstrings, 60s each
        - Gentle wall slides for flexion, 2 × 10
        - Straight leg raises (if cleared), 2 × 10

        **Evening Routine (25-35 min):**
        - Stationary bike or CPM, 20-30 min
        - Foam roll non-surgical leg, 2 min per area
        - Light massage gun on calves and quads, 60s each
        - Gentle stretching as tolerated
        - Ice/compression as needed
        """)
        
        st.markdown("""
        ### Middle Phase (Weeks 3-6) Daily Routine

        **Morning Routine (25-30 min):**
        - Foam roll quads, hamstrings, IT band, 2 min each
        - Terminal knee extension with ball, 3 × 15
        - Wall squats with stability ball, 3 × 10
        - Single-leg balance work, 3 × 30s each leg
        - Stationary bike, 10 min

        **Mid-Day Session (10-15 min):**
        - Small ball foot rolling, 2 min each foot
        - Quad sets and hamstring sets, 3 × 15 each
        - Chair squats to comfortable depth, 2 × 10
        - Patellar mobilization, all directions

        **Evening Routine (30-40 min):**
        - Stationary bike, 15-20 min
        - Stability ball bridges, 3 × 12
        - Hamstring curls with small ball, 3 × 10
        - Massage gun protocol for all leg muscles, 90s each area
        - Standing heel raises (with support), 3 × 15
        - Terminal stretch for extension/flexion
        """)
        
        st.markdown("""
        ### Late Phase (Weeks 7+) Daily Routine

        **Morning Routine (25-30 min):**
        - Dynamic warm-up with leg swings, arm circles
        - Foam rolling full lower body, 1-2 min per area
        - Stability ball single-leg balance, 3 × 30s each
        - Mini-band exercises (lateral/monster walks), 2 × 15
        - Bodyweight squats and lunges, 2 × 15 each

        **Mid-Day Quick Session (10-15 min):**
        - Targeted massage gun for trouble spots, 2 min
        - Hamstring/quad stretching, 30s holds
        - Light plyometrics (if appropriate day): double-leg hops, 2 × 10

        **Evening Training (45-60 min):**
        - Specific strength training or martial arts practice
        - Post-workout: Stability ball stretching
        - Foam rolling entire lower body
        - Massage gun recovery protocol
        - Ice if any swelling or discomfort
        
        **Weekly Plan Structure:**
        - Mon/Wed/Fri: Strength + appropriate plyometrics
        - Tue/Thu: Active recovery, mobility work, light cardio
        - Sat: Light technical martial arts practice
        - Sun: Full recovery day with foam rolling and massage gun only
        """)
        
        st.markdown("""
        ### Notes on Equipment Use

        - **Foam Roller**: Use more frequently when experiencing muscle tightness
        - **Massage Gun**: Excellent for pre-bed routine to improve overnight recovery
        - **Stability Ball**: Great for active rest days to maintain proprioception
        - **Small Ball**: Keep at desk/workplace for quick 2-min sessions throughout day
        - **Remember**: Quality of movement trumps quantity - focus on perfect form with each exercise
        """)
