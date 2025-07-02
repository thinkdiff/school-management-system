import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import application modules
from src.auth.authentication import Authentication
from src.ui.sidebar import render_sidebar
from src.ui.dashboard import render_dashboard
from src.config.settings import Settings

def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="School Management System",
        page_icon="🏫",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize settings
    settings = Settings()
    
    # Initialize authentication
    if 'auth' not in st.session_state:
        st.session_state.auth = Authentication()
    
    # Authentication state management
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    # Main application logic
    if not st.session_state.authenticated:
        # Show login page
        show_login_page()
    else:
        # Show main application
        show_main_app()

def show_login_page():
    """Display login page"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏫 School Management System</h1>
        <p>Secure Login Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            remember_me = st.checkbox("Remember me")
            
            submit_button = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submit_button:
                if username and password:
                    # Authenticate user
                    user_data = st.session_state.auth.authenticate_user(username, password)
                    
                    if user_data:
                        st.session_state.authenticated = True
                        st.session_state.user_data = user_data
                        logger.info(f"User {username} logged in successfully")
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                        logger.warning(f"Failed login attempt for username: {username}")
                else:
                    st.error("Please enter both username and password")
        
        # Demo credentials info
        with st.expander("Demo Credentials"):
            st.markdown("""
            **Admin**: admin / admin123  
            **Teacher**: teacher1 / teacher123  
            **Student**: student1 / student123  
            **Parent**: parent1 / parent123  
            """)

def show_main_app():
    """Display main application interface"""
    
    # Sidebar
    render_sidebar()
    
    # Main content area
    render_dashboard()
    
    # Auto-logout after session timeout
    check_session_timeout()

def check_session_timeout():
    """Check if session has timed out"""
    if 'last_activity' not in st.session_state:
        st.session_state.last_activity = datetime.now()
    
    # Check timeout (30 minutes default)
    timeout_minutes = int(os.getenv('SESSION_TIMEOUT_MINUTES', 30))
    if (datetime.now() - st.session_state.last_activity).seconds > (timeout_minutes * 60):
        st.session_state.authenticated = False
        st.session_state.user_data = None
        st.warning("Session expired. Please login again.")
        st.rerun()
    
    # Update last activity
    st.session_state.last_activity = datetime.now()

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred. Please check the logs and try again.")