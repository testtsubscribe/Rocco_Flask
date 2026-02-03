import sqlite3
import os

def setup_database():
    db_path = 'website.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Table for company general info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company_info (
            id INTEGER PRIMARY KEY,
            phone TEXT,
            email TEXT,
            address_az TEXT,
            address_ru TEXT,
            address_en TEXT,
            working_hours_az TEXT,
            working_hours_ru TEXT,
            working_hours_en TEXT
        )
    ''')

    # Table for website text content (multi-language)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY,
            key TEXT NOT NULL,
            lang TEXT NOT NULL,
            value TEXT NOT NULL,
            UNIQUE(key, lang)
        )
    ''')

    # Seed Company Info
    cursor.execute('''
        INSERT INTO company_info (phone, email, address_az, address_ru, address_en, working_hours_az, working_hours_ru, working_hours_en)
        VALUES (
            '+994 50 123 45 67', 
            'info@roccocut.com', 
            'Bakı, Azərbaycan, Nizami küç. 10', 
            'Баку, Азербайджан, ул. Низами 10', 
            'Baku, Azerbaijan, Nizami str. 10',
            'Bazar ertəsi - Şənbə: 09:00 - 18:00',
            'Понедельник - Суббота: 09:00 - 18:00',
            'Monday - Saturday: 09:00 - 18:00'
        )
    ''')

    # Seed Content
    seed_data = [
        # Navbar
        ('nav_home', 'az', 'Ana Səhifə'),
        ('nav_home', 'ru', 'Главная'),
        ('nav_home', 'en', 'Home'),
        ('nav_products', 'az', 'Məhsullar'),
        ('nav_products', 'ru', 'Продукция'),
        ('nav_products', 'en', 'Products'),
        ('nav_about', 'az', 'Haqqımızda'),
        ('nav_about', 'ru', 'О нас'),
        ('nav_about', 'en', 'About Us'),
        ('nav_contact', 'az', 'Əlaqə'),
        ('nav_contact', 'ru', 'Контакт'),
        ('nav_contact', 'en', 'Contact'),

        # Hero Section
        ('hero_title', 'az', 'Peşəkar Kəsmə və Cilalama Diskləri'),
        ('hero_title', 'ru', 'Профессиональные Отрезные и Шлифовальные Диски'),
        ('hero_title', 'en', 'Professional Cutting and Grinding Discs'),
        ('hero_subtitle', 'az', 'Yüksək keyfiyyət, uzunömürlülük və dəqiqlik bizim tərəfdaşlığımızın əsas təməlidir.'),
        ('hero_subtitle', 'ru', 'Высокое качество, долговечность и точность — основа нашего партнерства.'),
        ('hero_subtitle', 'en', 'High quality, durability and precision are the foundation of our partnership.'),
        ('hero_cta', 'az', 'Məhsulları Gör'),
        ('hero_cta', 'ru', 'Смотреть Продукцию'),
        ('hero_cta', 'en', 'View Products'),

        # Products Section
        ('products_title', 'az', 'Məhsullarımız'),
        ('products_title', 'ru', 'Наша Продукция'),
        ('products_title', 'en', 'Our Products'),
        ('disc_1_name', 'az', 'Metal Kəsmə Diski'),
        ('disc_1_name', 'ru', 'Диск для резки металла'),
        ('disc_1_name', 'en', 'Metal Cutting Disc'),
        ('disc_1_desc', 'az', 'Sürətli və təmiz kəsim üçün premium keyfiyyətli metal kəsmə diski.'),
        ('disc_1_desc', 'ru', 'Отрезной диск премиум-качества для быстрой и чистой резки.'),
        ('disc_1_desc', 'en', 'Premium quality metal cutting disc for fast and clean cutting.'),
        
        ('disc_2_name', 'az', 'Daş Cilalama Diski'),
        ('disc_2_name', 'ru', 'Шлифовальный диск по камню'),
        ('disc_2_name', 'en', 'Stone Grinding Disc'),
        ('disc_2_desc', 'az', 'Ağır işlər üçün nəzərdə tutulmuş yüksək dözümlü cilalama diski.'),
        ('disc_2_desc', 'ru', 'Высокопрочный шлифовальный диск, предназначенный для тяжелых работ.'),
        ('disc_2_desc', 'en', 'High durability grinding disc designed for heavy-duty work.'),

        # About Section
        ('about_title', 'az', 'Şirkət Haqqında'),
        ('about_title', 'ru', 'О компании'),
        ('about_title', 'en', 'About Company'),
        ('about_text', 'az', 'Biz illərdir ki, sənaye sektoru üçün ən keyfiyyətli kəsmə və cilalama alətlərinin təchizatı ilə məşğuluruq. Məqsədimiz müştərilərimizə maksimum effektivlik təmin etməkdir.'),
        ('about_text', 'ru', 'Мы уже много лет занимаемся поставкой высококачественного режущего и шлифовального инструмента для промышленного сектора. Наша цель — обеспечить максимальную эффективность для наших клиентов.'),
        ('about_text', 'en', 'We have been supplying the highest quality cutting and grinding tools for the industrial sector for years. Our goal is to provide maximum efficiency to our customers.'),

        # Contact Section
        ('contact_title', 'az', 'Əlaqə Saxlayın'),
        ('contact_title', 'ru', 'Свяжитесь с нами'),
        ('contact_title', 'en', 'Contact Us'),
        ('contact_btn', 'az', 'Mesaj Göndər'),
        ('contact_btn', 'ru', 'Отправить'),
        ('contact_btn', 'en', 'Send Message'),
    ]

    cursor.executemany('INSERT INTO content (key, lang, value) VALUES (?, ?, ?)', seed_data)

    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
