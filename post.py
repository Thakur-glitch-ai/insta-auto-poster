import requests
import time
import os

# GitHub Secrets se token aur ID uthayega
ACCESS_TOKEN = os.environ.get("IG_TOKEN")
IG_USER_ID = os.environ.get("IG_USER_ID")

IMAGE_URL = "https://images.unsplash.com/photo-1586281380349-632531db7ed4?q=80&w=1000" 
CAPTION = "Top 3 ATS Resume Tips for Freshers! 🚀\n\n1. Use standard headings.\n2. Save as PDF.\n3. Avoid tables and graphics.\n\n#ResumeTips #ATS #CareerAdvice #GetShortlisted"

def post_to_instagram():
    print("1. Creating media container...")
    create_url = f"https://graph.instagram.com/v20.0/{IG_USER_ID}/media"
    
    payload = {
        'image_url': IMAGE_URL,
        'caption': CAPTION,
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(create_url, data=payload)
    result = response.json()
    
    if 'id' not in result:
        print("Error creating container:", result)
        return
        
    creation_id = result['id']
    print(f"Container created! ID: {creation_id}")
    
    print("2. Waiting for Instagram to process...")
    time.sleep(10) 
    
    print("3. Publishing post...")
    publish_url = f"https://graph.instagram.com/v20.0/{IG_USER_ID}/media_publish"
    publish_payload = {
        'creation_id': creation_id,
        'access_token': ACCESS_TOKEN
    }
    
    publish_response = requests.post(publish_url, data=publish_payload)
    publish_result = publish_response.json()
    
    if 'id' in publish_result:
        print("Success! Post published.")
    else:
        print("Error publishing:", publish_result)

if __name__ == "__main__":
    post_to_instagram()
