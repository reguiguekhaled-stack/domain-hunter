# Domain Hunter الكامل: Scraper + Scorer + Database

from scraper import DomainScraper
from scorer import DomainScorer
from database import DomainDatabase

print("=" * 70)
print("🎯 DOMAIN HUNTER - COMPLETE PIPELINE")
print("=" * 70)

# أنشئ instances
scraper = DomainScraper()
scorer = DomainScorer()
db = DomainDatabase('domains.db')

# Step 1: اسحب الدومينات
print("\n[1/4] 🕷️  استخراج الدومينات...")
domains = scraper.get_domains()

print(f"✅ تم استخراج {len(domains)} دومين")

# Step 2: قيّم الدومينات
print("\n[2/4] 🧮 تقييم الدومينات...")
print("─" * 70)

qualified_count = 0
for domain in domains:
    # احسب الدرجة
    score = scorer.score_domain(domain)
    
    # استخرج TLD والطول
    tld = domain.split('.')[-1]
    length = len(domain.split('.')[0])
    
    # أضف في قاعدة البيانات
    db.insert_domain(domain, tld, length, score)
    
    # اطبع النتيجة
    status = "✅" if score >= 75 else "🟡" if score >= 60 else "🔴"
    print(f"{domain:30} → Score: {score:3}/100 {status}")
    
    if score >= 75:
        qualified_count += 1

# Step 3: عرض الإحصائيات
print("\n[3/4] 📊 الإحصائيات:")
print("─" * 70)

total = db.count_domains()
print(f"إجمالي الدومينات: {total}")
print(f"دومينات جيدة (75+): {qualified_count}")
print(f"نسبة النجاح: {qualified_count}/{len(domains)} ({qualified_count*100/len(domains):.1f}%)")

# Step 4: عرض الدومينات الجيدة
print("\n[4/4] ✨ الدومينات الجيدة (Score >= 75):")
print("─" * 70)

qualified = db.get_qualified_domains(min_score=75)
for i, domain in enumerate(qualified, 1):
    domain_name = domain[1]
    score = domain[4]
    print(f"{i}. {domain_name:30} → {score}/100")

# صدّر التقرير
db.export_to_csv('daily_report.csv')

print("\n" + "=" * 70)
print("✅ Pipeline كامل نجح!")
print("=" * 70)