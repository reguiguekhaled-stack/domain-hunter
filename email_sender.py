import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSender:
    def __init__(self, sender_email, app_password):
        """إرسال التقارير عبر Gmail"""
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 465
    
    def create_html_report(self, domains_data):
        """ينشئ تقرير HTML جميل"""
        
        # أنشئ صفوف الجدول
        table_rows = ""
        strong_count = 0
        
        for domain in domains_data:
            domain_name = domain[1]
            score = domain[4]
            tld = domain[2]
            length = domain[3]
            
            if score >= 75:
                row_class = "strong"
                strong_count += 1
            elif score >= 60:
                row_class = "average"
            else:
                row_class = "weak"
            
            table_rows += f'<tr class="{row_class}"><td><strong>{domain_name}</strong></td><td>{score}/100</td><td>{tld}</td><td>{length}</td></tr>'
        
        # HTML بسيط (بدون indentation معقدة)
        html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; margin: 0; padding: 20px; }}
.container {{ background-color: white; border-radius: 10px; padding: 30px; max-width: 800px; margin: 0 auto; }}
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 5px; text-align: center; }}
.header h1 {{ margin: 0; font-size: 28px; }}
.header p {{ margin: 5px 0 0 0; font-size: 14px; }}
.stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; }}
.stat-box {{ background-color: #f9f9f9; padding: 15px; border-left: 4px solid #667eea; border-radius: 3px; }}
.stat-label {{ color: #666; font-size: 12px; text-transform: uppercase; }}
.stat-value {{ color: #333; font-size: 24px; font-weight: bold; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
th {{ background-color: #667eea; color: white; padding: 12px; text-align: left; font-weight: bold; }}
td {{ padding: 12px; border-bottom: 1px solid #eee; }}
tr:hover {{ background-color: #f5f5f5; }}
.strong {{ background-color: #d4edda; }}
.average {{ background-color: #fff3cd; }}
.weak {{ background-color: #f8d7da; }}
.footer {{ text-align: center; margin-top: 20px; color: #999; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🎯 Domain Hunter Report</h1>
<p>{datetime.now().strftime('%B %d, %Y at %H:%M')}</p>
</div>

<div class="stats">
<div class="stat-box">
<div class="stat-label">Total Domains</div>
<div class="stat-value">{len(domains_data)}</div>
</div>
<div class="stat-box">
<div class="stat-label">Strong (75+)</div>
<div class="stat-value">{strong_count}</div>
</div>
</div>

<table>
<tr>
<th>Domain</th>
<th>Score</th>
<th>TLD</th>
<th>Length</th>
</tr>
{table_rows}
</table>

<div class="footer">
<p>This is an automated report from Domain Hunter</p>
</div>
</div>
</body>
</html>'''
        
        return html
    
    def send_report(self, receiver_email, subject, domains_data):
        """يرسل التقرير عبر البريد"""
        try:
            # أنشئ الرسالة
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = receiver_email
            
            # أنشئ HTML report
            html_report = self.create_html_report(domains_data)
            
            # أضف الـ HTML
            html_part = MIMEText(html_report, 'html')
            message.attach(html_part)
            
            # اتصل بـ Gmail
            print("📧 جاري الاتصال بـ Gmail...")
            
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.app_password)
                server.sendmail(self.sender_email, receiver_email, message.as_string())
            
            print(f"✅ تم إرسال التقرير إلى {receiver_email}")
            return True
        
        except smtplib.SMTPAuthenticationError:
            print("❌ خطأ في المصادقة - تحقق من البريد و App Password")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ خطأ في إرسال البريد: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
            return False
    
    def send_test_email(self, receiver_email):
        """يرسل بريد اختبار"""
        print("=" * 70)
        print("📧 EMAIL SENDER TEST")
        print("=" * 70)
        
        test_domains = [
            (1, 'techvault.com', 'com', 9, 85, 0, 0, '', '2026-04-19', 'new'),
            (2, 'tradingflow.com', 'com', 11, 82, 0, 0, '', '2026-04-19', 'new'),
            (3, 'securepayment.co', 'co', 14, 80, 0, 0, '', '2026-04-19', 'new'),
        ]
        
        success = self.send_report(
            receiver_email,
            f"🎯 Domain Hunter Report - {datetime.now().strftime('%Y-%m-%d')}",
            test_domains
        )
        
        return success