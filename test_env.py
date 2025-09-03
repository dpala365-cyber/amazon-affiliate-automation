from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Fetch values
affiliate_key = os.getenv("DIGISTORE24_AFFILIATE_KEY")
reporting_key = os.getenv("DIGISTORE24_REPORTING_KEY")
affiliate_id = os.getenv("DIGISTORE24_AFFILIATE_ID")

# Print to verify
print("Affiliate Key:", affiliate_key)
print("Reporting Key:", reporting_key)
print("Affiliate ID:", affiliate_id)
