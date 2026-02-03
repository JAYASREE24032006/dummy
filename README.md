# Agentic AI-Driven SSO System

An advanced Single Sign-On (SSO) authentication system enhanced with Agentic AI for real-time security monitoring, risk assessment, and session management. This project demonstrates a premium, high-fidelity enterprise interface with state-of-the-art security features.

## 🚀 Key Features

### 🔐 **Advanced Security Core**
- **Ephemeral Sessions (Privacy Mode)**: Built strictly on `sessionStorage` to ensure zero persistence. closing a tab instantly terminates the session.
- **Aggressive Anti-Autocomplete**: Implements blind inputs, randomized attribute names (`agent_user_id_x9`), and read-only buffers to prevent browser password managers from compromising security logic.
- **Token-Based Authentication**: Secure JWT implementation for stateless yet verifiable access.

### 🤖 **Agentic Architecture**
- **Risk Agent**: Continuously evaluates user behavior and context for anomalies.
- **Monitoring Agent**: Tracks active sessions and device fingerprints in real-time.
- **Executioner Agent**: Capable of terminating high-risk sessions instantly across all active clients.

### 🎨 **Premium User Experience (UI/UX)**
- **Glassmorphism Design**: Modern, translucent UI components with frosted glass effects.
- **Interactive Particle Background**: A custom Canvas-based constellation animation on the login screen that reacts to mouse movement.
- **Responsive Dashboard**: Adaptive layouts for HR, CRM, ERP, and Admin consoles.

### ⚡ **Real-Time Communication**
- **Socket.IO Integration**: Full duplex communication for instant global logout signals and security alerts.
- **Multi-Tab Synchronization**: While ensuring strict privacy, the broader architecture supports synchronized security states.

---

## 🛠️ Technology Stack

### **Frontend**
- **Framework**: React 18 (Vite)
- **Styling**: Vanilla CSS (Custom Variables, CSS3 Animations)
- **State Management**: React Hooks + SessionStorage
- **Communication**: Socket.IO Client

### **Backend**
- **Framework**: FastAPI (Python 3.10+)
- **Asynchronous**: Fully async/await architecture
- **Database/Cache**: Redis (for high-speed session storage and pub/sub)
- **Communication**: Python-SocketIO

### **DevOps**
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Multi-service architecture (Frontend, Backend, Redis)

---

## 🏃‍♂️ Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Redis (Local or Docker)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Docker (Optional)
Run the entire stack with a single command:
```bash
docker-compose up -d --build
```

---

## 🧪 Usage Guide

1.  **Access the Application**: Open [http://localhost:5174](http://localhost:5174).
2.  **Login**: Use any test credential (e.g., `admin` / `password`).
    *   *Note: The system simulates successful authentication for prototype testing.*
3.  **Explore Modules**: Navigate through HR, CRM, and ERP dashboards.
4.  **Test Security**:
    *   **Global Logout**: Click the "Global Logout" button to simulate an admin terminating the session from the server side.
    *   **Privacy Test**: Close the tab and reopen it to verify that you are forced to log in again.

---

## 📂 Project Structure

```
agentic-sso/
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── agents/         # AI Logic (Risk, Monitoring, Execution)
│   │   ├── auth/           # OAuth2 & Socket Auth
│   │   └── core/           # Database & Config
│   └── Dockerfile
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # UI Components (LoginBackground, etc.)
│   │   ├── pages/          # Application Pages (Login, Dashboard)
│   │   └── auth/           # Interceptors & Socket Logic
│   └── Dockerfile
└── docker-compose.yml      # Orchestration Config
```

---

## 🛡️ License
Proprietary - Research Prototype for Agentic Security Systems.
