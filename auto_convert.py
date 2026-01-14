"""
Auto-convert latest HTML file to Google Doc
Run this after n8n workflow uploads HTML
"""

import os
import sys
import pickle
import io

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except ImportError:
    print("Installing packages...")
    os.system('pip install google-auth google-auth-oauthlib google-api-python-client')
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = "1CwmxaJ5LEvokptosoiNx1rHXC-wL110-"  # Your ProgrammX folder

def get_creds():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
    return creds

def convert(file_id):
    """Convert HTML file to Google Doc"""
    service = build('drive', 'v3', credentials=get_creds())
    
    # Get file info
    info = service.files().get(fileId=file_id, fields='name,parents').execute()
    name = info['name'].replace('.html', '')
    parents = info.get('parents', [FOLDER_ID])
    
    print(f"Converting: {info['name']} -> {name}")
    
    # Download HTML
    request = service.files().get_media(fileId=file_id)
    content = io.BytesIO()
    downloader = MediaIoBaseDownload(content, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    
    # Save temp file
    content.seek(0)
    with open('temp.html', 'wb') as f:
        f.write(content.read())
    
    # Upload as Google Doc
    metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.document',
        'parents': parents
    }
    media = MediaFileUpload('temp.html', mimetype='text/html')
    result = service.files().create(body=metadata, media_body=media, fields='id,name,webViewLink').execute()
    
    os.remove('temp.html')
    
    print(f"\n✅ Created Google Doc!")
    print(f"   Name: {result['name']}")
    print(f"   Link: {result['webViewLink']}")
    
    return result

def get_latest_html():
    """Get most recent HTML file in folder"""
    service = build('drive', 'v3', credentials=get_creds())
    results = service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType='text/html'",
        orderBy='createdTime desc',
        pageSize=1,
        fields='files(id,name)'
    ).execute()
    files = results.get('files', [])
    return files[0] if files else None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_id = sys.argv[1]
    else:
        print("Finding latest HTML file...")
        latest = get_latest_html()
        if latest:
            file_id = latest['id']
            print(f"Found: {latest['name']}")
        else:
            print("No HTML files found!")
            sys.exit(1)
    
    convert(file_id)

