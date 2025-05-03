# ACL Rehabilitation Tracker

A comprehensive web application for tracking your ACL rehabilitation progress. Built with Streamlit and designed to help users monitor exercises, range of motion, pain levels, and follow a structured rehab plan.

![ACL Rehab Tracker Screenshot](app/images/screenshot.png)

## Features

- **User Profiles**: Store personal details and surgery information
- **Exercise Tracker**: Log workouts with sets, reps, weights and difficulty
- **ROM & Pain Tracker**: Monitor knee extension, flexion and symptom progress
- **Progress Dashboard**: Visualize recovery metrics with interactive charts
- **Rehabilitation Plan**: Comprehensive phase-by-phase ACL recovery protocol
- **Equipment & Exercises**: Database of exercises organized by category

## Modern UI

The application features a modern, card-based UI with:
- Responsive fitness-themed layout
- Progress metrics with visual indicators
- Achievement cards for motivation
- Interactive exercise history
- Modern color scheme and animations

## Setup Instructions

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv stream
   ```
3. Activate the environment:
   - Windows: `stream\Scripts\activate`
   - Mac/Linux: `source stream/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   streamlit run app.py
   ```

## Data Storage

The app stores data in CSV files by default. MongoDB integration is available but optional.

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- NumPy
- Plotly
- Matplotlib
- Streamlit Option Menu

## License

MIT License 