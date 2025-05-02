import os
import pymongo
import streamlit as st
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB Connection String
# Try to get from environment variables or .streamlit/secrets.toml
def get_mongo_uri():
    try:
        # Try to get from Streamlit secrets
        uri = st.secrets.get("mongo_uri", None)
        if uri:
            return uri
    except:
        pass
    
    # Try to get from environment variable
    uri = os.environ.get("MONGO_URI")
    if uri:
        return uri
    
    # Default connection string (localhost)
    return "mongodb://localhost:27017"

# Initialize database connection
@st.cache_resource
def init_connection():
    try:
        uri = get_mongo_uri()
        # Add SSL configuration to handle connection issues
        client = MongoClient(
            uri,
            tlsAllowInvalidCertificates=True  # This bypasses certificate validation
        )
        # Test the connection
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

# Get database
def get_database():
    client = init_connection()
    if client:
        return client.acl_rehab_db
    return None

# User authentication functions
def hash_password(password):
    return pbkdf2_sha256.hash(password)

def verify_password(stored_password, provided_password):
    return pbkdf2_sha256.verify(provided_password, stored_password)

# User management
def create_user(username, password, email=None):
    db = get_database()
    if db is None:
        return False, "Database connection failed"
    
    # Check if user already exists
    if db.users.find_one({"username": username}):
        return False, "Username already exists"
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Create user document
    user = {
        "username": username,
        "password": hashed_password,
        "email": email,
        "created_at": datetime.now()
    }
    
    try:
        db.users.insert_one(user)
        return True, "User created successfully"
    except Exception as e:
        return False, f"Error creating user: {e}"

def authenticate_user(username, password):
    db = get_database()
    if db is None:
        return False, "Database connection failed"
    
    user = db.users.find_one({"username": username})
    if not user:
        return False, "User not found"
    
    if verify_password(user["password"], password):
        return True, user
    else:
        return False, "Incorrect password"

# Data management functions
def save_user_profile(username, profile_data):
    db = get_database()
    if db is None:
        return False, "Database connection failed"
    
    try:
        # Convert profile_data DataFrame to dictionary for MongoDB
        profile_dict = profile_data.to_dict(orient='records')[0]
        profile_dict['username'] = username
        
        # Use upsert to create or update profile
        db.profiles.update_one(
            {"username": username},
            {"$set": profile_dict},
            upsert=True
        )
        return True, "Profile saved successfully"
    except Exception as e:
        return False, f"Error saving profile: {e}"

def get_user_profile(username):
    db = get_database()
    if db is None:
        return None
    
    try:
        profile = db.profiles.find_one({"username": username})
        if profile:
            # Convert MongoDB document to DataFrame (excluding _id field)
            profile.pop('_id', None)
            return pd.DataFrame([profile])
        return pd.DataFrame({
            'name': [''],
            'age': [30],
            'weight': [70.0],
            'height': [170.0],
            'surgery_date': [''],
            'injury_type': ['ACL Tear'],
            'username': [username]
        })
    except Exception as e:
        st.error(f"Error retrieving profile: {e}")
        return None

def save_exercise_log(username, exercise_data):
    db = get_database()
    if db is None:
        return False, "Database connection failed"
    
    try:
        # Convert exercise_data DataFrame to list of dictionaries for MongoDB
        exercise_records = exercise_data.to_dict(orient='records')
        
        # Add username to each record
        for record in exercise_records:
            record['username'] = username
        
        # Delete existing records for this user
        db.exercises.delete_many({"username": username})
        
        # Insert all records
        if exercise_records:
            db.exercises.insert_many(exercise_records)
        
        return True, "Exercise log saved successfully"
    except Exception as e:
        return False, f"Error saving exercise log: {e}"

def get_exercise_log(username):
    db = get_database()
    if db is None:
        return pd.DataFrame(columns=[
            'date', 'category', 'exercise', 'sets', 'reps', 'weight', 'notes', 'username'
        ])
    
    try:
        exercises = list(db.exercises.find({"username": username}))
        if exercises:
            # Convert MongoDB documents to DataFrame
            for exercise in exercises:
                exercise.pop('_id', None)
            return pd.DataFrame(exercises)
        return pd.DataFrame(columns=[
            'date', 'category', 'exercise', 'sets', 'reps', 'weight', 'notes', 'username'
        ])
    except Exception as e:
        st.error(f"Error retrieving exercise log: {e}")
        return pd.DataFrame(columns=[
            'date', 'category', 'exercise', 'sets', 'reps', 'weight', 'notes', 'username'
        ])

def save_rom_pain_log(username, rom_pain_data):
    db = get_database()
    if db is None:
        return False, "Database connection failed"
    
    try:
        # Convert rom_pain_data DataFrame to list of dictionaries for MongoDB
        rom_pain_records = rom_pain_data.to_dict(orient='records')
        
        # Add username to each record
        for record in rom_pain_records:
            record['username'] = username
        
        # Delete existing records for this user
        db.rom_pain.delete_many({"username": username})
        
        # Insert all records
        if rom_pain_records:
            db.rom_pain.insert_many(rom_pain_records)
        
        return True, "ROM and pain log saved successfully"
    except Exception as e:
        return False, f"Error saving ROM and pain log: {e}"

def get_rom_pain_log(username):
    db = get_database()
    if db is None:
        return pd.DataFrame(columns=[
            'date', 'extension_angle', 'flexion_angle', 'pain_level', 'swelling', 'notes', 'username'
        ])
    
    try:
        rom_pain = list(db.rom_pain.find({"username": username}))
        if rom_pain:
            # Convert MongoDB documents to DataFrame
            for entry in rom_pain:
                entry.pop('_id', None)
            return pd.DataFrame(rom_pain)
        return pd.DataFrame(columns=[
            'date', 'extension_angle', 'flexion_angle', 'pain_level', 'swelling', 'notes', 'username'
        ])
    except Exception as e:
        st.error(f"Error retrieving ROM and pain log: {e}")
        return pd.DataFrame(columns=[
            'date', 'extension_angle', 'flexion_angle', 'pain_level', 'swelling', 'notes', 'username'
        ])

def remove_exercise_entry(username, date, exercise):
    db = get_database()
    if db is None:
        return False, "Database connection failed"
    
    try:
        result = db.exercises.delete_one({
            "username": username, 
            "date": date, 
            "exercise": exercise
        })
        
        if result.deleted_count > 0:
            return True, f"Exercise entry removed successfully"
        else:
            return False, "Entry not found"
    except Exception as e:
        return False, f"Error removing exercise entry: {e}"

def remove_rom_pain_entry(username, date):
    db = get_database()
    if db is None:
        return False, "Database connection failed"
    
    try:
        result = db.rom_pain.delete_one({
            "username": username, 
            "date": date
        })
        
        if result.deleted_count > 0:
            return True, f"ROM/Pain entry removed successfully"
        else:
            return False, "Entry not found"
    except Exception as e:
        return False, f"Error removing ROM/Pain entry: {e}"

def get_user_list():
    db = get_database()
    if db is None:
        return []
    
    try:
        # Get all profile documents
        profiles = list(db.profiles.find({}, {"username": 1, "name": 1}))
        return [{"username": p.get("username"), "name": p.get("name", "")} for p in profiles]
    except Exception as e:
        st.error(f"Error retrieving user list: {e}")
        return []
