import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


class DomainScraper:
    def __init__(self):
        """Web Scraper للدومينات المنتهية"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }

    def scrape_namejet_pending(self):
        print("📥 جاري الاتصال بـ NameJet...")

        url = "https://www.namejet.com/Pages/Auctions/PendingDelete.aspx"

        try:
            response = requests.get(url, headers=self.headers, timeout=15)

            if response.status_code != 200:
                print(f"❌ فشل الاتصال: {response.status_code}")
                return self._get_fallback_domains()

            soup = BeautifulSoup(response.text, 'html.parser')

            domains = []
            rows = soup.find_all('tr')

            for row in rows[:100]:
                cells = row.find_all('td')

                if len(cells) >= 1:
                    domain_cell = cells[0].get_text(strip=True)

                    if '.' in domain_cell:
                        domain = domain_cell.lower().strip()

                        if domain.endswith('.com'):
                            domains.append(domain)

            if domains:
                print(f"✅ تم الحصول على {len(domains)} دومين من NameJet")
                return domains[:50]

            print("⚠️ لم يتم العثور على دومينات")
            return self._get_fallback_domains()

        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            return self._get_fallback_domains()

    def scrape_expireddomains_rss(self):
        print("📥 جاري الاتصال بـ ExpiredDomains...")

        url = "https://www.expireddomains.net/domain-name-search/?fwhois=22&flimit=500"

        try:
            response = requests.get(url, headers=self.headers, timeout=15)

            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.text, 'html.parser')

            domains = []
            table = soup.find('table', {'class': 'base1'})

            if table:
                rows = table.find_all('tr')[1:]

                for row in rows[:100]:
                    cols = row.find_all('td')

                    if len(cols) >= 1:
                        link = cols[0].find('a')

                        if link:
                            domain = link.get_text(strip=True).lower()

                            if domain.endswith('.com'):
                                domains.append(domain)

            if domains:
                print(f"✅ تم الحصول على {len(domains)} دومين")
                return domains[:50]

            return []

        except Exception as e:
            print(f"❌ خطأ: {e}")
            return []

    def scrape_api_domains(self):
        print("📥 جاري جلب الدومينات من API...")
        print("🔥 API FUNCTION IS RUNNING")

        url = "https://api.domainsdb.info/v1/domains/search?domain=shop"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            print("STATUS:", response.status_code)

            if response.status_code != 200:
                print("❌ API فشل")
                return []

            data = response.json()

            domains = []
            for item in data.get("domains", []):
                domain = item.get("domain")
                if domain:
                    domains.append(domain)

            print(f"✅ تم جلب {len(domains)} دومين من API")
            return domains

        except Exception as e:
            print(f"❌ خطأ: {e}")
            return []

    def _get_fallback_domains(self):
        print("⚠️ استخدام دومينات احتياطية...")

        return [
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

    def clean_domain(self, domain):
        domain = domain.strip().lower()
        return ''.join(c for c in domain if c.isalnum() or c in '.-')

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

    def get_domains(self):
        print("=" * 70)
        print("🕷️ DOMAIN SCRAPER")
        print("=" * 70)

        raw_domains = []

        # API أولاً
        api_domains = self.scrape_api_domains()
        raw_domains.extend(api_domains)

        # fallback إلى NameJet
        if len(raw_domains) < 20:
            namejet_domains = self.scrape_namejet_pending()
            raw_domains.extend(namejet_domains)

        # fallback نهائي
        if not raw_domains:
            raw_domains = self._get_fallback_domains()

        clean_domains = []
        seen = set()

        for domain in raw_domains:
            cleaned = self.clean_domain(domain)

            if cleaned not in seen and self.validate_domain(cleaned):
                clean_domains.append(cleaned)
                seen.add(cleaned)

        print(f"\n✅ النتائج:")
        print(f"   الخام: {len(raw_domains)}")
        print(f"   النظيف: {len(clean_domains)}")

        return clean_domains[:50]