#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail account and app password
GMAIL_USER = "uniteldistributorsltd786@gmail.com"
GMAIL_APP_PASSWORD = "zvrgljgmqqywvdxs"  # TikTokAnalyticsBot App Password
TO_EMAIL = "uniteldistributorsltd786@gmail.com"

def send_email(subject, body, to_email=TO_EMAIL):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"Email sent to {to_email} at {datetime.now(timezone.utc)} UTC")

    except Exception as e:
        print("Failed to send email:", e)

def get_peak_hour():
    # Example: read from file or calculate analytics
    try:
        if os.path.exists("best_hour.txt"):
            with open("best_hour.txt", "r") as f:
                return int(f.read().strip())
        else:
            return 14  # default peak hour
    except Exception:
        return 14

def main():
    now = datetime.now(timezone.utc)
    peak_hour = get_peak_hour()

    print(f"Weekly analytics completed. Updated peak hour: {peak_hour} UTC")
    notification_msg = f"📊 Weekly Analytics Completed. Updated peak hour: {peak_hour} UTC at {now.isoformat()}"

    send_email("Weekly Analytics Update", notification_msg)

if __name__ == "__main__":
    main()
