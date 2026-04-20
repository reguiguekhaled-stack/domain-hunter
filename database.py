import sqlite3
from datetime import datetime

class DomainDatabase:
    def __init__(self, db_name='domains.db'):
        """
        ينشئ قاعدة البيانات إذا ما كانت موجودة
        """
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """
        ينشئ جدول الدومينات
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''CREATE TABLE IF NOT EXISTS domains (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_name TEXT UNIQUE,
            tld TEXT,
            length INTEGER,
            score INTEGER,
            search_volume INTEGER,
            backlinks INTEGER,
            estimated_price TEXT,
            date_found TEXT,
            status TEXT
        )''')
        
        conn.commit()
        conn.close()
        print(f"✅ جدول الدومينات جاهز في {self.db_name}")
    
    def insert_domain(self, domain, tld, length, score, search_vol=0, backlinks=0):
        """
        يحط دومين جديد في قاعدة البيانات
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO domains 
            (domain_name, tld, length, score, search_volume, backlinks, date_found, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (domain, tld, length, score, search_vol, backlinks,
             datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'new'))
            
            conn.commit()
            print(f"✅ تم إضافة: {domain}")
        except sqlite3.IntegrityError:
            print(f"⚠️ {domain} موجود بالفعل")
        finally:
            conn.close()
    
    def get_qualified_domains(self, min_score=70):
        """
        يجيب الدومينات اللي score فيها أكبر من الحد الأدنى
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('SELECT * FROM domains WHERE score >= ? ORDER BY score DESC LIMIT 50',
                 (min_score,))
        
        results = c.fetchall()
        conn.close()
        return results
    
    def get_today_domains(self):
        """
        يجيب الدومينات اللي اتحطت اليوم فقط
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''SELECT * FROM domains 
                    WHERE date_found LIKE ? 
                    ORDER BY score DESC''',
                 (datetime.now().strftime('%Y-%m-%d') + '%',))
        
        results = c.fetchall()
        conn.close()
        return results
    
    def export_to_csv(self, filename='daily_report.csv'):
        """
        يصدر الدومينات لملف CSV
        """
        import csv
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # اجيب الدومينات اليوم
        c.execute('''SELECT domain_name, tld, length, score, search_volume, date_found 
                    FROM domains 
                    WHERE date_found LIKE ? 
                    ORDER BY score DESC''',
                 (datetime.now().strftime('%Y-%m-%d') + '%',))
        
        rows = c.fetchall()
        conn.close()
        
        # اكتب في CSV
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Domain', 'TLD', 'Length', 'Score', 'Search Vol', 'Date Found'])
            writer.writerows(rows)
        
        print(f"✅ تم تصدير التقرير إلى {filename}")
    
    def get_all_domains(self):
        """
        يجيب جميع الدومينات
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('SELECT * FROM domains ORDER BY score DESC')
        results = c.fetchall()
        conn.close()
        return results
    
    def count_domains(self):
        """
        يعد عدد الدومينات
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('SELECT COUNT(*) FROM domains')
        count = c.fetchone()[0]
        conn.close()
        return count
    
    def delete_domain(self, domain_name):
        """
        يحذف دومين من قاعدة البيانات
        """
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('DELETE FROM domains WHERE domain_name = ?', (domain_name,))
        conn.commit()
        conn.close()
        print(f"❌ تم حذف: {domain_name}")
        