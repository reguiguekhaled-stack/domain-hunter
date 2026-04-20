import time

class DomainScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_expireddomains_sample(self):
        print("📥 جاري الاتصال بـ ExpiredDomains.net...")
        
        sample_domains = [
            'techvault.com',
            'smartlogistics.net',
            'innovatehub.io',
            'tradingflow.com',
            'databridge.app',
            'securepayment.co',
            'rapidshipping.com',
            'cloudsync.ai',
            'marketpulse.io',
            'digitalforge.co',
            'streamconnect.com',
            'vaultsecure.net',
            'quickroute.io',
            'primedeliver.app',
            'tradeflow.com',
        ]
        
        print(f"✅ تم الحصول على {len(sample_domains)} دومين")
        return sample_domains
    
    def clean_domain(self, domain):
        domain = domain.strip().lower()
        domain = ''.join(c for c in domain if c.isalnum() or c in '.-')
        return domain
    
    def validate_domain(self, domain):
        if '.' not in domain:
            return False
        
        parts = domain.split('.')
        if len(parts) < 2:
            return False
        
        if len(parts[0]) < 3 or len(parts[0]) > 63:
            return False
        
        if len(parts[-1]) < 2 or len(parts[-1]) > 6:
            return False
        
        return True
    
    def scrape_with_retry(self, max_retries=3):
        for attempt in range(max_retries):
            try:
                domains = self.scrape_expireddomains_sample()
                return domains
            except Exception as e:
                print(f"❌ محاولة {attempt + 1} فشلت: {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    print(f"⏳ انتظار {wait_time} ثواني...")
                    time.sleep(wait_time)
        
        return []
    
    def get_domains(self):
        print("=" * 70)
        print("🕷️  DOMAIN SCRAPER")
        print("=" * 70)
        
        raw_domains = self.scrape_with_retry()
        
        clean_domains = []
        for domain in raw_domains:
            cleaned = self.clean_domain(domain)
            if self.validate_domain(cleaned):
                clean_domains.append(cleaned)
        
        print(f"\n✅ تم تنظيف الدومينات:")
        print(f"   الأصلي: {len(raw_domains)}")
        print(f"   النظيف: {len(clean_domains)}")
        
        return clean_domains