import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Gunakan /tmp/database.db jika berjalan di Vercel/serverless agar database selalu writable
if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or os.environ.get('VERCEL_ENV'):
    DB_PATH = '/tmp/database.db'
else:
    DB_PATH = 'database.db'


def init_db():
    """Menginisialisasi database SQLite jika belum ada dan mengisi data awal."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Buat Tabel Menu Diet
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menus (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            calories INTEGER NOT NULL,
            nutrients TEXT NOT NULL,
            benefits TEXT NOT NULL,
            suggested_time TEXT NOT NULL
        )
    ''')
    
    # 2. Buat Tabel Olahraga
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            suggested_duration TEXT NOT NULL,
            calories_burned INTEGER NOT NULL,
            benefits TEXT NOT NULL
        )
    ''')
    
    # Cek apakah tabel kosong sebelum memasukkan data awal
    cursor.execute('SELECT COUNT(*) FROM menus')
    if cursor.fetchone()[0] == 0:
        # Masukkan Data Menu Diet (25 Menu Makanan + 10 Minuman)
        diet_data = [
            # Sarapan (6 menu)
            ('b1', 'Oatmeal Pisang dan Madu', 'Sarapan', 250, 'Karbohidrat Kompleks, Serat, Kalium', 'Tinggi serat untuk melancarkan pencernaan, membantu kenyang lebih lama.', '07.00 - 08.00'),
            ('b2', 'Roti Gandum dan Telur Rebus', 'Sarapan', 280, 'Protein, Serat, Karbohidrat Kompleks, Kolin', 'Menyuplai asam amino lengkap untuk otot, memberi kenyang stabil.', '07.00 - 08.00'),
            ('b3', 'Smoothie Buah Berry', 'Sarapan', 200, 'Vitamin C, Serat Alami, Antioksidan Polifenol', 'Melindungi sel tubuh dari radikal bebas, menyegarkan tubuh.', '07.00 - 08.00'),
            ('b4', 'Yogurt dan Granola', 'Sarapan', 220, 'Probiotik Alami, Kalsium Tinggi, Serat', 'Menjaga mikrobioma usus dan memperkuat tulang harian.', '07.00 - 08.00'),
            ('b5', 'Salad Buah', 'Sarapan', 150, 'Vitamin A, C, Serat Alami, Air', 'Membantu hidrasi tubuh setelah tidur malam, ringan di perut.', '07.00 - 08.00'),
            ('b6', 'Bubur Kacang Hijau Tanpa Santan', 'Sarapan', 180, 'Protein Nabati, Serat, Zat Besi, Asam Folat', 'Mencegah anemia dan memasok protein sehat bebas lemak jenuh.', '07.00 - 08.00'),
            
            # Makan Siang (6 menu)
            ('l1', 'Nasi Merah dan Dada Ayam Panggang', 'Makan Siang', 350, 'Protein Bebas Lemak, Karbohidrat Kompleks Low-GI', 'Sangat baik untuk pertumbuhan otot, menjaga gula darah stabil.', '12.30 - 13.30'),
            ('l2', 'Salad Ayam Sayur', 'Makan Siang', 280, 'Serat Tinggi, Vitamin A, C, E, Protein', 'Optimal untuk pembakaran lemak harian dan memelihara kelembapan kulit.', '12.30 - 13.30'),
            ('l3', 'Sup Sayur dan Tahu', 'Makan Siang', 180, 'Protein Nabati, Serat, Kalium, Vitamin K', 'Rendah kalori namun kaya mineral mikro, menghangatkan lambung.', '12.30 - 13.30'),
            ('l4', 'Ikan Panggang dan Brokoli', 'Makan Siang', 300, 'Asam Lemak Omega-3, Serat Kasar, Protein', 'Mendukung sirkulasi darah jantung, tinggi zat anti-inflamasi.', '12.30 - 13.30'),
            ('l5', 'Tumis Sayur dan Tempe', 'Makan Siang', 220, 'Protein Nabati Terfermentasi, Isoflavon, Serat', 'Tempe mudah diserap, isoflavon sebagai pelindung sel radikal bebas.', '12.30 - 13.30'),
            ('l6', 'Gado-Gado Rendah Kalori', 'Makan Siang', 260, 'Kalsium, Serat Sayur Kukus, Protein Nabati', 'Kaya sayuran bergizi penyuplai serat dengan porsi saus terbatas.', '12.30 - 13.30'),
            
            # Makan Malam (6 menu)
            ('d1', 'Sup Ayam Sayuran', 'Makan Malam', 220, 'Protein, Air, Serat, Kalium, Vitamin C', 'Sangat ramah bagi lambung, mudah dicerna sebelum istirahat malam.', '18.00 - 19.00'),
            ('d2', 'Salad Tuna', 'Makan Malam', 250, 'Protein Tinggi, Omega-3, Selenium, Vitamin D', 'Menu rendah karbohidrat ideal penunjang pembakaran energi malam.', '18.00 - 19.00'),
            ('d3', 'Kentang Rebus dan Sayuran', 'Makan Malam', 190, 'Karbohidrat Sedang, Serat Pangan, Kalium', 'Mengisi glikogen tubuh yang habis tanpa membuat perut begah.', '18.00 - 19.00'),
            ('d4', 'Capcay Sehat', 'Makan Malam', 200, 'Serat Kasar, Vitamin Kompleks, Protein Ayam', 'Menggunakan sedikit minyak, menyuplai gizi untuk detoks harian.', '18.00 - 19.00'),
            ('d5', 'Omelet Sayur', 'Makan Malam', 180, 'Protein Telur, Serat Bayam/Wortel, Vitamin A', 'Cepat saji, tinggi protein esensial, kenyang nyaman berkualitas.', '18.00 - 19.00'),
            ('d6', 'Salmon Panggang', 'Makan Malam', 320, 'Omega-3 (EPA/DHA), Protein Premium, Vitamin B12', 'Menurunkan peradangan tubuh, mempercepat regenerasi sel malam.', '18.00 - 19.00'),
            
            # Camilan Sehat (7 menu)
            ('s1', 'Apel', 'Camilan Sehat', 80, 'Serat Pektin, Vitamin C, Air', 'Membantu menahan nafsu makan yang berlebihan, sangat praktis.', '10.00 / 15.30'),
            ('s2', 'Pisang', 'Camilan Sehat', 105, 'Kalium, Serat, Karbohidrat Sehat, B6', 'Sumber energi instan sebelum/setelah olahraga, mencegah kram.', '10.00 / 15.30'),
            ('s3', 'Almond Panggang', 'Camilan Sehat', 160, 'Lemak Tak Jenuh Tunggal, Vitamin E, Serat', 'Menjaga kesehatan jantung, rasa kenyang awet berkat serat.', '10.00 / 15.30'),
            ('s4', 'Edamame Rebus', 'Camilan Sehat', 120, 'Protein Nabati, Serat Pangan, Zat Besi', 'Mengganjal lapar sore tanpa merusak defisit kalori harian.', '10.00 / 15.30'),
            ('s5', 'Puding Chia Seed', 'Camilan Sehat', 150, 'Omega-3, Serat Larut Tinggi, Kalsium', 'Mengembang di lambung sehingga memperlambat pencernaan makanan.', '10.00 / 15.30'),
            ('s6', 'Jagung Rebus', 'Camilan Sehat', 130, 'Karbohidrat Kompleks, Serat Kasar, Lutein', 'Menunjang penglihatan sehat, rasa manis alami bebas kolesterol.', '10.00 / 15.30'),
            ('s7', 'Smoothie Alpukat Rendah Gula', 'Camilan Sehat', 170, 'Lemak Baik (Monounsaturated), Vitamin E & K', 'Menyehatkan pembuluh darah, kenyang awet meredam hormon lapar.', '10.00 / 15.30'),

            # Minuman Sehat (10 menu)
            ('dr1', 'Air Putih', 'Minuman Sehat', 0, 'Mineral Esensial', 'Hidrasi utama tubuh, melancarkan metabolisme, membuang sisa racun.', 'Setiap 2 jam'),
            ('dr2', 'Infused Water Lemon', 'Minuman Sehat', 5, 'Vitamin C, Enzim Detoks', 'Mendukung detoksifikasi alami hati, memberi kesegaran alami.', 'Pagi/Siang'),
            ('dr3', 'Teh Hijau', 'Minuman Sehat', 2, 'Antioksidan Katekin, EGCG', 'Mempercepat pembakaran lemak harian dan menenangkan pikiran.', 'Sore Hari'),
            ('dr4', 'Jus Wortel', 'Minuman Sehat', 80, 'Beta-Karoten, Vitamin A, Serat', 'Sangat baik untuk perlindungan retina mata dan peremajaan kulit.', 'Pagi/Sore'),
            ('dr5', 'Jus Tomat', 'Minuman Sehat', 60, 'Likopen, Vitamin C, Mineral', 'Antioksidan tinggi pelindung jantung dari timbunan kolesterol.', 'Siang Hari'),
            ('dr6', 'Smoothie Bayam', 'Minuman Sehat', 120, 'Zat Besi, Klorofil, Serat', 'Penambah energi murni alami, melancarkan ekskresi usus.', 'Pagi Hari'),
            ('dr7', 'Susu Almond', 'Minuman Sehat', 60, 'Kalsium, Vitamin E, Bebas Laktosa', 'Alternatif susu sapi yang rendah kalori dan menyehatkan kulit.', 'Malam Hari'),
            ('dr8', 'Air Kelapa', 'Minuman Sehat', 45, 'Elektrolit Alami, Kalium Tinggi', 'Mengganti cairan tubuh yang hilang dan menstabilkan asam tubuh.', 'Setelah Olahraga'),
            ('dr9', 'Jus Semangka', 'Minuman Sehat', 80, 'Likopen, Asam Amino L-Citrulline', 'Menghidrasi dengan baik dan memulihkan otot pegal pasca latihan.', 'Siang Hari'),
            ('dr10', 'Jus Jeruk Tanpa Gula', 'Minuman Sehat', 110, 'Vitamin C Murni, Asam Sitrat', 'Meningkatkan kekebalan tubuh dari ancaman penyakit luar.', 'Pagi/Siang')
        ]
        cursor.executemany('INSERT INTO menus VALUES (?, ?, ?, ?, ?, ?, ?)', diet_data)
        conn.commit()

    # Cek apakah tabel olahraga kosong sebelum memasukkan data awal
    cursor.execute('SELECT COUNT(*) FROM exercises')
    if cursor.fetchone()[0] == 0:
        # Masukkan Data Olahraga (15 Gerakan)
        exercise_data = [
            ('ex1', 'Jalan Kaki', 'Mudah', '30 - 45 Menit', 180, 'Menyehatkan jantung secara konsisten, aman bagi persendian lutut (low impact).'),
            ('ex2', 'Jogging', 'Sedang', '30 Menit', 350, 'Meningkatkan kapasitas kardiorespirasi (paru-paru & jantung), membakar lemak efektif.'),
            ('ex3', 'Bersepeda', 'Mudah', '45 Menit', 300, 'Memperkuat otot paha, betis, dan bokong, melatih koordinasi keseimbangan.'),
            ('ex4', 'Berenang', 'Sedang', '30 - 45 Menit', 450, 'Latihan seluruh tubuh (full-body workout) yang ramah bagi sendi bermasalah.'),
            ('ex5', 'Yoga', 'Mudah', '45 - 60 Menit', 150, 'Meningkatkan kelenturan tubuh, memperbaiki postur, dan mengurangi stres.'),
            ('ex6', 'Senam Aerobik', 'Sedang', '30 - 45 Menit', 320, 'Meningkatkan stamina, memompa endorfin kegembiraan melalui musik ritmis.'),
            ('ex7', 'Lompat Tali', 'Tinggi', '15 - 20 Menit', 250, 'Kardio intensitas tinggi melatih kelincahan kaki dan kepadatan mineral tulang.'),
            ('ex8', 'Naik Turun Tangga', 'Sedang', '15 - 20 Menit', 200, 'Mengencangkan otot bokong harian dan melatih ketahanan otot kuadrisep.'),
            ('ex9', 'Pilates', 'Sedang', '45 Menit', 220, 'Memperkuat otot inti perut (core stability) dan menyelaraskan postur.'),
            ('ex10', 'Zumba', 'Sedang', '45 - 60 Menit', 400, 'Membakar tumpukan lemak perut melalui gabungan tari latin yang dinamis.'),
            ('ex11', 'Push Up', 'Sedang', '3 Set x 12 Repetisi', 65, 'Membangun kekuatan fungsional dada, trisep, dan stabilitas bahu.'),
            ('ex12', 'Sit Up', 'Sedang', '3 Set x 15 Repetisi', 50, 'Melatih kekencangan otot perut melintang dan stabilitas organ perut.'),
            ('ex13', 'Plank', 'Sedang', '3 Set x 45 Detik', 40, 'Meningkatkan ketahanan isometrik otot perut, menjaga kekuatan punggung.'),
            ('ex14', 'Squat', 'Mudah', '3 Set x 15 Repetisi', 75, 'Melatih mobilitas fungsional otot paha depan, paha belakang, dan bokong.'),
            ('ex15', 'Hiking', 'Tinggi', '1 - 2 Jam', 500, 'Melatih stamina ketahanan paru-paru di alam terbuka serta merefresh pikiran.')
        ]
        cursor.executemany('INSERT INTO exercises VALUES (?, ?, ?, ?, ?, ?)', exercise_data)
        conn.commit()
        
    conn.close()

# Inisialisasi database saat aplikasi dinyalakan
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    category_filter = request.args.get('category', 'Semua')
    search_query = request.args.get('search', '')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM menus WHERE 1=1"
    params = []
    
    if category_filter != 'Semua':
        query += " AND category = ?"
        params.append(category_filter)
        
    if search_query:
        query += " AND (name LIKE ? OR nutrients LIKE ? OR benefits LIKE ?)"
        like_str = f"%{search_query}%"
        params.extend([like_str, like_str, like_str])
        
    cursor.execute(query, params)
    menus = cursor.fetchall()
    conn.close()
    
    # Kelompokkan data minuman terpisah demi kerapihan UI
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menus WHERE category = 'Minuman Sehat'")
    drinks = cursor.fetchall()
    conn.close()
    
    return render_template('menu.html', menus=menus, drinks=drinks, active_category=category_filter, search=search_query)

@app.route('/olahraga')
def olahraga():
    level_filter = request.args.get('level', 'Semua')
    search_query = request.args.get('search', '')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM exercises WHERE 1=1"
    params = []
    
    if level_filter != 'Semua':
        query += " AND difficulty = ?"
        params.append(level_filter)
        
    if search_query:
        query += " AND (name LIKE ? OR benefits LIKE ?)"
        like_str = f"%{search_query}%"
        params.extend([like_str, like_str])
        
    cursor.execute(query, params)
    exercises = cursor.fetchall()
    conn.close()
    
    return render_template('olahraga.html', exercises=exercises, active_level=level_filter, search=search_query)

@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    bmi_val = None
    category = None
    recommendation = None
    weight = ""
    height = ""
    
    if request.method == 'POST':
        try:
            weight_val = float(request.form.get('weight', 0))
            height_val = float(request.form.get('height', 0))
            
            weight = request.form.get('weight', '')
            height = request.form.get('height', '')
            
            if weight_val > 0 and height_val > 0:
                height_m = height_val / 100
                bmi_val = round(weight_val / (height_m * height_m), 1)
                
                if bmi_val < 18.5:
                    category = 'Kurus'
                    recommendation = 'Rekomendasi Anda adalah menaikkan berat badan secara sehat. Fokus pada surplus kalori bersih sekitar 300-500 kkal per hari dengan mengonsumsi makanan padat nutrisi tinggi protein (seperti telur, dada ayam, tempe, alpukat), dan lakukan latihan kekuatan (strength training) minimal 2-3 kali seminggu untuk membangun massa otot secara bertahap.'
                elif bmi_val >= 18.5 and bmi_val < 25.0:
                    category = 'Normal'
                    recommendation = 'Kondisi tubuh Anda berada di titik ideal! Pertahankan pola makan gizi seimbang dengan porsi karbohidrat kompleks, serat sayuran hijau, protein tanpa lemak, serta hidrasi air putih yang cukup. Tetap aktif berolahraga sedang (seperti jogging, berenang, atau bersepeda) 150 menit per minggu untuk menjaga kebugaran jantung.'
                elif bmi_val >= 25.0 and bmi_val < 30.0:
                    category = 'Overweight'
                    recommendation = 'Rekomendasi Anda adalah defisit kalori ringan. Kurangi asupan kalori harian Anda sekitar 200-350 kkal di bawah kebutuhan pemeliharaan harian Anda. Kurangi konsumsi gorengan, cemilan manis, dan gantikan dengan cemilan sehat tinggi serat seperti buah apel, edamame, serta tingkatkan durasi aktivitas kardio ringan secara berkala.'
                else:
                    category = 'Obesitas'
                    recommendation = 'Rekomendasi Anda adalah diet rendah kalori dan olahraga rutin secara terukur. Lakukan pengurangan kalori secara konsisten, prioritaskan makanan utuh (whole foods), hindari gula rafinasi, tepung, dan lemak jenuh. Kombinasikan latihan kardio (30 menit, 4-5 kali seminggu) dengan latihan beban ringan untuk mengaktifkan metabolisme pembakaran lemak tubuh.'
        except ValueError:
            pass
            
    # Pola jadwal harian tetap (static timeline)
    schedule = [
        {"time": "07.00", "activity": "Sarapan Sehat (Breakfast)", "type": "meal", "details": "Pilihlah menu sarapan berprotein tinggi dan berkarbohidrat kompleks. Contoh: Oatmeal Pisang atau Roti Gandum + Telur."},
        {"time": "10.00", "activity": "Snack Pagi (Morning Snack)", "type": "snack", "details": "Mencegah penurunan metabolisme tubuh sebelum makan siang. Contoh: Buah Apel atau Pisang."},
        {"time": "12.30", "activity": "Makan Siang Seimbang (Lunch)", "type": "meal", "details": "Gizi seimbang protein tinggi tanpa lemak, karbohidrat kompleks. Contoh: Nasi Merah + Dada Ayam Panggang."},
        {"time": "15.30", "activity": "Snack Sore (Afternoon Snack)", "type": "snack", "details": "Mengembalikan fokus penenang rasa lapar. Contoh: Segenggam Almond panggang atau Edamame rebus."},
        {"time": "18.30", "activity": "Makan Malam Ringan (Dinner)", "type": "meal", "details": "Menu mudah dicerna rendah karbohidrat sederhana sebelum tidur. Contoh: Sup Ayam Sayur atau Salad Tuna."},
        {"time": "Setiap 2-3 Jam", "activity": "Minum Air Putih (Water Intake)", "type": "water", "details": "Pastikan minum 8-10 gelas sehari (total minimal 2-2.5 Liter)."}
    ]
            
    return render_template('bmi.html', bmi=bmi_val, category=category, recommendation=recommendation, weight=weight, height=height, schedule=schedule)

@app.route('/tentang')
def tentang():
    return render_template('tentang.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
