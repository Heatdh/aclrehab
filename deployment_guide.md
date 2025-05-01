# Deploying Your ACL Rehab Streamlit App

This guide provides several options for deploying your Streamlit application.

## Private Deployment Options

If you want your app to be private and accessible only to you, here are the best options:

### 1. Streamlit Cloud Teams (Most Straightforward)

Streamlit Community Cloud offers a paid Teams plan with private app deployment:

1. Sign up for [Streamlit Teams](https://streamlit.io/cloud) (starts at $100/month)
2. Push your code to a private GitHub repository
3. Connect your repository to Streamlit Cloud
4. Deploy as private app with password protection

### 2. Render with Authentication

Render allows you to set up basic authentication:

1. Push your code to a private GitHub repository
2. Create a `requirements.txt` file with dependencies
3. In your Streamlit app, add basic auth code:
   ```python
   import streamlit as st
   import hmac
   
   def check_password():
       """Returns `True` if the user had the correct password."""
       def password_entered():
           """Checks whether a password entered by the user is correct."""
           if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
               st.session_state["password_correct"] = True
               del st.session_state["password"]  # Don't store password
           else:
               st.session_state["password_correct"] = False
   
       if "password_correct" not in st.session_state:
           # First run, show input for password.
           st.text_input(
               "Password", type="password", on_change=password_entered, key="password"
           )
           return False
       elif not st.session_state["password_correct"]:
           # Password not correct, show input + error.
           st.text_input(
               "Password", type="password", on_change=password_entered, key="password"
           )
           st.error("😕 Password incorrect")
           return False
       else:
           # Password correct.
           return True
   
   if not check_password():
       st.stop()  # Don't run the rest of the app
   ```
4. Create a `.streamlit/secrets.toml` file with your password (don't commit this to GitHub):
   ```toml
   password = "your-secret-password"
   ```
5. Deploy to Render with the secret configured in the environment variables

### 3. Self-hosting on a VPS (Most Private)

For complete control and privacy:

1. Rent a Virtual Private Server (VPS) from providers like DigitalOcean, Linode, or AWS EC2 (starts ~$5/month)
2. SSH into your server
3. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
4. Clone your repository
5. Build and run with Docker:
   ```bash
   docker build -t acl-rehab-app .
   docker run -d -p 8501:8501 acl-rehab-app
   ```
6. Set up a reverse proxy with Nginx and SSL:
   ```bash
   sudo apt-get install nginx certbot python3-certbot-nginx
   ```
7. Configure Nginx to require basic authentication and proxy to your Streamlit app
8. Access via your domain with username/password

### 4. Local Deployment (Completely Private)

If you only need to access from your own computer:

1. Simply run the app locally with:
   ```bash
   streamlit run app.py
   ```
2. For occasional remote access, use a tool like ngrok:
   ```bash
   ngrok http 8501
   ```
   This creates a temporary public URL for your local app

## Option 1: Streamlit Cloud (Easiest)

[Streamlit Cloud](https://streamlit.io/cloud) provides free hosting for public Github repositories.

1. Push your code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Sign in with GitHub, Google, etc.
4. Click "New app"
5. Select your repository, branch, and main file path (e.g., `app.py`)
6. Click "Deploy"

Your app will be available at a `streamlit.app` URL.

## Option 2: Render (Simple, Free Tier Available)

[Render](https://render.com/) offers a straightforward deployment process:

1. Push your code to GitHub
2. Create a `requirements.txt` file with your dependencies
3. Sign up for Render and connect your GitHub repository
4. Create a new Web Service
5. Select Python and use the following as the start command:
   ```
   streamlit run app.py
   ```
6. Choose your plan (there's a free tier available)
7. Click "Create Web Service"

## Option 3: Heroku (More Control)

To deploy on Heroku:

1. Create a `requirements.txt` with all dependencies
2. Create a `Procfile` containing:
   ```
   web: streamlit run app.py --server.port=$PORT
   ```
3. Create a `setup.sh` file:
   ```
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   " > ~/.streamlit/config.toml
   ```
4. Push to GitHub or deploy directly using Heroku CLI

## Option 4: Docker (Full Control)

For more control, especially for development/testing:

1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY . .
   RUN pip install -r requirements.txt
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "app.py"]
   ```
2. Build and run the container:
   ```
   docker build -t acl-rehab-app .
   docker run -p 8501:8501 acl-rehab-app
   ```
3. Deploy to any cloud provider that supports Docker containers

## Important Notes for Your App

Before deploying:

1. Ensure your file paths use relative paths (e.g., `data/exercise_log.csv`)
2. Create a `requirements.txt` file with all dependencies:
   ```
   streamlit==1.27.0
   pandas==2.0.3
   numpy==1.24.3
   matplotlib==3.7.2
   ```
3. Make sure any data folders needed by your app are created if they don't exist:
   ```python
   import os
   if not os.path.exists('data'):
       os.makedirs('data')
   ```
4. For persistence, consider using cloud storage services instead of local files, as most deployments use ephemeral file systems.

## Data Persistence Options

Since your app saves exercise data to CSV files, you'll need to consider data persistence:

1. **Streamlit-specific solutions**:
   - Use Streamlit's `st.cache_data.persist` for simple persistence
   - For Streamlit Cloud, consider [connecting to a database](https://docs.streamlit.io/knowledge-base/tutorials/databases)

2. **Cloud database options**:
   - SQLite with GitHub integration (for small apps)
   - MongoDB Atlas (free tier available)
   - Supabase or Firebase (easy setup)

3. **File storage options**:
   - AWS S3
   - Google Cloud Storage
   - Dropbox API
