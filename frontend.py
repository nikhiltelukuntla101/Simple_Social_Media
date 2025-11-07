import streamlit as st
import requests
import base64
import urllib.parse

st.set_page_config(page_title="Simple Social", layout="wide")

BASE_URL = "http://localhost:8000"

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = "login"  # Default page


def get_headers():
    """Get authorization headers with token"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


# ------------------- REGISTER PAGE -------------------

def register_page():
    st.title("📝 Create an Account")

    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")
    confirm_password = st.text_input("Confirm Password:", type="password")

    if st.button("Sign Up", type="primary"):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return
        
        signup_data = {"email": email, "password": password}
        response = requests.post(f"{BASE_URL}/auth/register", json=signup_data)

        if response.status_code == 201:
            st.success("🎉 Account created successfully! You can now log in.")
            if st.button("Go to Login"):
                st.session_state.page = "login"
                st.rerun()
        else:
            error = response.json().get("detail", "Registration failed")
            st.error(f"Registration failed: {error}")

    st.markdown("---")
    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


# ------------------- LOGIN PAGE -------------------

def login_page():
    st.title("🚀 Welcome to Simple Social")

    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if st.button("Login", type="primary", use_container_width=True):
        login_data = {"username": email, "password": password}
        response = requests.post(f"{BASE_URL}/auth/jwt/login", data=login_data)

        if response.status_code == 200:
            token_data = response.json()
            st.session_state.token = token_data["access_token"]

            # Get user info
            user_response = requests.get(f"{BASE_URL}/users/me", headers=get_headers())
            if user_response.status_code == 200:
                st.session_state.user = user_response.json()
                st.session_state.page = "feed"
                st.rerun()
            else:
                st.error("Failed to get user info")
        else:
            st.error("Invalid email or password!")

    st.markdown("---")
    if st.button("Go to Register", type="secondary"):
        st.session_state.page = "register"
        st.rerun()


# ------------------- UPLOAD PAGE -------------------

def upload_page():
    st.title("📸 Share Something")

    uploaded_file = st.file_uploader("Choose media", type=['png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'mkv', 'webm'])
    caption = st.text_area("Caption:", placeholder="What's on your mind?")

    if uploaded_file and st.button("Share", type="primary"):
        with st.spinner("Uploading..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"caption": caption}
            response = requests.post(f"{BASE_URL}/upload", files=files, data=data, headers=get_headers())

            if response.status_code == 200:
                st.success("Posted successfully! 🎉")
                st.rerun()
            else:
                st.error("Upload failed!")


# ------------------- FEED PAGE -------------------

def encode_text_for_overlay(text):
    """Encode text for ImageKit overlay - base64 then URL encode"""
    if not text:
        return ""
    base64_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return urllib.parse.quote(base64_text)


def create_transformed_url(original_url, transformation_params, caption=None):
    if caption:
        encoded_caption = encode_text_for_overlay(caption)
        text_overlay = f"l-text,ie-{encoded_caption},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"
        transformation_params = text_overlay

    if not transformation_params:
        return original_url

    parts = original_url.split("/")
    file_path = "/".join(parts[4:])
    base_url = "/".join(parts[:4])
    return f"{base_url}/tr:{transformation_params}/{file_path}"


def feed_page():
    st.title("🏠 Feed")

    response = requests.get(f"{BASE_URL}/feed", headers=get_headers())
    if response.status_code == 200:
        posts = response.json()["posts"]

        if not posts:
            st.info("No posts yet! Be the first to share something.")
            return

        for post in posts:
            st.markdown("---")

            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{post['email']}** • {post['created_at'][:10]}")
            with col2:
                if post.get('is_owner', False):
                    if st.button("🗑️", key=f"delete_{post['id']}", help="Delete post"):
                        response = requests.delete(f"{BASE_URL}/posts/{post['id']}", headers=get_headers())
                        if response.status_code == 200:
                            st.success("Post deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete post!")

            caption = post.get('caption', '')
            if post['file_type'] == 'image':
                uniform_url = create_transformed_url(post['url'], "", caption)
                st.image(uniform_url, width=300)
            else:
                uniform_video_url = create_transformed_url(post['url'], "w-400,h-400,cm-pad_resize,bg-blurred")
                st.video(uniform_video_url, width=300)
                st.caption(caption)
    else:
        st.error("Failed to load feed")


# ------------------- MAIN APP FLOW -------------------

if st.session_state.user is None:
    if st.session_state.page == "register":
        register_page()
    else:
        login_page()
else:
    st.sidebar.title(f"👋 Hi {st.session_state.user['email']}!")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigate:", ["🏠 Feed", "📸 Upload"])

    if page == "🏠 Feed":
        feed_page()
    else:
        upload_page()
