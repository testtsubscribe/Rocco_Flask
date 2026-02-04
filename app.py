from flask import Flask, render_template, request, session, redirect, url_for, flash, make_response
import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from functools import wraps
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'rocco_secret_key_123'

def get_db_connection():
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row
    return conn

# Simple Auth Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_content(lang):
    conn = get_db_connection()
    content_rows = conn.execute('SELECT id, key, value FROM content WHERE lang = ?', (lang,)).fetchall()
    company_info = conn.execute('SELECT * FROM company_info LIMIT 1').fetchone()
    conn.close()
    
    content_dict = {row['key']: row['value'] for row in content_rows}
    
    # Map language-specific company info
    info_dict = {
        'phone': company_info['phone'],
        'email': company_info['email'],
        'address': company_info[f'address_{lang}'],
        'working_hours': company_info[f'working_hours_{lang}']
    }
    
    return content_dict, info_dict

@app.route('/')
def index():
    # Default language is Azerbaijani
    if 'lang' not in session:
        session['lang'] = 'az'
    
    lang = session['lang']
    content, company = get_content(lang)
    
    return render_template('index.html', content=content, company=company, current_lang=lang)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['az', 'ru', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

# --- ADMIN ROUTES ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM admins WHERE username = ?', (username,)).fetchone()
        conn.close()

        if admin and check_password_hash(admin['password'], password):
            session['admin_logged_in'] = True
            session['admin_user'] = username
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    conn = get_db_connection()
    content_items = conn.execute('SELECT * FROM content ORDER BY key, lang').fetchall()
    company_info = conn.execute('SELECT * FROM company_info LIMIT 1').fetchone()
    conn.close()
    return render_template('admin/dashboard.html', content_items=content_items, company=company_info)

@app.route('/admin/content/add', methods=['GET', 'POST'])
@login_required
def admin_add_content():
    if request.method == 'POST':
        key = request.form.get('key')
        lang = request.form.get('lang')
        value = request.form.get('value')
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO content (key, lang, value) VALUES (?, ?, ?)', (key, lang, value))
            conn.commit()
            flash('Content added successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Error: Key and language pair already exists!', 'error')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/edit.html', action='Add', item=None)

@app.route('/admin/content/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_edit_content(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM content WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        value = request.form.get('value')
        conn.execute('UPDATE content SET value = ? WHERE id = ?', (value, id))
        conn.commit()
        conn.close()
        flash('Content updated!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    conn.close()
    return render_template('admin/edit.html', action='Edit', item=item)

@app.route('/admin/content/delete/<int:id>')
@login_required
def admin_delete_content(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM content WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Content deleted!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/company/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_company():
    conn = get_db_connection()
    company = conn.execute('SELECT * FROM company_info LIMIT 1').fetchone()
    
    if request.method == 'POST':
        fields = ['phone', 'email', 'address_az', 'address_ru', 'address_en', 'working_hours_az', 'working_hours_ru', 'working_hours_en']
        data = [request.form.get(f) for f in fields]
        
        query = 'UPDATE company_info SET ' + ', '.join([f'{f} = ?' for f in fields]) + ' WHERE id = ?'
        conn.execute(query, (*data, company['id']))
        conn.commit()
        conn.close()
        flash('Company info updated!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    conn.close()
    return render_template('admin/edit_company.html', company=company)
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash('Please fill all fields.', 'error')
        return redirect(url_for('index', _anchor='contact'))

    # Store in database
    conn = get_db_connection()
    conn.execute('INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))
    
    # Get company email to notify
    company = conn.execute('SELECT email FROM company_info LIMIT 1').fetchone()
    conn.commit()
    conn.close()

    # Email notification (Mock or real depends on ENV)
    # If SMTP is configured, this would send an email. For now, we simulation.
    try:
        msg = MIMEText(f"New message from {name} ({email}):\n\n{message}")
        msg['Subject'] = 'New Contact Form Submission'
        msg['From'] = 'no-reply@roccocut.com'
        msg['To'] = company['email']
        
        # print(f"SENDING EMAIL TO {company['email']}...") 
        # with smtplib.SMTP('localhost') as s:
        #     s.send_message(msg)
    except Exception as e:
        print(f"Email error: {e}")

    flash('Your message has been sent successfully!', 'success')
    return redirect(url_for('index', _anchor='contact'))

@app.route('/admin/messages')
@login_required
def admin_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM contact_messages ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('admin/messages.html', messages=messages, now=datetime.now())

@app.route('/admin/messages/delete/<int:id>')
@login_required
def admin_delete_message(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contact_messages WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Message deleted!', 'success')
    return redirect(url_for('admin_messages'))

@app.route('/robots.txt')
def robots():
    content = "User-agent: *\nAllow: /\nSitemap: " + request.url_root + "sitemap.xml"
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

@app.route('/sitemap.xml')
def sitemap():
    pages = []
    # Main page with localized versions
    for lang in ['az', 'ru', 'en']:
        pages.append([request.url_root, datetime.now().strftime('%Y-%m-%d')])
    
    xml_content = render_template('sitemap.xml', pages=pages)
    response = make_response(xml_content)
    response.headers["Content-Type"] = "application/xml"
    return response

if __name__ == '__main__':
    app.run(debug=True)
