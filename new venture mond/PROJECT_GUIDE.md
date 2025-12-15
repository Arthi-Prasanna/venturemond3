# Venturemond Project Guide

Welcome to the Venturemond Application! This is a full-stack web application built with FastAPI (Python) and Vanilla HTML/JS.

## Features
- **Database**: SQLite (local) to store users and project data.
- **Authentication**: Safe and secure login using JWT (JSON Web Tokens).
- **Dashboards**: Admin and Client dashboards with real database connections.
- **API**: RESTful API endpoints for data access.

## Files Overview
- **`main.py`**: The heart of the application. Starts the web server, handles API requests, and serves pages.
- **`database.py`**: Manages the connection to the SQLite database (`venturemond.db`).
- **`models.py`**: Defines how data looks in the database (User tables, etc.).
- **`auth.py`**: Handles password security (hashing) and token creation.
- **`templates/`**: Contains the visual web pages (HTML).
- **`static/`**: Contains styles (CSS) and scripts (JS).

## How to Run Locally

1.  **Install Requirements** (One time setup):
    ```powershell
    py -m pip install -r requirements.txt
    ```

2.  **Start the Server**:
    ```powershell
    py main.py
    ```

3.  **Getting Started**:
    - **Sign Up**: Go to [http://localhost:8000/signup](http://localhost:8000/signup) or click "Create Account" on the login page.
    - **Log In**: Use your new credentials.
    - **Admin Access**:
        - To simulate an Admin account, register a user with an email containing the word "admin" (e.g., `admin@test.com`) and log in. The system automatically assigns the 'admin' role if 'admin' is in the email string (for demo simplicity).

## How to Deploy (Vercel)

This project is configured for Vercel.

1.  **Install Vercel CLI**: `npm i -g vercel` (if you have Node.js) OR download from vercel.com.
2.  **Deploy**:
    Run the command:
    ```powershell
    vercel
    ```
    Follow the prompts. It will read `vercel.json` and deploy your API and Frontend instantly.

> **Note on Database**: On Vercel (serverless), the SQLite database (`venturemond.db`) will reset every time the server restarts (which is often). For permanent data storage in production, you would typically connect this to a cloud database (like Vercel Postgres or Supabase), but this setup works perfectly for demos.
