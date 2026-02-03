from flask import Flask, render_template, request, session, redirect, url_for, flash
import sqlite3
from functools import wraps

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
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
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

if __name__ == '__main__':
    app.run(debug=True)
