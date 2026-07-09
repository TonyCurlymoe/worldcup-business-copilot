# World Cup Business Intelligence Copilot

A Streamlit MVP that analyzes World Cup teams by performance and business value, then generates AI-powered business reports.

## Features
- Team commercial value ranking
- Business value scoring model
- Interactive dashboard
- AI-generated team business report
- Local sample data for quick demo

## Quick Start on Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

Add your OpenAI API key in `.env` if you want AI report generation.
