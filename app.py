from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'rocco_secret_key_123'

def get_db_connection():
    conn = sqlite3.connect('website.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_content(lang):
    conn = get_db_connection()
    content_rows = conn.execute('SELECT key, value FROM content WHERE lang = ?', (lang,)).fetchall()
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

if __name__ == '__main__':
    app.run(debug=True)
