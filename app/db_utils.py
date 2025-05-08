import pandas as pd
import os
import streamlit as st

def get_rom_pain_log(username):
    """Get ROM and pain log for a user"""
    try:
        if mongodb_connected:
            # Get from MongoDB
            user_data = users_collection.find_one({"username": username})
            if user_data and "rom_pain_log" in user_data:
                # Convert dates to datetime when loading from MongoDB
                df = pd.DataFrame(user_data["rom_pain_log"])
                if not df.empty and 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                return df
        else:
            # Get from local file
            file_path = f"data/{username}_rom_pain_log.csv"
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                if not df.empty and 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                return df
    except Exception as e:
        st.error(f"Error loading ROM and pain log: {e}")
    return pd.DataFrame()

def save_rom_pain_log(username, df):
    """Save ROM and pain log for a user"""
    try:
        if mongodb_connected:
            # Convert DataFrame to dict for MongoDB
            log_data = df.copy()
            if not log_data.empty and 'date' in log_data.columns:
                log_data['date'] = log_data['date'].dt.strftime('%Y-%m-%d')
            users_collection.update_one(
                {"username": username},
                {"$set": {"rom_pain_log": log_data.to_dict('records')}}
            )
        else:
            # Save to local file
            file_path = f"data/{username}_rom_pain_log.csv"
            df.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"Error saving ROM and pain log: {e}") 