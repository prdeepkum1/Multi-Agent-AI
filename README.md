# Multi Agent System (Streamlit App)

##  Overview

This project is a **Multi-Agent System** built using Python and Streamlit.
It allows multiple AI agents to collaborate and perform tasks efficiently.

---

## Tech Stack

* Python 
* Streamlit
* LangChain
* Groq API

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

---

### 2️ Create virtual environment

```bash
python -m venv venv
```

---

### 3️ Activate environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 4️ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5️ Run the app

```bash
streamlit run app.py
```

---

## Project Structure

```
multi-agent-system/
│── app.py
│── agents.py
│── pipeline.py
│── tools.py
│── requirements.txt
│── README.md
│── .gitignore
│
│── .env                # (not included, contains secrets)
│── venv/               # (ignored)
│── .venv/              # (ignored)
│── __pycache__/        # (auto-generated)

---

## Environment Variables

Create a `.env` file and add your API key:

```
GROQ_API_KEY=your_api_key_here
```

---

## Features

* Multi-agent collaboration
* Streamlit UI
* Fast responses using Groq
* Modular code structure

---

