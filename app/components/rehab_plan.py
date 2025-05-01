import streamlit as st
import pandas as pd

def show_rehab_plan():
    st.title("ACL Rehabilitation Plan")
    
    st.markdown("""
    This comprehensive rehabilitation plan is designed for ACL recovery with special focus on arthrofibrosis prevention.
    It incorporates daily mobility work, progressive strength training, and sport-specific exercises for martial arts return.
    """)
    
    # Key principles section
    st.header("Key Principles")
    
    principles_data = {
        "Principle": [
            "Early, frequent terminal-extension work",
            "High-frequency ROM, low joint load",
            "Daily patellar & scar-track mobilisations",
            "Criterion-based loading",
            "Anti-inflammatory & pain control",
            "Continuous Passive Motion (CPM) or frequent pedal cycling"
        ],
        "Why It Matters": [
            "Extension loss is the hallmark of cyclops/AF; restoring 0° fast prevents re-scarring",
            "Adhesive tissue reforms in <72h without motion",
            "The patella must glide for flex-ext symmetry",
            "Strength gains mean nothing if ROM is lost",
            "Swelling = fibroblast trigger",
            "Provides gentle, long-duration stretch; strongest evidence in post-lysis AF patients"
        ],
        "How We'll Apply It": [
            "\"Heel-prop\" blocks, prone hangs ≥6×/day, extension board overnight",
            "Stationary bike/CPM or pedal-trainer every 2-3h while awake",
            "Self-mobilise 5 directions × 1 min; add instrument-assisted or massage-gun to quads/ITB when skin healed",
            "You only progress resistance when the day-after ROM is unchanged",
            "Ice/compression 15 min on/45 min off, short NSAID course per MD, Omega-3 & collagen already in place",
            "Use the pedal trainer/CPM ≥4 h/day during Weeks 0-2"
        ]
    }
    
    principles_df = pd.DataFrame(principles_data)
    st.table(principles_df)
    
    # Create tabs for different phases
    tabs = st.tabs([
        "Pre-op", 
        "Surgery Day", 
        "Phase 0 (Days 0-6)", 
        "Phase 1 (Weeks 1-2)",
        "Phase 2 (Weeks 3-6)",
        "Phase 3 (Weeks 7-12)",
        "Phase 4 (Weeks 13-20)",
        "Phase 5 (Months 6-9)",
        "Pain Management"
    ])
    
    # Pre-op content
    with tabs[0]:
        st.subheader("Pre-op \"Pre-habilitation\" (Week -2 to -1)")
        
        st.markdown("""
        **Goals**: ↓ swelling/inflammation, achieve ≤ 3° flexion contracture, ≥ 130° flexion, prime hip/core strength, arrive with quiet knee.
        
        ### Daily Mobility (2-3 mini-sessions)
        
        **Terminal-knee-extension circuit** (6 rounds/day):
        - Heel-prop on rolled towel, 3 × 30s holds
        - Prone hang off bed, 3 × 30s
        - EMS quad set (Russian or 50 Hz, 10s on/50s off × 10 min)
        
        **Flexion circuit**:
        - Wall-slides or supine heel-slides, 3 × 15
        - Pedal trainer 10-15 min no resistance every evening
        
        **Patellar mobs & soft-tissue**:
        - 5 directions, 60s each
        - Foam-roll quads/ITB, massage-gun glute-med, hamstrings, calf
        """)
        
        st.markdown("### Strength & Conditioning (4 gym days, upper + contralateral leg normal intensity)")
        
        strength_data = {
            "Lift": [
                "Rear-foot-elevated split squat (uninvolved)",
                "Hip-thrust / glute bridge (bilateral)",
                "Romanian dead-lift",
                "Core: Pallof press, dead-bug, farmer carry"
            ],
            "Dose": [
                "4 × 8-10",
                "4 × 12",
                "3 × 8",
                "3 rounds"
            ],
            "Notes": [
                "Maintain leg symmetry",
                "Place bar above pelvis, keep knee <70° flexion",
                "Hamstring strength without knee shear",
                "Anti-rotation & bracing"
            ]
        }
        
        strength_df = pd.DataFrame(strength_data)
        st.table(strength_df)
        
        st.info("Finish each session with 10 min pedal trainer at 80 rpm to flush joint.")
    
    # Surgery Day content
    with tabs[1]:
        st.subheader("Surgery Day")
        
        st.markdown("""
        - Ask OR staff to measure intra-op extension lag so you know your "true zero."
        - Confirm you will leave theatre with a drain, cryo-cuff, and written lysis-of-adhesions protocol.
        """)
    
    # Phase 0 content
    with tabs[2]:
        st.subheader("Phase 0: Week 0 (Days 0-6) — \"Motion is medicine\"")
        
        st.markdown("### Targets by Day 6")
        
        targets_data = {
            "Target": [
                "Extension = 0°, flexion ≥ 90°",
                "WBAT with 2 crutches",
                "Effusion ≤ +1",
                "Pain ≤ 3/10 at rest"
            ],
            "Interventions": [
                "• CPM/pedal trainer 20-30 min every 2h while awake (aim +5° flex/day)",
                "• Quad setting with EMS (10 min every hour you're seated)",
                "• Cryo-cuff or ice-bath 15 min on/45 min off",
                "• Patellar mobs & scar massage around portals (start Day 3 once incisions sealed)\n• Ankle pumps, straight-leg raise-lock (ensure no ext. lag)"
            ]
        }
        
        targets_df = pd.DataFrame(targets_data)
        st.table(targets_df)
        
        st.warning("**Red-flags**: can't achieve 0° by Day 3 → call surgeon.")
    
    # Phase 1 content
    with tabs[3]:
        st.subheader("Phase 1: Weeks 1-2 — Early Motion & Progressive Weight-Bearing")
        
        st.markdown("**Goals**: maintain 0° ext, reach 110-120° flex; normalize gait without crutches.")
        
        phase1_data = {
            "Modality": [
                "ROM",
                "Strength (daily micro-dosing)",
                "Gym (2 light lower-body sessions/wk)",
                "Recovery / scar-control",
                "Milestone test end Week 2"
            ],
            "Prescription": [
                "• CPM/pedal trainer 3-4 h/day (can be broken up)\n• Stationary bike full revolutions as soon as 105° flex reached",
                "• Quad set into extension board 3 × 15\n• Straight-leg raise 4 planes 3 × 10\n• Glute bridge on yoga mat 3 × 12",
                "• Body-weight box squat to 45° 3 × 10\n• Standing hip abduction with band 3 × 15\n• Seated calf raise 3 × 12",
                "• Scar mobilisation with vitamin E oil\n• Foam-roll/massage-gun quads/ITB daily\n• NSAIDs if night swelling (MD clearance)",
                "> 120° flex, ext. 0°, single-leg raise hold 30s"
            ]
        }
        
        phase1_df = pd.DataFrame(phase1_data)
        st.table(phase1_df)
        
        st.info("**Rationale**: Rapid early ROM lowers re-operation risk and improves PROs, especially when lysis is performed >3 months from the index ACLR.")
    
    # Phase 2 content
    with tabs[4]:
        st.subheader("Phase 2: Weeks 3-6 — Progressive Loading & Enhanced Mobility")
        
        st.markdown("**Targets**: flexion 125-135°, begin load-bearing squats to 60°, discontinue CPM when flex ≥ 125° two consecutive mornings.")
        
        st.markdown("""
        ### Strength (3 × wk)
        
        - Goblet squat 0-60° 4 × 8
        - Romanian DL 4 × 8
        - Leg-press 0-60° sled-type 3 × 10 (start 30% BW → +10%/wk if no next-day stiffness)
        - Single-leg heel-raised bridge 3 × 12
        - Core: side-plank & bird-dog circuits
        
        ### Neuromuscular & Balance
        
        - Mini-trampoline weight-shift
        - Single-leg balance eyes-open 3 × 45s
        
        ### Cardio & Recovery
        
        - Stationary bike 20-30 min, HR 60-70% max
        - Add deep-water running if available
        - Continue foam-roll/massage-gun around portals
        - Add spike-ball under hamstrings
        """)
        
        st.success("**Milestone end Week 6**: pain-free reciprocal stair ascent/descent, knee flex ≥ 135°, Y-balance ⩾90% contralateral.")
    
    # Phase 3 content
    with tabs[5]:
        st.subheader("Phase 3: Weeks 7-12 — \"Strength Normalisation\"")
        
        st.markdown("**Targets**: symmetric ROM, closed-chain strength ≥ 80% contra-side, effusion 0.")
        
        phase3_data = {
            "Category": [
                "Lower-body strength (3 days/wk)",
                "Hip & posterior chain",
                "Plyo prep",
                "Conditioning",
                "Scar management",
                "Milestones Week 12"
            ],
            "Prescription / progression": [
                "• Back squat 0-90°: start empty bar × 15, add 10 kg/session if next-day ROM unchanged.\n• Leg-press full depth to tolerance.\n• Walking lunges with dumbbells → deficit reverse-lunge.",
                "• Hip-thrust 4 × 10\n• Nordic hamstring (band-assisted) 3 × 6",
                "• Mini-hops in sagittal plane, pogo jumps (both legs) 2 × 20",
                "• Elliptical/rower 25-35 min; aim BW×1.5 × 10 min watt-minutes",
                "• IASTM or Graston quads/quad-tendon weekly (physio)",
                "• SL leg-press 1.5×BW for 5\n• Single-leg squat to 60° with neutral pelvis\n• Hop-for-distance ⩾75% contra-side"
            ]
        }
        
        phase3_df = pd.DataFrame(phase3_data)
        st.table(phase3_df)
        
        st.markdown("""
        ### Martial Arts-Specific Exercises
        
        - Shadow boxing with controlled footwork (no pivoting on surgical leg)
        - Slow, controlled kicks with non-surgical leg
        - Upper body bag/pad work in stable stance
        - Balance drills in fighting stance
        """)
    
    # Phase 4 content
    with tabs[6]:
        st.subheader("Phase 4: Weeks 13-20 — \"Power & Return to Loading\"")
        
        st.markdown("**Goals**: symmetrical hop tests > 90%, resume jog-to-run, integrate sporting patterns.")
        
        st.markdown("""
        ### Programming
        
        **Plyometrics**:
        - Drop-jump (start low, progress to medium height)
        - Lateral bounds (controlled, then with increasing distance)
        - Box jump (30 cm → 50 cm)
        
        **Strength**:
        - Linear periodisation 3-week waves (e.g., 4×6 → 5×5 → 6×4)
        - Heavy compound lifts (squats, deadlifts, lunges)
        - Single-leg strength focus (split squats, step-ups)
        
        **Agility**:
        - Ladder drills (forward, lateral, diagonal patterns)
        - Cone cutting at 50% speed → 75%
        - Martial arts footwork drills with increasing speed
        
        **Load Management**:
        - 10% rule—weekly total lower-body tonnage or running volume ↑ ≤10%
        - Monitor next-day knee symptoms and adjust accordingly
        """)
        
        st.success("**Milestones Week 20**: triple-hop, crossover-hop, timed‐hop all > 90% LSI; isokinetic quad peak torque > 85% body-weight.")
    
    # Phase 5 content
    with tabs[7]:
        st.subheader("Phase 5: Months 6-9 — \"Return to Sport/Impact\"")
        
        st.markdown("""
        Pass full test battery (IKDC, KOOS, ACL-RSI) → gradual return to field sports.
        
        ### Martial Arts Return Protocol
        
        **Month 6-7**:
        - Technical sparring with controlled intensity
        - Progressive kicking combinations with surgical leg
        - Light controlled sparring with trusted partners
        - Defensive movement and countering drills
        
        **Month 7-8**:
        - Moderate sparring with protective knee brace
        - Full technical combinations with power
        - Simulated match conditions with limited contact
        
        **Month 8-9**:
        - Full sparring/competition preparation
        - Sport-specific conditioning with full intensity
        - Competitive return with appropriate medical clearance
        
        **Lifetime Maintenance**:
        - Maintain ROM block: 5 min heel-props + 10 min bike as warm-up every session (lifetime habit to keep scar tissue silent)
        - Consistent hamstring and quad strengthening routine
        - Proper warm-up and recovery protocols before/after training
        """)
    
    # Pain management content
    with tabs[8]:
        st.subheader("Pain & Swelling Decision Tree")
        
        pain_data = {
            "Symptom": [
                "Sunrise swelling > 1 cm girth diff",
                "Night pain > 3/10",
                "Extension loss ≥ 3° 2 days in a row"
            ],
            "Immediate Action": [
                "Skip resistance that day, double bike ROM blocks",
                "Ice + NSAID (MD approved), elevate",
                "Urgent physio; may need MUA before 3-week mark"
            ],
            "Next Day": [
                "If still swollen, drop back to prior week's loads",
                "Check ROM AM; if ext. lag > 2°, schedule physio/manual session",
                ""
            ]
        }
        
        pain_df = pd.DataFrame(pain_data)
        st.table(pain_df)
        
        st.markdown("""
        ### Evidence & Tips
        
        - Early post-lysis protocols call for PT 5 days/wk for the first 2 weeks and unrestricted ROM from Day 1
        - Patients who regained 0° extension by Week 2 after lysis had significantly lower re-operation rates
        - Continuous passive motion after arthrofibrosis release is medically accepted when active PT is limited
        - Rehab success hinges on early motion, fast quad activation and patella mobilisation
        
        **Final Tips**:
        - Train the opposite leg hard—cross-education preserves ~15% strength in the involved limb
        - Log morning extension, flexion & circumference daily for the first 6 weeks
        - Keep soft-tissue tools handy at your desk; 2-min quads massage every hour beats 1 long session
        - Stay patient: most scar-release cases hit "normal" flexion at 8-10 weeks, not 4-6 weeks like standard ACLR
        - A setback ≠ failure—just drop back one micro-phase and re-progress
        """)
