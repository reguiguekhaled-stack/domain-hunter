from email_sender import EmailSender
from config import SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL

print("=" * 70)
print("🧪 EMAIL OFFLINE TEST (بدون إرسال فعلي)")
print("=" * 70)

# أنشئ instance
sender = EmailSender(SENDER_EMAIL, APP_PASSWORD)

# أنشئ بيانات اختبار
test_domains = [
    (1, 'techvault.com', 'com', 9, 85, 0, 0, '', '2026-04-19', 'new'),
    (2, 'tradingflow.com', 'com', 11, 82, 0, 0, '', '2026-04-19', 'new'),
    (3, 'securepayment.co', 'co', 14, 80, 0, 0, '', '2026-04-19', 'new'),
]

# أنشئ HTML بدون إرسال
print("\n📧 جاري إنشاء التقرير HTML...")
html = sender.create_html_report(test_domains)

# احفظه في ملف
with open('sample_report.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ تم إنشاء التقرير!")
print("   الملف: sample_report.html")
print("   افتح الملف في المتصفح لترى التقرير")

print("\n" + "=" * 70)