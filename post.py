import requests
import time

# ==========================================
# YAHAN APNI DETAILS BHAREIN
# ==========================================
# Token quotes ke andar bina kisi extra space ke daalein
ACCESS_TOKEN = "IGAA5iBWAwZBJRBZAFpBWjhoNUdKTjd4ZAF9hamlyUDlxTWRNLUdhbUI5MG1uNVk5UHNBZAklaRXVUdHZASZAnRVV1l6RVJBN2kyUXlJOE5acWgyaGwtTzJfNEpCZAHY2c1lPZAjNLV19Tejh5TXB1LWNWUXZAJNmkzMWNHNC02SElfeE9RZAwZDZD" 

# Instagram Business Account ID (Sirf numbers)
IG_USER_ID = "17841480422642486" 

# Image ka public URL (Internet par kahi hosted image ka link)
IMAGE_URL = "https://images.unsplash.com/photo-1586281380349-632531db7ed4?q=80&w=1000" 

# Post ka Caption (Aap ise apne hisaab se badal sakte hain)
CAPTION = "Top 3 ATS Resume Tips for Freshers! 🚀\n\n1. Use standard headings.\n2. Save as PDF.\n3. Avoid tables and graphics.\n\n#ResumeTips #ATS #CareerAdvice #GetShortlisted"

# ==========================================
# CODE LOGIC (ISE CHANGE NA KAREIN)
# ==========================================
def post_to_instagram():
    print("1. Creating media container...")
    
    # Step 1: Create Container (Using graph.instagram.com)
    create_url = f"https://graph.instagram.com/v20.0/{IG_USER_ID}/media"
    
    payload = {
        'image_url': IMAGE_URL,
        'caption': CAPTION,
        'access_token': ACCESS_TOKEN
    }
    
    response = requests.post(create_url, data=payload)
    result = response.json()
    
    # Agar error aaye toh print karein
    if 'id' not in result:
        print("\n❌ Error creating container:")
        print(result)
        return
        
    creation_id = result['id']
    print(f"✅ Container created! ID: {creation_id}")
    
    # Step 2: Wait for Instagram to process the image
    print("2. Waiting for Instagram to process the image (10 seconds)...")
    time.sleep(10) 
    
    # Step 3: Publish the container
    print("3. Publishing post...")
    publish_url = f"https://graph.instagram.com/v20.0/{IG_USER_ID}/media_publish"
    
    publish_payload = {
        'creation_id': creation_id,
        'access_token': ACCESS_TOKEN
    }
    
    publish_response = requests.post(publish_url, data=publish_payload)
    publish_result = publish_response.json()
    
    if 'id' in publish_result:
        print("\n🎉 Success! Post published successfully.")
        print(f"Post ID: {publish_result['id']}")
    else:
        print("\n❌ Error publishing post:")
        print(publish_result)

if __name__ == "__main__":
    post_to_instagram()