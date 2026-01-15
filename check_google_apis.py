"""
Check which Google APIs are enabled for your project.
Note: This requires the Google Cloud SDK or service account credentials.

For OAuth2 credentials (Client ID/Secret), you need to check manually
in the Google Cloud Console:
https://console.cloud.google.com/apis/dashboard

This script shows you what to check:
"""

print("=" * 60)
print("    HOW TO CHECK ENABLED GOOGLE APIs")
print("=" * 60)

print("""
Since you're using OAuth2 (Client ID & Secret), you need to 
check enabled APIs in the Google Cloud Console:

STEP 1: Open Google Cloud Console
   https://console.cloud.google.com

STEP 2: Select your project
   Project ID: 466549990081

STEP 3: Go to APIs & Services
   Left menu → "APIs & Services" → "Enabled APIs & services"

STEP 4: Check if these APIs are enabled:
""")

apis_to_check = [
    ("Google Drive API", "drive.googleapis.com", "Creating/uploading files"),
    ("Google Docs API", "docs.googleapis.com", "Editing document content"),
    ("Gmail API", "gmail.googleapis.com", "Sending emails"),
    ("Google Sheets API", "sheets.googleapis.com", "Working with spreadsheets"),
]

print("-" * 60)
print(f"{'API Name':<25} {'Required For':<30}")
print("-" * 60)

for name, endpoint, purpose in apis_to_check:
    print(f"{name:<25} {purpose:<30}")

print("-" * 60)

print("""
QUICK LINKS TO ENABLE APIs:

1. Google Drive API:
   https://console.cloud.google.com/apis/library/drive.googleapis.com?project=466549990081

2. Google Docs API (YOU NEED THIS!):
   https://console.cloud.google.com/apis/library/docs.googleapis.com?project=466549990081

3. Gmail API:
   https://console.cloud.google.com/apis/library/gmail.googleapis.com?project=466549990081

""")

print("=" * 60)
print("  Click each link above and press 'ENABLE' if not enabled")
print("=" * 60)

