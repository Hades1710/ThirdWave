# Bright Side

<p align="center">
  <img src="https://img.shields.io/badge/Empowering%20Students-Bright%20Side-blueviolet?style=for-the-badge" alt="Bright Side" />
</p>

## 🚀 Overview
Bright Side is a modern, full-stack student dashboard designed to empower students with analytics, emotional intelligence tools, quizzes, and more. Built with React, TypeScript, Vite, Tailwind CSS, and a FastAPI backend, it offers a seamless and interactive experience.

---

## ✨ Features
- 📊 **Analytics Dashboard**: Visualize your progress and performance.
- 🤖 **Debate & EQ Bots**: AI-powered bots for debate and emotional intelligence support.
- 📝 **Quizzes**: Test your knowledge and track improvement.
- 📚 **Resources**: Curated learning materials.
- ⚡ **Emergency Notification**: FastAPI backend for real-time alerts.
- 🔒 **Authentication**: Secure login and signup.

---

## 🛠️ Tech Stack
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Chart.js
- **Backend**: FastAPI, Python
- **Database**:SQLite
- **APIs**: OpenAI, Groq, HuggingFace

---

## 🚦 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Harshlilha/Bright-Side.git
cd Bright-Side
```

### 2. Setup Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

### 3. Install Frontend Dependencies
```bash
npm install
```

### 4. Start the Frontend
```bash
npm run dev
```

### 5. Setup & Run Backend
```bash
cd python_backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python api.py
```

---

## 📂 Project Structure
```
BrightSide-main/
  ├── src/                # Frontend source code
  ├── python_backend/     # FastAPI backend
  ├── public/             # Static assets
  ├── .env.example        # Example environment variables
  └── ...
```

---

## 🤝 Contributing
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License
This project is licensed under the MIT License.

<p align="center">
  <b>Bright Side — Empowering Students, One Click at a Time!</b>
</p>
