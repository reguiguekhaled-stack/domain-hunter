import time
import requests


class DomainScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }

    def scrape_real_domains(self):
        print("📥 جاري جلب الدومينات من API...")

        url = "https://api.domainsdb.info/v1/domains/search?domain=com"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                print(f"❌ فشل الطلب: {response.status_code}")
                return []

            data = response.json()

            domains = []
            for item in data.get("domains", []):
                domain = item.get("domain")
                if domain:
                    domains.append(domain)

            print(f"✅ تم جلب {len(domains)} دومين")
            return domains

        except Exception as e:
            print(f"❌ خطأ أثناء الجلب: {e}")
            return []

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
                domains = self.scrape_real_domains()
                if domains:
                    return domains

            except Exception as e:
                print(f"❌ محاولة {attempt + 1} فشلت: {str(e)}")

            wait_time = 5 * (attempt + 1)
            print(f"⏳ إعادة المحاولة بعد {wait_time} ثانية...")
            time.sleep(wait_time)

        return []

    def get_domains(self):
        print("=" * 70)
        print("🕷️ DOMAIN SCRAPER (REAL)")
        print("=" * 70)

        raw_domains = self.scrape_with_retry()

        clean_domains = []
        for domain in raw_domains:
            cleaned = self.clean_domain(domain)
            if self.validate_domain(cleaned):
                clean_domains.append(cleaned)

        print("\n✅ النتائج:")
        print(f"   الخام: {len(raw_domains)}")
        print(f"   بعد التنظيف: {len(clean_domains)}")

        return clean_domains
