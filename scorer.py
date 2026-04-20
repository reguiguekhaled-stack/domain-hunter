import re
from datetime import datetime

class DomainScorer:
    def __init__(self):
        """
        نظام تقييم الدومينات
        """
        # كلمات حمراء (تقلل الدرجة)
        self.red_flags = [
            'ultra', 'super', 'hyper', 'pro', 'max',
            'evans', 'johnson', 'miller', 'smith',  'surnames',
            'wad', 'xxx', 'porn', 'sex', 'vulgar',
            'test', 'demo', 'sample', 'temp',
        ]
        
        # كلمات خضراء (تزيد الدرجة)
        self.good_words = [
            'relay', 'parcel', 'copper', 'rental', 'flow',
            'vault', 'hub', 'nest', 'spark', 'drift',
            'swift', 'swift', 'prime', 'apex', 'pulse',
            'sync', 'track', 'route', 'stream', 'bridge',
            'logic', 'forge', 'craft', 'scale', 'shift', 
            'power','vision','pay','moving','service','home'
            'open','smart','cyber','mega','labs','lab',
        ]
        
        # كلمات تجارية قوية (bonus)
        self.commerce_words = [
            'pay', 'shop', 'trade', 'deal', 'buy', 'sell',
            'market', 'store', 'sale', 'cart', 'checkout',
            'order', 'delivery', 'shipping', 'logistics',
            'payment', 'invoice', 'purchase', 'merchant'
        ]
        
        # صناعات ساخنة (trending niches)
        self.hot_niches = {
            'ai': 10,        # كلمات AI
            'crypto': 8,     # Blockchain/Crypto
            'fintech': 10,   # Financial Tech
            'logistics': 10, # Logistics/Delivery
            'real estate': 7, # Real Estate
            'ecommerce': 9,  # E-Commerce
            'saas': 9,       # Software as Service
            'health': 7,     # HealthTech
            'education': 6,  # EdTech
            'data': 8,       # Data/Analytics
        }
    
    def score_domain(self, domain):
        """
        تحسب درجة الدومين (0-100)
        """
        score = 0
        domain_name = domain.split('.')[0].lower()
        tld = domain.split('.')[-1].lower()
        
        # القاعدة 1: طول الدومين (أفضل: 8-12 حرف)
        score += self._score_length(len(domain_name))
        
        # القاعدة 2: بدون أرقام وهايفن
        score += self._score_clean_name(domain_name)
        
        # القاعدة 3: فحص الكلمات الحمراء
        score += self._score_red_flags(domain_name)
        
        # القاعدة 4: الكلمات الخضراء
        score += self._score_good_words(domain_name)
        
        # القاعدة 5: كلمات تجارية
        score += self._score_commerce_words(domain_name)
        
        # القاعدة 6: تقييم الامتداد
        score += self._score_tld(tld)
        
        # القاعدة 7: عدد الكلمات
        score += self._score_word_count(domain_name)
        
        # القاعدة 8: صيغة brandable
        score += self._score_brandability(domain_name)
        
        # تأكد إن الدرجة ما تزيد عن 100
        return min(score, 100)
    
    def _score_length(self, length):
        """
        تقييم طول الدومين
        أفضل طول: 8-12 حرف
        """
        if 8 <= length <= 12:
            return 15
        elif 6 <= length <= 14:
            return 10
        elif 5 <= length <= 15:
            return 5
        else:
            return 0
    
    def _score_clean_name(self, domain_name):
        """
        تقييم النظافة (بدون أرقام، بدون هايفن)
        """
        points = 0
        
        # بدون هايفن = +15
        if '-' not in domain_name:
            points += 15
        
        # بدون أرقام = +10
        if not any(char.isdigit() for char in domain_name):
            points += 10
        
        return points
    
    def _score_red_flags(self, domain_name):
        """
        فحص الكلمات الحمراء
        كل red flag = -10 درجات
        """
        points = 15  # نقطة البداية
        
        for flag in self.red_flags:
            if flag in domain_name.lower():
                points -= 10
        
        return max(points, 0)  # لا تزيد عن الصفر
    
    def _score_good_words(self, domain_name):
        """
        فحص الكلمات الخضراء
        كل good word = +15 درجة
        """
        points = 0
        
        for word in self.good_words:
            if word in domain_name.lower():
                points += 15
                break  # نقطة واحدة فقط للكلمات الخضراء
        
        return min(points, 15)
    
    def _score_commerce_words(self, domain_name):
        """
        فحص كلمات تجارية
        كل كلمة تجارية = +10 درجات
        """
        points = 0
        
        for word in self.commerce_words:
            if word in domain_name.lower():
                points += 10
                break
        
        return min(points, 10)
    
    def _score_tld(self, tld):
        """
        تقييم الامتداد (TLD)
        """
        if tld == 'com':
            return 20  # .com الأفضل
        elif tld in ['ai', 'io', 'co', 'app']:
            return 12  # Extensions حديثة جيدة
        elif tld in ['net', 'org', 'biz']:
            return 5   # Acceptable
        else:
            return 0   # غير مقبول
    
    def _score_word_count(self, domain_name):
        """
        تقييم عدد الكلمات
        أفضل: كلمتان واضحتان
        """
        # عدّ الأحرف الكبيرة (تشير للكلمات)
        capital_count = sum(1 for c in domain_name if c.isupper())
        
        if capital_count == 1:  # كلمة واحدة فقط
            return 5
        elif capital_count == 2:  # كلمتان (مثالي)
            return 15
        elif capital_count >= 3:  # أكثر من كلمتان
            return 3
        else:
            return 0
    
    def _score_brandability(self, domain_name):
        """
        تقييم الصيغة الـ brandable
        """
        points = 0
        
        # طول الكلمات معقول؟
        if 3 <= len(domain_name) <= 20:
            points += 5
        
        # محتوي حروف متنوعة (consonants و vowels)؟
        vowels = sum(1 for c in domain_name if c.lower() in 'aeiou')
        consonants = len(domain_name) - vowels
        
        if vowels > 0 and consonants > 0:
            points += 5
        
        # ما فيش تكرار حروف كثير
        if len(set(domain_name)) >= len(domain_name) * 0.6:
            points += 5
        
        return points
    
    def get_score_breakdown(self, domain):
        """
        يعطيك تفصيل الدرجة
        (للـ debugging والفهم)
        """
        domain_name = domain.split('.')[0].lower()
        tld = domain.split('.')[-1].lower()
        
        breakdown = {
            'domain': domain,
            'length': self._score_length(len(domain_name)),
            'cleanness': self._score_clean_name(domain_name),
            'red_flags': self._score_red_flags(domain_name),
            'good_words': self._score_good_words(domain_name),
            'commerce': self._score_commerce_words(domain_name),
            'tld': self._score_tld(tld),
            'word_count': self._score_word_count(domain_name),
            'brandability': self._score_brandability(domain_name),
            'total': self.score_domain(domain)
        }
        
        return breakdown


# اختبر الـ scorer
if __name__ == '__main__':
    scorer = DomainScorer()
    
    # قائمة الدومينات للاختبار
    test_domains = [
        'RelayParcel.com',
        'CopperRental.com',
        'iDrape.com',
        'PowerImagery.com',
        'VisionsEstate.com',
        'OpenWad.com',
    ]
    
    print("=" * 70)
    print("🎯 DOMAIN SCORER TEST")
    print("=" * 70)
    
    for domain in test_domains:
        score = scorer.score_domain(domain)
        breakdown = scorer.get_score_breakdown(domain)
        
        print(f"\n📊 {domain}")
        print(f"   Length: {breakdown['length']}/15")
        print(f"   Cleanness: {breakdown['cleanness']}/25")
        print(f"   Red Flags: {breakdown['red_flags']}/15")
        print(f"   Good Words: {breakdown['good_words']}/15")
        print(f"   Commerce: {breakdown['commerce']}/10")
        print(f"   TLD: {breakdown['tld']}/20")
        print(f"   Word Count: {breakdown['word_count']}/15")
        print(f"   Brandability: {breakdown['brandability']}/15")
        print(f"   ─────────────")
        print(f"   TOTAL SCORE: {breakdown['total']}/100")
        
        if score >= 75:
            print(f"   ✅ STRONG")
        elif score >= 60:
            print(f"   🟡 AVERAGE")
        else:
            print(f"   🔴 WEAK")
            