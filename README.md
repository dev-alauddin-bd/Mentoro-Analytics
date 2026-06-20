# Mentoro Analytics Dashboard

## Overview
A **Streamlit**‑based analytics dashboard for the Mentoro platform. It visualizes user, revenue, course, and overview data pulled from a PostgreSQL database via **Prisma**. The project demonstrates secure database connections on Windows, proper handling of environment variables, and a clean Git history after removal of a leaked `.env` file.

## Features
- Interactive charts using **Plotly** integrated with Streamlit.
- Modular page architecture (`pages/overview.py`, `pages/users.py`, etc.).
- Secure PostgreSQL connection with SSL certificate handling via `certifi`.
- Automated logging for debugging database issues.
- Fully documented `.gitignore` to protect sensitive files.

## Getting Started

### Prerequisites
- **Python 3.12** (or later)
- **Git**
- **PostgreSQL** instance (you can use the Prisma hosted database).

### Installation
```bash
# Clone the repository (already done)
# cd into the project directory
cd d:/projects/mentoro/analytics

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the project root (it is ignored by Git) with the following key:
```dotenv
DATABASE_URL=postgres://<user>:<password>@<host>:5432/<db>?sslmode=verify-full
```
> **Important**: After the earlier leak, rotate the Prisma secret in the Prisma console and replace the old `DATABASE_URL` with the new one.

### Running the Dashboard
```bash
streamlit run dashboard/app.py
```
Visit `http://localhost:8501` in your browser.

## Security Measures
- The `.env` file is listed in `.gitignore` to prevent accidental commits.
- After the initial accidental push, the repository history was rewritten using `git filter-branch` and force‑pushed to remove the leaked secret.
- Database connections on Windows use `certifi.where()` to supply the SSL root certificate.

## Git History Cleanup (Reference)
The first commit containing the `.env` file was removed with:
```bash
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch .env" --prune-empty --tag-name-filter cat -- --all

git push --force origin main
```
> **Warning**: This rewrites history. All collaborators must reset their local clones.

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Ensure your changes do not expose secrets.
4. Open a pull request.

## License
This project is licensed under the MIT License.
