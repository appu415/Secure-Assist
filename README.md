# 🛡️ SecureAssist: AI-Powered Cybersecurity Advisor
**A specialized Retrieval-Augmented Generation (RAG) framework for enterprise security.**

SecureAssist is a cutting-edge chatbot designed to provide expert cybersecurity advice by prioritizing internal company security policies over general AI knowledge. Built with a "Hacker-Terminal" aesthetic, it features high availability through automated model fallback and a secure administrative audit layer.

---

## 🚀 Key Features

- **Retrieval-Augmented Generation (RAG):** Connects to a private Gemini File Search Store to provide answers based on official `security_docs.txt`.
- **Intelligent Fallback Loop:** Automatically rotates through `Gemini 3.0 Flash`, `2.5 Flash`, and `2.0 Flash` to bypass API quota limits.
- **Cyber-Terminal UI:** Features a split-screen layout with a real-time **System Console** for monitoring network activity and model status.
- **Admin Audit Dashboard:** A password-protected management area to review chat history, monitor performance, and delete logs for privacy compliance.
- **Source Badging:** Automatically identifies responses as `VERIFIED POLICY` (internal) or `GENERAL INFO` (global AI training data).

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python / Flask 3.0+ |
| **AI Engine** | Google Gemini 3.0 Flash (RAG enabled) |
| **Database** | SQLite3 |
| **Frontend** | Vanilla JS, CSS3 (Modern Flexbox), HTML5 |
| **Security** | Flask Sessions & Environment Variables |

---

## 📂 Project Structure

```text
SecureAssist/
├── app.py                   # Main Backend Logic & Flask Routes
├── upload_rag.py            # Utility to sync local docs with Gemini Cloud
├── security_docs.txt        # Your source knowledge base
├── .env                     # API Keys (Excluded from Git)
├── requirements.txt         # Dependencies
├── static/
│   ├── css/style.css        # Hacker-mode Styling
│   └── js/chat.js           # Frontend Logic & Console Logs
└── templates/
    ├── index.html           # Main Interface
    ├── admin_login.html     # Admin Gate
    └── admin_dashboard.html # Data Management Panel
