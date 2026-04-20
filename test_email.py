from email_sender import EmailSender
from config import SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL

print("=" * 70)
print("🧪 EMAIL INTEGRATION TEST")
print("=" * 70)

# أنشئ instance
sender = EmailSender(SENDER_EMAIL, APP_PASSWORD)

# أرسل بريد اختبار
success = sender.send_test_email(RECEIVER_EMAIL)

if success:
    print("\n✅ تم إرسال البريد بنجاح!")
    print(f"   تحقق من بريدك: {RECEIVER_EMAIL}")
else:
    print("\n❌ فشل إرسال البريد")
    print("   تحقق من البريد و App Password")

print("=" * 70)