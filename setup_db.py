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

    # Table for admins general info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )           
    ''')

    # Table for contact_messages definition info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT (datetime('now', '+4 hours'))
        )           
    ''')


    # Seed Company Info
    cursor.execute('''
        INSERT INTO company_info (phone, email, address_az, address_ru, address_en, working_hours_az, working_hours_ru, working_hours_en)
        VALUES (
            '+994 55 212 46 12', 
            'info@rocco.az', 
            'Bakı, Azərbaycan, Naxçıvanski küç. 81', 
            'Баку, Азербайджан, ул. Нахчыванская 81', 
            'Baku, Azerbaijan, Nakhchivanski str. 81',
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
        ('about_text', 'az', 'Sektorda 15 ildən artıq təcrübəyə malik peşəkar daş kəsmə və cilalama xidmətləri. Biz bütün təbii daş növlərinin dəqiq kəsimi üzrə ixtisaslaşmışıq.'),
        ('about_text', 'ru', 'Профессиональные услуги по резке и полировке камня с более чем 15-летним опытом работы в отрасли. Мы специализируемся на точной резке всех видов натурального камня.'),
        ('about_text', 'en', 'Professional stone cutting and polishing services with over 15 years of industry experience. We specialize in precision cutting of all types of natural stone.'),

        ('mission_title', 'az', 'Missiyamız'),
        ('mission_title', 'ru', 'Наша миссия'),
        ('mission_title', 'en', 'Our Mission'),
        ('mission_text', 'az', 'Rocco Group-da bizim missiyamız müştərilərimizə ən yüksək keyfiyyətli daş kəsmə və cilalama xidmətləri təqdim etməkdir. Biz hər layihənin unikal olduğunu başa düşürük və hər bir detalda mükəmməlliyə nail olmağa çalışırıq. Təcrübəli komandamız və qabaqcıl avadanlığımızla biz müştərilərimizin təsəvvürlərini həqiqətə çeviririk.'),
        ('mission_text', 'ru', 'Наша миссия в Rocco Group — предоставлять нашим клиентам услуги по резке и полировке камня самого высокого качества. Мы понимаем, что каждый проект уникален, и стремимся к совершенству в каждой детали. Благодаря нашей опытной команде и современному оборудованию мы воплощаем идеи наших клиентов в реальность.'),
        ('mission_text', 'en', 'Our mission at Rocco Group is to provide our customers with the highest quality stone cutting and polishing services. We understand that every project is unique and strive for excellence in every detail. With our experienced team and advanced equipment, we turn our customers\' visions into reality.'),

        ('vision_title', 'az', 'Vizyonumuz'),
        ('vision_title', 'ru', 'Наше видение'),
        ('vision_title', 'en', 'Our Vision'),
        ('vision_text', 'az', 'Bizim vizyonumuz daş emal sənayesində lider olmaq, innovasiya, keyfiyyət və müştəri məmnuniyyətində standartlar yaratmaqdır. Biz davamlı təkmilləşmə və texnoloji irəliləyişlərə sadiq qalaraq, hər bir layihədə gözəl və davamlı nəticələr verməyə çalışırıq.'),
        ('vision_text', 'ru', 'Наше видение — быть лидером в индустрии обработки камня, устанавливая стандарты инноваций, качества и удовлетворенности клиентов. Мы стремимся к постоянному совершенствованию и технологическому прогрессу, стремясь обеспечить красивые и долговечные результаты в каждом проекте.'),
        ('vision_text', 'en', 'Our vision is to be a leader in the stone processing industry, setting standards in innovation, quality, and customer satisfaction. We are committed to continuous improvement and technological advancement, striving to provide beautiful and lasting results in every project.'),

        ('why_choose_title', 'az', 'Rocco niyə seçilir ?'),
        ('why_choose_title', 'ru', 'Почему выбирают Rocco?'),
        ('why_choose_title', 'en', 'Why Choose Rocco?'),

        ('feature_1_title', 'az', 'Keyfiyyətli İşçilik'),
        ('feature_1_title', 'ru', 'Качественное мастерство'),
        ('feature_1_title', 'en', 'Quality Craftsmanship'),
        ('feature_1_text', 'az', 'Hər detalda mükəmməlliyə nail olmaq üçün təcrübəli ustaların bacarıqları'),
        ('feature_1_text', 'ru', 'Навыки опытных мастеров для достижения совершенства в каждой детали.'),
        ('feature_1_text', 'en', 'Skills of experienced craftsmen to achieve excellence in every detail.'),

        ('feature_2_title', 'az', 'Vaxtında Çatdırılma'),
        ('feature_2_title', 'ru', 'Своевременная доставка'),
        ('feature_2_title', 'en', 'Timely Delivery'),
        ('feature_2_text', 'az', 'Keyfiyyətdən güzəştə getmədən layihələrin vaxtında tamamlanması'),
        ('feature_2_text', 'ru', 'Завершение проектов в срок без ущерба для качества.'),
        ('feature_2_text', 'en', 'Completion of projects on time without compromising on quality.'),

        ('feature_3_title', 'az', 'Ekspert Komanda'),
        ('feature_3_title', 'ru', 'Команда экспертов'),
        ('feature_3_title', 'en', 'Expert Team'),
        ('feature_3_text', 'az', '15+ il təcrübəsi olan peşəkar daş emalı mütəxəssisləri'),
        ('feature_3_text', 'ru', 'Профессиональные специалисты по обработке камня с опытом работы более 15 лет.'),
        ('feature_3_text', 'en', 'Professional stone processing specialists with 15+ years of experience.'),

        ('feature_4_title', 'az', 'Müasir Avadanlıq'),
        ('feature_4_title', 'ru', 'Современное оборудование'),
        ('feature_4_title', 'en', 'Modern Equipment'),
        ('feature_4_text', 'az', 'Dəqiq və səmərəli emal üçün ən son texnologiya'),
        ('feature_4_text', 'ru', 'Последние технологии для точной и эффективной обработки.'),
        ('feature_4_text', 'en', 'Latest technology for precise and efficient processing.'),

        ('feature_5_title', 'az', 'Keyfiyyət Zəmanəti'),
        ('feature_5_title', 'ru', 'Гарантия качества'),
        ('feature_5_title', 'en', 'Quality Guarantee'),
        ('feature_5_text', 'az', 'Bütün xidmətlərimiz üzrə tam məmnuniyyət zəmanəti'),
        ('feature_5_text', 'ru', 'Полная гарантия удовлетворения на все наши услуги.'),
        ('feature_5_text', 'en', 'Full satisfaction guarantee on all our services.'),

        ('feature_6_title', 'az', 'Müştəri Mərkəzli'),
        ('feature_6_title', 'ru', 'Клиентоориентированность'),
        ('feature_6_title', 'en', 'Customer Centric'),
        ('feature_6_text', 'az', 'Sizin ehtiyaclarınız və məmnuniyyətiniz bizim əsas prioritetimizdir'),
        ('feature_6_text', 'ru', 'Ваши потребности и удовлетворение — наш главный приоритет.'),
        ('feature_6_text', 'en', 'Your needs and satisfaction are our main priority.'),

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
