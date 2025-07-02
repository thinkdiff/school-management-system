import streamlit as st
from streamlit_option_menu import option_menu
from src.auth.authorization import Authorization
import logging

logger = logging.getLogger(__name__)

def render_sidebar():
    """Render the main sidebar navigation"""
    
    auth = Authorization()
    
    with st.sidebar:
        # Logo and title
        st.markdown("""
        <div class="sidebar-logo">
            <h2>🏫 School Management</h2>
            <p>Welcome back!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User info
        if st.session_state.get('authenticated', False):
            user_data = st.session_state.get('user_data', {})
            st.markdown(f"**👤 {user_data.get('full_name', 'User')}**")
            st.markdown(f"*Role: {user_data.get('role', '').title()}*")
            st.markdown("---")
        
        # Navigation menu
        accessible_pages = auth.get_accessible_pages()
        
        # Convert page names to menu items with icons
        menu_items = []
        icons = []
        
        page_config = {
            'Dashboard': 'house',
            'User Management': 'people',
            'Class Management': 'door-open',
            'Student Management': 'person-workspace',
            'Teacher Management': 'person-badge',
            'My Classes': 'book',
            'Attendance': 'calendar-check',
            'Assignments': 'file-text',
            'Grades': 'graph-up',
            'Students': 'people-fill',
            'Reports': 'bar-chart',
            'Announcements': 'megaphone',
            'System Settings': 'gear',
            'Child Progress': 'person-heart',
            'Communication': 'chat-dots'
        }
        
        for page in accessible_pages:
            if page in page_config:
                menu_items.append(page)
                icons.append(page_config[page])
        
        # Render navigation menu
        if menu_items:
            selected_page = option_menu(
                menu_title=None,
                options=menu_items,
                icons=icons,
                menu_icon="cast",
                default_index=0,
                key="main_menu",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "#667eea", "font-size": "18px"},
                    "nav-link": {
                        "font-size": "16px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#eee"
                    },
                    "nav-link-selected": {"background-color": "#667eea"},
                }
            )
            
            # Store selected page in session state
            st.session_state.current_page = selected_page
        
        st.markdown("---")
        
        # Quick actions based on role
        render_quick_actions(auth)
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            st.session_state.auth.logout_user()
            st.rerun()
        
        # Footer
        st.markdown("""
        <div style="position: absolute; bottom: 10px; left: 10px; right: 10px; text-align: center; color: #666; font-size: 12px;">
            © 2025 School Management System<br>
            Version 1.0.0
        </div>
        """, unsafe_allow_html=True)

def render_quick_actions(auth: Authorization):
    """Render role-specific quick actions"""
    
    role = auth.get_user_role()
    
    st.markdown("**⚡ Quick Actions**")
    
    if role == 'admin':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👥 Add User", use_container_width=True):
                st.session_state.show_add_user_modal = True
        with col2:
            if st.button("🏢 Add Class", use_container_width=True):
                st.session_state.show_add_class_modal = True
    
    elif role == 'teacher':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓️ Mark Attendance", use_container_width=True):
                st.session_state.current_page = 'Attendance'
        with col2:
            if st.button("📝 New Assignment", use_container_width=True):
                st.session_state.show_add_assignment_modal = True
    
    elif role == 'student':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📅 View Schedule", use_container_width=True):
                st.session_state.current_page = 'My Classes'
        with col2:
            if st.button("📊 View Grades", use_container_width=True):
                st.session_state.current_page = 'Grades'
    
    elif role == 'parent':
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 Child Progress", use_container_width=True):
                st.session_state.current_page = 'Child Progress'
        with col2:
            if st.button("💬 Message Teacher", use_container_width=True):
                st.session_state.current_page = 'Communication'