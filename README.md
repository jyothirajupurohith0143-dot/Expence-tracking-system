# 💰 Expense Tracking & Analytics System

A beginner-friendly personal finance application built with **Python, Streamlit, SQLite, Pandas, Plotly, and ReportLab**.

The project records income and expenses, tracks budgets, calculates savings, visualizes financial patterns, and generates monthly PDF reports.

## ✨ Features

- User registration and login
- Secure password hashing with SHA-256
- Add and manage income
- Add and manage expenses
- Expense categories
- Payment-method tracking
- Monthly budget tracking
- Budget utilization and over-budget alerts
- Income, expenses, savings and savings-rate KPIs
- Monthly cash-flow analysis
- Category-wise expense analysis
- Savings trend visualization
- Interactive Plotly dashboard
- Monthly PDF financial report
- CSV export
- SQLite database
- Basic unit tests

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web application UI |
| SQLite | Database |
| Pandas | Data analysis |
| Plotly | Interactive visualization |
| ReportLab | PDF report generation |
| unittest | Testing |

## 📁 Project Structure

```text
expense-tracking-system/
│
├── data/
│   └── finance.db              # Created automatically
├── reports/                    # Generated PDF reports
├── charts/                     # Optional chart exports
├── src/
│   ├── auth.py
│   ├── analytics.py
│   ├── budget.py
│   ├── dashboard.py
│   ├── database.py
│   ├── reports.py
│   └── transactions.py
├── tests/
│   └── test_expense_manager.py
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/expense-tracking-system.git
cd expense-tracking-system
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🔐 Login

Create an account from the **Create Account** tab and then log in.

Passwords are hashed before being stored in SQLite.

> For a production application, use a modern password-hashing algorithm such as Argon2 or bcrypt and add additional security controls.

## 📊 Dashboard

The dashboard provides:

- Total income
- Total expenses
- Savings
- Savings rate
- Monthly income vs expenses
- Category-wise spending
- Savings trend
- Recent transactions

## 🎯 Budget Tracking

Create a monthly budget for categories such as:

- Food
- Transport
- Shopping
- Bills
- Entertainment
- Health
- Education
- Rent
- Travel
- Other

The system compares actual spending against the configured budget.

## 📄 Monthly PDF Report

Select a month and generate a PDF containing:

- Total income
- Total expenses
- Savings
- Savings rate
- Category-wise expenses

## 🧪 Run Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## 📌 Data Analyst Concepts Demonstrated

This project demonstrates practical use of:

- Data collection
- Data cleaning/preparation
- Aggregation
- GroupBy analysis
- Pivot tables
- KPI calculation
- Time-series analysis
- Category analysis
- Data visualization
- Reporting
- SQL/SQLite database operations
- Basic testing

## 📈 Future Enhancements

Possible next versions can add:

- Edit transaction functionality
- Recurring transactions
- Email reports
- Advanced filters
- User profile management
- Excel report generation
- Power BI integration
- Deployment with Streamlit Community Cloud
- More advanced authentication

## 👩‍💻 Author

**Jyothi Kawar**

BCA — Kuvempu University

Data Analyst / Python / SQL / Data Visualization

---

⭐ If you find this project useful, consider giving the repository a star.
