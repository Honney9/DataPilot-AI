# 🚀 DataPilot AI

### AI-Powered Data Analysis & Reporting Platform

DataPilot AI is an end-to-end intelligent data analysis system that allows users to upload datasets, explore insights, generate visualizations, interact via chat, and produce AI-generated reports — all in one place.

---

## 📌 Features

* 📂 **Upload Dataset** (CSV support)
* 🧹 **Automatic Data Cleaning**
* 📊 **Exploratory Data Analysis (EDA)**
* 📈 **Dynamic Visualizations**
* 🧠 **AI-Generated Insights**
* 💬 **Chat with Your Data**
* 📄 **AI Report Generation (PDF Download)**

---

## 🧠 Tech Stack

### 🔹 Backend

* FastAPI
* Pandas / NumPy
* Scikit-learn
* ReportLab (PDF generation)
* LLM Integration:

  * Groq (LLaMA models)
  * Google Gemini
  * OpenRouter (fallback)

### 🔹 Frontend

* React (Vite)
* TypeScript
* TailwindCSS
* Lucide Icons

---

## 🏗️ Architecture

```
User → React Frontend → FastAPI Backend → AI Agents → LLM APIs
                                      ↓
                                Session Memory
```

### 🤖 AI Agent Pipeline

* Ingestion Agent
* Cleaning Agent
* Analysis Agent
* Visualization Agent
* Insight Agent
* Report Agent
* Query Agent (chat)

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Honney9/DataPilot-AI
cd datapilot-ai
```

---

### 2️⃣ Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

#### 🔐 Create `.env`

```env
GROQ_API_KEY=your_key
GEMINI_API_KEY=your_key
OPENROUTER_API_KEY=your_key
```

#### ▶️ Run Backend

```bash
uvicorn app.main:app --reload
```

---

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
```

#### 🔐 Create `.env`

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_USE_MOCK=false
```

#### ▶️ Run Frontend

```bash
npm run dev
```

---

## 📄 API Endpoints

| Method | Endpoint           | Description     |
| ------ | ------------------ | --------------- |
| POST   | `/upload`          | Upload dataset  |
| GET    | `/data/raw`        | Raw data        |
| GET    | `/data/preview`    | Cleaned data    |
| GET    | `/visualizations`  | Charts          |
| GET    | `/insights`        | AI insights     |
| POST   | `/report`          | Generate report |
| GET    | `/report/download` | Download PDF    |
| POST   | `/chat`            | Chat with data  |

---

## 📊 Example Workflow

1. Upload dataset 📂
2. View cleaned preview 🧹
3. Explore charts 📈
4. Get insights 🧠
5. Ask questions 💬
6. Generate report 📄

---

## 📸 Screenshots (Optional)

*Add screenshots of your UI here*

---

## 🚧 Known Issues

* LLM responses depend on API availability
* Large datasets may take longer to process

---

## 🎯 Future Improvements

* Real-time streaming responses
* More chart customization
* Multi-file support
* Dashboard exports

---

## 👨‍💻 Author

**Your Name**
Final Year Computer Science Project

---

## 📜 License

This project is for academic purposes.

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
