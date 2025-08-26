# Bright Side

<p align="center">
  <img src="https://img.shields.io/badge/Empowering%20Students-Bright%20Side-blueviolet?style=for-the-badge" alt="Bright Side" />
</p>

## 🚀 Overview
Bright Side is a modern, full-stack student dashboard designed to empower students with analytics, emotional intelligence tools, quizzes, and more. Built with React, TypeScript, Vite, Tailwind CSS, and a FastAPI backend, it offers a seamless and interactive experience.

---

## ✨ Features  

- 📊 **Analytics Dashboard**  
  Get a clear picture of your growth over time with interactive charts and insights.  
  - Tracks **debate scores**, **EQ levels**, and **progress trends**.  
  - Provides **visual breakdowns** of strengths (logic, empathy, tone) and areas for improvement.  
  - Encourages students to monitor their performance just like a fitness tracker — but for communication skills.  

- 🤖 **Debate & EQ Bots**  
  Practice debates with an AI-powered coach that analyzes both **what you say** and **how you say it**.  
  - Gives **real-time argument feedback** (clarity, logic, persuasiveness).  
  - Detects **emotional tone** (confidence, empathy, stress).  
  - Offers **personalized suggestions** to balance logic with emotional intelligence.  

- 📝 **EQ-Enhanced Quizzes & Journaling**  
  Not just regular quizzes — these are designed to assess both **knowledge** and **emotional awareness**.  
  - Short quizzes that reflect how you respond under pressure.  
  - Journaling prompts to help students reflect on daily stress, communication style, or debate performance.  
  - Results feed back into the analytics dashboard for a **holistic progress report**.  

- 📚 **Learning Resources**  
  Handpicked materials to help students **sharpen debate skills and boost EQ**.  
  - Curated guides on logic, communication, and empathy.  
  - AI-recommended resources based on quiz and debate performance.  
  - Supports **self-paced learning** alongside real-time practice.  

- 📧 **Emotional Alert System**  
  Monitors student input during sessions and sends **alerts if signs of stress or distress are detected**.  
  - Uses NLP sentiment analysis to spot negative emotional trends.  
  - Sends email notifications (via SMTP) to the student for self-awareness.  
  - Acts as a **safety net** for mental well-being in digital learning.  

- 🔒 **Authentication & Security**  
  A simple and secure student login system.  
  - Email-based authentication for signup & login.  
  - Protects student sessions and personal progress data.  
  - Ensures only registered students can access debates, quizzes, and analytics.  


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
