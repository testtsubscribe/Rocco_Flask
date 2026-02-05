# ROCCO Corporate Website

A modern, high-quality corporate website for a company specializing in professional cutting and grinding discs. Built with Flask and SQLite, featuring full multi-language support and a secure administrative control panel.

## Features

- **Multi-language Support**: Fully localized in Azerbaijani (default), Russian, and English.
- **Dynamic Content Management**: Control all website text, company info, and SEO metadata via a modern Admin Panel.
- **Secure Authentication**: Hashed password protection for administrative accounts.
- **SEO Optimized**: Dynamic meta tags, OG tags, structured data (JSON-LD), `sitemap.xml`, and `robots.txt`.
- **Modern Design**: Responsive, dark-themed industrial aesthetic with premium visuals.
- **Leads Management**: Functional contact form with database storage and admin message viewer.

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3 (Vanilla), Jinja2
- **Security**: Werkzeug (Password Hashing)

---

## Getting Started

Follow these steps to set up and run the project locally from scratch.

### 1. Prerequisites
Ensure you have Python 3 installed on your system.
```bash
python3 --version
```

### 2. Install Dependencies
Install Flask and other required libraries:
```bash
pip install flask werkzeug
```

### 3. Initialize the Database
Run the setup script to create the tables and seed the initial content (Azerbaijani, Russian, English):
```bash
python3 setup_db.py
```

### 4. Create an Admin Account
Use the security utility script to create your administrative account:
```bash
# Usage: python3 create_admin.py <username> <password>
for example: python3 create_admin.py admin admin123
```

### 5. Run the Application
Start the Flask development server:
```bash
python3 app.py
```

### 6. Access the Website
- **Live Site**: [http://127.0.0.1:5000](http://127.0.0.1:5000)
- **Admin Panel**: [http://127.0.0.1:5000/admin](http://127.0.0.1:5000/admin)
  - *Login with your created credentials.*

---

## Project Structure

- `app.py`: Main application logic and routing.
- `setup_db.py`: Database schema definition and professional content seeding.
- `create_admin.py`: Secure admin user management utility.
- `website.db`: SQLite database (generated after setup).
- `templates/`: Jinja2 HTML templates.
  - `index.html`: Main landing page.
  - `admin/`: Administrative panel templates.
- `static/`: Static assets (CSS, JS, Images, Favicon).

## Management Guide

### Updating Content
1. Log in to the Admin Panel.
2. Navigate to the **Content** tab.
3. Click **Edit** on any entry to modify its value for a specific language.
4. Changes are reflected instantly on the live site.

### Viewing Inquiries
1. Log in to the Admin Panel.
2. Navigate to the **Messages** tab.
3. You can view all user submissions from the contact form and delete them after processing.

---

&copy; 2026 ROCCO Corporate. All rights reserved.
