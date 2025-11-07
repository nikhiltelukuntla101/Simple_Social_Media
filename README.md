# 🌐 Simple Social Media App

A **mini full-stack social media application** built using **FastAPI** (backend) and **Streamlit** (frontend).  
Users can register, log in, upload images or videos, view posts from all users in a feed, and delete their own posts.  
Media files are stored securely in **ImageKit**, and authentication is handled using **FastAPI Users** with JWT tokens.

---

## 🚀 Features

✅ User registration and login (JWT-based)  
✅ Upload images and videos to ImageKit  
✅ View all posts in a global feed  
✅ Delete your own posts only  
✅ Secure authentication with `fastapi-users`  
✅ Environment-based secret management with `.env`  
✅ Streamlit frontend with live API integration

---

## 🧠 Tech Stack

| Layer                      | Technology              |
| :------------------------- | :---------------------- |
| **Frontend**               | Streamlit               |
| **Backend**                | FastAPI                 |
| **Database**               | SQLite (SQLAlchemy ORM) |
| **Auth**                   | FastAPI Users + JWT     |
| **Media Storage**          | ImageKit                |
| **Environment Management** | python-dotenv           |
| **Language**               | Python 3.11+            |

---

## 📁 Folder Structure

small-social/
│
├── app/
│ ├── app.py # FastAPI main app
│ ├── db.py # Database models and session
│ ├── images.py # ImageKit configuration
│ ├── users.py # Auth and user manager
│ ├── schemas.py # Pydantic schemas
│
├── frontend/
│ ├── streamlit_app.py # Streamlit web app
│
├── .env # Environment variables (ignored in git)
├── .env.example # Example env file
├── .gitignore
├── pyproject.toml / uv.lock # Dependencies
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/nikhiltelukuntla101/Simple_Social_Media.git
cd Simple_Social_Media


uv venv
source .venv/bin/activate  # (Linux/macOS)
.venv\Scripts\activate     # (Windows)
```

uv pip install -r requirements.txt

# or

pip install fastapi uvicorn streamlit sqlalchemy aiosqlite imagekitio python-dotenv fastapi-users

SECRET=your_jwt_secret_key
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL=your_imagekit_url

uvicorn app.app:app --reload
streamlit run frontend/streamlit_app.py
