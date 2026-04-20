import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import random
import socket


class DomainScraper:
    def __init__(self):
        """Web Scraper للدومينات"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }

    # =============================
    # 🔥 NEW: DOMAIN GENERATOR
    # =============================
    def generate_domains(self):
        print("🧠 توليد domains ذكية...")

        keywords = [
            "ai", "tech", "cloud", "data", "crypto",
            "shop", "market", "digital", "fast", "smart"
        ]

        suffixes = [
            "hub", "lab", "pro", "flow", "base",
            "zone", "core", "space", "works"
        ]

        domains = []

        for _ in range(100):
            name = random.choice(keywords) + random.choice(suffixes)
            domains.append(name + ".com")

        print(f"✅ تم توليد {len(domains)} دومين")
        return domains

    # =============================
    # 🔥 NEW: AVAILABILITY CHECK
    # =============================
    def is_available(self, domain):
        try:
            socket.gethostbyname(domain)
            return False  # محجوز
        except:
            return True   # متاح

    def filter_available_domains(self, domains):
        print("🔍 فحص الدومينات...")

        available = []

        for d in domains:
            if self.is_available(d):
                print(f"💰 متاح: {d}")
                available.append(d)

        print(f"✅ المتاح: {len(available)}")
        return available

    # =============================
    # OLD SCRAPING (احتياطي)
    # =============================
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

            return self._get_fallback_domains()

        except Exception as e:
            print(f"❌ خطأ في الاتصال: {e}")
            return self._get_fallback_domains()

    def scrape_api_domains(self):
        print("📥 محاولة API (احتياطي)...")

        url = "https://api.domainsdb.info/v1/domains/search?domain=shop"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                return []

            data = response.json()

            domains = []
            for item in data.get("domains", []):
                domain = item.get("domain")
                if domain:
                    domains.append(domain)

            return domains

        except:
            return []

    def _get_fallback_domains(self):
        print("⚠️ fallback domains")

        return [
            'techvault.com',
            'smartlogistics.net',
            'innovatehub.io',
            'tradingflow.com',
            'databridge.app'
        ]

    # =============================
    # CLEAN + VALIDATE
    # =============================
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

    # =============================
    # 🔥 MAIN PIPELINE (UPDATED)
    # =============================
    def get_domains(self):
        print("=" * 70)
        print("🚀 DOMAIN GENERATOR + CHECKER")
        print("=" * 70)

        # 1. توليد domains
        generated = self.generate_domains()

        # 2. فحص availability
        available = self.filter_available_domains(generated)

        # 3. تنظيف
        clean_domains = []
        seen = set()

        for domain in available:
            cleaned = self.clean_domain(domain)

            if cleaned not in seen and self.validate_domain(cleaned):
                clean_domains.append(cleaned)
                seen.add(cleaned)

        print(f"\n✅ النتائج النهائية: {len(clean_domains)}")

        return clean_domains[:20]