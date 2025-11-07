# 🌐 Simple Social Media App

A basic social media web app built with **FastAPI** (backend) and **Streamlit** (frontend).  
Users can register, log in, upload images or videos, view posts, and delete their own posts.  
Media is stored using **ImageKit**, and authentication is handled with **FastAPI Users (JWT)**.

---

## 🚀 Features

- User registration & login
- Upload images and videos
- View all posts in a feed
- Delete your own posts
- Secure authentication (JWT)
- Environment variable management with `.env`

---

## 🧠 Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Database:** SQLite (SQLAlchemy)
- **Auth:** FastAPI Users + JWT
- **Media Storage:** ImageKit
- **Language:** Python 3.11+

---

---

## ⚙️ Setup

```bash
# Clone the repository
git clone https://github.com/nikhiltelukuntla101/Simple_Social_Media.git
cd Simple_Social_Media

# Create virtual environment
uv venv
source .venv/bin/activate  # (Linux/macOS)
.venv\Scripts\activate     # (Windows)

# Install dependencies
uv pip install -r requirements.txt


SECRET=your_jwt_secret_key
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL=your_imagekit_url

# Start backend
uvicorn app.app:app --reload

# Start frontend
streamlit run frontend/streamlit_app.py
```
