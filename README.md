# Premium Habit Tracker

A modern, dark-themed habit tracking web application built with Python (Flask) and JavaScript. Track your daily progress with streaks and interactive charts.

## 📸 Screenshots

![Habit Tracker Dashboard](attachment:uploaded_image_1767033960472.png)
_Modern, responsive, and data-driven dashboard._

## ✨ Features

- **Daily Tracking**: Mark habits as complete with a single click.
- **Streaks**: Automatic calculation of current habit streaks.
- **Visual Analytics**: Interactive 7-day progress charts for every habit.
- **Premium Design**: Dark mode aesthetic with glassmorphism effects and responsive layout.
- **Cross-Platform Database Support**:
  - **Local**: Uses SQLite for simple development.
  - **Production**: Supports PostgreSQL (e.g., Supabase) for robust cloud hosting.

## 🛠️ Technology Stack

- **Backend**: Python (Flask)
- **Database**: SQLite (Local) / PostgreSQL (Production)
- **Frontend**: HTML5, Vanilla CSS, JavaScript (Vanilla + Chart.js)
- **Production Server**: Gunicorn

## 🚀 Local Setup

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd habit-tracker
   ```

2. **Create a virtual environment**:

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```powershell
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

## 🌐 Deployment (Render + Supabase)

Detailed deployment instructions can be found in the `brain` directory guide:

1. **GitHub**: Push your code to a GitHub repository.
2. **Supabase**: Create a Postgres database and use the **Connection Pooler (Port 6543)** URI.
3. **Render**: Create a New Web Service, connect your repo, and set the `DATABASE_URL` environment variable.
4. **Initialize DB**: Use the Supabase CLI (`supabase db push`) or the Render shell to run the migration.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
