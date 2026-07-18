# 🏆 World Cup Business Intelligence Copilot

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red)
![License](https://img.shields.io/badge/License-MIT-green)

<p align="center">

AI-powered Business Intelligence Dashboard for evaluating FIFA World Cup teams' commercial value, sponsorship opportunities, and historical tournament performance.

Built with **Python**, **Streamlit**, **Plotly**, **Pandas**, and optional **OpenAI API** integration.

</p>

---

## 🚀 Live Demo

🌐 **Online Demo**

https://worldcup-business-copilot-xwetqs4solcofyvkds9fkn.streamlit.app

---

## 📌 Highlights

- 📊 Interactive Business Intelligence Dashboard
- 🌍 Historical World Cup Analytics
- 🤖 AI-inspired Business Copilot
- 📝 Executive Business Report Generator
- 📈 Commercial Value Evaluation Model
- 🔄 Offline + AI Architecture
- ☁️ Streamlit Cloud Deployment
- 🐍 Python + Plotly + Pandas

---

# 📚 Table of Contents

- Project Overview
- Features
- Dashboard Preview
- Technology Stack
- Project Architecture
- Project Structure
- Installation
- Configuration
- Deployment
- Roadmap
- Learning Outcomes
- Author
- License

---

# 📖 Project Overview

The **World Cup Business Intelligence Copilot** is an interactive business intelligence dashboard designed to analyze FIFA World Cup teams from a commercial perspective.

Unlike traditional football dashboards that focus solely on match statistics, this application evaluates each team's business potential using commercial indicators such as:

- Market Size
- Sponsor Exposure
- Social Media Heat
- Star Power
- Performance Score
- Advancement Probability
- Business Value Score

The project demonstrates how data analytics and AI can support sponsorship strategy, business decision-making, and commercial opportunity analysis.

---

# ✨ Features

## 📊 Business Intelligence Dashboard

- Interactive KPI dashboard
- Regional filtering
- Business Value filtering
- Team profile analysis
- Radar visualization
- Commercial metrics

---

## 🌍 Historical Analytics

- Historical World Cup champions
- Tournament timeline
- Champion history
- Historical performance visualization

---

## 🤖 Business Copilot

The built-in Business Copilot supports questions such as:

- Should Adidas sponsor France?
- What are Argentina's commercial risks?
- How valuable is Brazil?
- How can England improve fan engagement?
- What are Japan's business advantages?

Business Copilot provides:

- Sponsorship recommendations
- Commercial value analysis
- Business risk assessment
- Fan engagement suggestions
- Investment recommendations

---

## 📝 Business Report Generator

Generate an executive-style report including:

- Executive Summary
- Commercial Opportunity
- Sponsorship Recommendation
- Risk Assessment
- Strategic Recommendation

Reports can be downloaded directly from the dashboard.

---

## 🔄 Offline + AI Mode

The application supports two operating modes.

### Offline Mode

No API key required.

Business recommendations are generated using predefined commercial rules.

### AI Mode

When an OpenAI API key is available, the application can generate AI-powered business insights.

If AI is unavailable, the application automatically switches back to Offline Mode.

---

# 📸 Dashboard Preview

> Screenshots will be updated after Version 1.0 release.

## Dashboard

![Dashboard](<img width="1425" height="664" alt="image" src="https://github.com/user-attachments/assets/e3230e1c-2f47-494f-8d35-79c4dcb86f4e" />
)
---

## Business Copilot

![Business Copilot](<img width="1098" height="489" alt="image" src="https://github.com/user-attachments/assets/f119be3a-1425-48d7-8bd2-d59c0408bca3" />
)

---

## Business Report

![Business Report](<img width="1438" height="795" alt="image" src="https://github.com/user-attachments/assets/af4be795-9347-4839-9c96-e516663501c5" /><img width="1439" height="794" alt="image" src="https://github.com/user-attachments/assets/522721a8-8fed-45f6-b237-b6a9d5445a49" /><img width="1437" height="789" alt="image" src="https://github.com/user-attachments/assets/b57143b5-d30b-4470-8fbe-5fa10a33231f" />)

---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Dashboard | Streamlit |
| Data Analysis | Pandas |
| Visualization | Plotly |
| AI | OpenAI API (Optional) |
| Version Control | Git & GitHub |
| Deployment | Streamlit Community Cloud |

---

# 🏗 Project Architecture

```
                    User
                      │
                      ▼
              Streamlit Dashboard
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
 Business Analytics           Business Copilot
        │                           │
        ▼                           ▼
 Plotly Charts             Offline Rules / OpenAI
        │                           │
        └─────────────┬─────────────┘
                      ▼
             Business Report Output
```

---

# 📂 Project Structure

```
worldcup-business-copilot/
│
├── app.py
├── README.md
├── requirements.txt
├── .env.example
│
├── data/
│   ├── teams.csv
│   └── historical_world_cup.csv
│
├── src/
│   └── worldcup_business_copilot/
│       ├── app.py
│       ├── charts.py
│       ├── business_value.py
│       ├── config.py
│       ├── data.py
│       └── llm.py
│
└── images/
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/TonyCurlymoe/worldcup-business-copilot.git
```

Move into the project folder:

```bash
cd worldcup-business-copilot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create your environment file:

```bash
copy .env.example .env
```

Run the application:

```bash
streamlit run app.py
```

---

# 🔑 Configuration

Optional environment variables:

```text
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

TEAM_DATA_PATH=data/teams.csv
HISTORICAL_DATA_PATH=data/historical_world_cup.csv
```

Without an API key, the dashboard automatically runs in Offline Mode.

---

# ☁️ Deployment

This application is deployed using:

- Streamlit Community Cloud
- GitHub Actions (future)
- GitHub Repository

Every push to the **main** branch automatically updates the live application.

---

# 🛣 Roadmap

## Version 1.0 ✅

- Interactive Dashboard
- Business Value Model
- Historical Analytics
- Business Copilot
- Offline Mode
- Business Report
- Cloud Deployment

---

## Version 2.0

- Team Comparison Dashboard
- Dual Radar Charts
- AI Comparison Report
- Enhanced KPI Dashboard

---

## Version 3.0

- Live Match Data
- Real FIFA API
- Player-level Analytics
- Sponsorship ROI Prediction
- GPT-5 Business Copilot

---

# 🎓 Learning Outcomes

This project demonstrates practical experience in:

- Business Intelligence
- Data Analytics
- Dashboard Development
- Data Visualization
- AI Integration
- Cloud Deployment
- Python Programming
- Git Version Control

---

# 👨‍💻 Author

**Wei Che (Tony)**

Business Analytics

San Francisco State University

GitHub

https://github.com/TonyCurlymoe

---

# 📄 License

This project is licensed under the MIT License.
