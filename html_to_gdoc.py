"""
Convert HTML file in Google Drive to Google Doc
Simple script - just run it!
"""

import os
import pickle
import io
import sys

# Install required packages if not present
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
except ImportError:
    print("Installing required packages...")
    os.system('pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client')
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# Scopes
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():
    """Get Google API credentials"""
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("=" * 60)
                print("ERROR: credentials.json not found!")
                print("=" * 60)
                print("""
How to create credentials.json:

1. Go to: https://console.cloud.google.com
2. Select project: 466549990081
3. Go to: APIs & Services → Credentials
4. Click: Create Credentials → OAuth client ID
5. Select: Desktop app
6. Click: Create
7. Click: Download JSON
8. Rename file to: credentials.json
9. Move to: C:\\Users\\PC\\Desktop\\Seo_Audit_Report\\
10. Run this script again!
                """)
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds


def convert_html_to_gdoc(file_id):
    """
    Convert HTML file to Google Doc
    
    Args:
        file_id: Google Drive file ID of the HTML file
    
    Returns:
        dict: New Google Doc info (id, name, webViewLink)
    """
    print("=" * 60)
    print("   HTML → GOOGLE DOC CONVERTER")
    print("=" * 60)
    
    creds = get_credentials()
    if not creds:
        return None
    
    service = build('drive', 'v3', credentials=creds)
    
    try:
        # Step 1: Get file info
        print("\n[1/4] Getting file info...")
        file_info = service.files().get(
            fileId=file_id, 
            fields='name, parents, mimeType'
        ).execute()
        
        original_name = file_info.get('name', 'Document')
        parents = file_info.get('parents', [])
        mime_type = file_info.get('mimeType', '')
        
        print(f"      File: {original_name}")
        print(f"      Type: {mime_type}")
        
        # Step 2: Download HTML content
        print("\n[2/4] Downloading HTML content...")
        request = service.files().get_media(fileId=file_id)
        content = io.BytesIO()
        downloader = MediaIoBaseDownload(content, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"      Progress: {int(status.progress() * 100)}%")
        
        content.seek(0)
        html_content = content.read()
        print(f"      Downloaded: {len(html_content)} bytes")
        
        # Step 3: Save temporarily
        print("\n[3/4] Processing...")
        temp_file = 'temp_convert.html'
        with open(temp_file, 'wb') as f:
            f.write(html_content)
        
        # Step 4: Upload as Google Doc
        print("\n[4/4] Creating Google Doc...")
        
        # New name without .html
        new_name = original_name.replace('.html', '').replace('.htm', '')
        
        file_metadata = {
            'name': new_name,
            'mimeType': 'application/vnd.google-apps.document'  # This converts to Google Doc!
        }
        
        if parents:
            file_metadata['parents'] = parents
        
        media = MediaFileUpload(
            temp_file, 
            mimetype='text/html',
            resumable=True
        )
        
        new_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink, mimeType'
        ).execute()
        
        # Cleanup
        os.remove(temp_file)
        
        # Success!
        print("\n" + "=" * 60)
        print("   ✅ CONVERSION SUCCESSFUL!")
        print("=" * 60)
        print(f"\n   New Document:")
        print(f"   • Name: {new_file.get('name')}")
        print(f"   • ID:   {new_file.get('id')}")
        print(f"   • Type: {new_file.get('mimeType')}")
        print(f"\n   📄 Open in browser:")
        print(f"   {new_file.get('webViewLink')}")
        print("\n" + "=" * 60)
        
        return new_file
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


def list_recent_html_files():
    """List recent HTML files in Google Drive"""
    creds = get_credentials()
    if not creds:
        return []
    
    service = build('drive', 'v3', credentials=creds)
    
    results = service.files().list(
        q="mimeType='text/html'",
        orderBy="createdTime desc",
        pageSize=10,
        fields="files(id, name, createdTime, parents)"
    ).execute()
    
    files = results.get('files', [])
    
    print("\n" + "=" * 60)
    print("   RECENT HTML FILES IN GOOGLE DRIVE")
    print("=" * 60)
    
    if not files:
        print("\n   No HTML files found!")
        return []
    
    for i, f in enumerate(files, 1):
        print(f"\n   [{i}] {f['name']}")
        print(f"       ID: {f['id']}")
    
    print("\n" + "=" * 60)
    return files


# =============================================================
# MAIN - Run this!
# =============================================================

if __name__ == "__main__":
    
    # YOUR FILE ID - Replace with your HTML file ID
    # Or pass as command line argument: python html_to_gdoc.py FILE_ID
    
    if len(sys.argv) > 1:
        # File ID from command line
        file_id = sys.argv[1]
    else:
        # Default: List files and convert most recent
        print("\nNo file ID provided. Listing recent HTML files...\n")
        files = list_recent_html_files()
        
        if files:
            print("\nConvert the most recent file? (y/n): ", end="")
            choice = input().strip().lower()
            
            if choice == 'y':
                file_id = files[0]['id']
            else:
                print("\nEnter file ID to convert: ", end="")
                file_id = input().strip()
        else:
            print("\nNo HTML files found. Please provide a file ID.")
            sys.exit(1)
    
    # Convert!
    result = convert_html_to_gdoc(file_id)
    
    if result:
        print("\n✅ Done! Your Google Doc is ready.")
    else:
        print("\n❌ Conversion failed. Check the error above.")

