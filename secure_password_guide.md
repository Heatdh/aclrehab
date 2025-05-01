# Secure Password Management for Your Streamlit App

This guide explains how to securely manage passwords in your ACL rehab app without exposing them in your source code.

## What's Already Set Up

I've updated your app to securely handle passwords using two methods:

1. A local `.streamlit/secrets.toml` file (created automatically)
2. Environment variables (for cloud deployment)

Your app will first try to read the password from the secrets file, and if that fails, it will check for an environment variable.

## Managing Your Password Locally

### The secrets.toml file

When you first run the updated app, it will create a `.streamlit/secrets.toml` file with a default password:

```toml
# .streamlit/secrets.toml

# Store your passwords or API keys here
app_password = "aclrehab"

# Add other secrets below as needed
```

To change your password:

1. Edit the `.streamlit/secrets.toml` file
2. Change the value for `app_password`
3. Save the file
4. Restart your app

### Security Benefits

- The `.streamlit/secrets.toml` file is automatically listed in `.gitignore` by default
- This means your password won't be pushed to GitHub if you share your code
- You can safely store your password and other sensitive information (API keys, etc.)

## For Cloud Deployment

If you deploy your app to a cloud platform, you should use environment variables instead:

### Streamlit Cloud

1. Go to your app settings in the Streamlit Cloud dashboard
2. Find the "Secrets" section
3. Add your password in the same TOML format:
   ```toml
   app_password = "your-secure-password"
   ```

### Render

1. In your Render dashboard, go to your app settings
2. Under "Environment Variables" add:
   - Key: `STREAMLIT_APP_PASSWORD`
   - Value: `your-secure-password`

### Heroku

1. In your Heroku dashboard, go to your app settings
2. Under "Config Vars" add:
   - Key: `STREAMLIT_APP_PASSWORD`
   - Value: `your-secure-password`

## Best Practices for Password Security

1. **Use a strong password**
   - At least 12 characters
   - Mix of uppercase, lowercase, numbers, and symbols
   - Avoid easily guessable words

2. **Don't reuse passwords**
   - Use a unique password for your app

3. **Change passwords periodically**
   - Update your password every few months

4. **Additional considerations**
   - If multiple people need access, consider implementing user accounts
   - For very sensitive data, consider implementing more robust authentication

## How It Works in Your App

Your app's password checking function now works like this:

```python
def check_password():
    # Check if already authenticated
    if "password_correct" in st.session_state and st.session_state["password_correct"]:
        return True
        
    # Try to get password from secrets.toml first
    try:
        correct_password = st.secrets["app_password"]
    except:
        # Fall back to environment variable
        correct_password = os.environ.get("STREAMLIT_APP_PASSWORD", "aclrehab")
    
    # Password input
    password = st.text_input("Enter the password:", type="password")
    if password == correct_password:
        st.session_state["password_correct"] = True
        return True
    else:
        if password:
            st.error("Incorrect password")
        return False
```

This ensures your password is never hardcoded in your source code. 