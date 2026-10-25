import requests
import time
import os
import random
import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# GITHUB SECRETS SE DETAILS UTHAYEGA
# ==========================================
ACCESS_TOKEN = os.environ.get("IG_TOKEN")
IG_USER_ID = os.environ.get("IG_USER_ID")
PIXABAY_API_KEY = os.environ.get("PIXABAY_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_KEY")
IMGBB_API_KEY = os.environ.get("IMGBB_KEY")

def get_tips_from_gemini():
    print("1. Asking Gemini for 5 random ATS Resume tips...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={GEMINI_API_KEY}"
    
    # PROMPT UPDATED: Strictly maximum 8 words
    prompt = "Give me exactly 5 short, actionable ATS resume tips for freshers. Each tip must be a single sentence, strictly maximum 8 words. Do not include numbers, bullet points, or intro/outro text. Separate each tip with a new line."
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        
        if 'candidates' not in result:
            print("❌ Gemini API Error:", result)
            return get_fallback_tips()
            
        text_response = result['candidates'][0]['content']['parts'][0]['text']
        tips = [line.strip() for line in text_response.strip().split('\n') if line.strip()]
        tips = tips[:5]
        
        if len(tips) < 3:
            print("⚠️ Gemini returned insufficient tips, using fallback.")
            return get_fallback_tips()
            
        print(f"✅ Gemini Tips: {tips}")
        return tips
        
    except Exception as e:
        print(f"❌ Gemini Exception: {e}. Using fallback tips.")
        return get_fallback_tips()

def get_fallback_tips():
    fallback = [
        "Use a clean, simple format for ATS.",
        "Customize your resume for each job.",
        "Save your resume as a standard PDF.",
        "Avoid tables, images, or special characters.",
        "Quantify achievements with numbers and percentages."
    ]
    return random.sample(fallback, 5)

def fetch_and_create_image():
    print("2. Fetching random image from Pixabay...")
    search_query = random.choice(["office desk", "job interview", "laptop workspace", "career", "resume"])
    pixabay_url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={search_query}&image_type=photo&orientation=square&per_page=3"
    
    response = requests.get(pixabay_url)
    data = response.json()
    
    if not data.get('hits'):
        img_url = "https://images.unsplash.com/photo-1586281380349-632531db7ed4?q=80&w=1080&h=1080&fit=crop"
    else:
        img_url = random.choice(data['hits'])['largeImageURL']
    
    print(f"Downloading image: {img_url}")
    img_response = requests.get(img_url)
    img = Image.open(BytesIO(img_response.content)).convert("RGBA")
    img = img.resize((1080, 1080))

    overlay = Image.new('RGBA', img.size, (0, 0, 0, 160))
    img = Image.alpha_composite(img, overlay)
    
    draw = ImageDraw.Draw(img)
    
    try:
        # FONT SIZE UPDATED: Reduced from 45 to 40
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 55)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    draw.text((50, 80), "TOP 5 ATS RESUME TIPS", font=title_font, fill="white")
    
    tips = get_tips_from_gemini()
    
    # POSITIONING UPDATED: Starts higher and tighter gaps
    y_offset = 220
    
    for i, tip in enumerate(tips):
        words = tip.split()
        lines = []
        current_line = ""
        for word in words:
            # Increased width limit slightly to 950 so text doesn't wrap too early
            if draw.textlength(current_line + " " + word, font=font) < 950:
                current_line += " " + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        draw.text((50, y_offset), f"{i+1}. ", font=font, fill="#FFD700")
        for line in lines:
            draw.text((100, y_offset), line, font=font, fill="white")
            y_offset += 50 # Reduced from 60
        y_offset += 15 # Reduced from 20

    image_path = "final_post.jpg"
    img.convert("RGB").save(image_path, quality=90)
    print("✅ Image created successfully!")
    return image_path, tips

def upload_image_to_host(image_path):
    print("3. Uploading image to temporary host (ImgBB)...")
    url = "https://api.imgbb.com/1/upload"
    
    with open(image_path, "rb") as file:
        payload = {
            "key": IMGBB_API_KEY,
            "image": base64.b64encode(file.read())
        }
        
    response = requests.post(url, data=payload)
    result = response.json()
    
    if result.get("success"):
        print("✅ Image uploaded successfully to ImgBB!")
        return result["data"]["url"]
    else:
        print(f"❌ Upload Error: {result}")
        return None

def post_to_instagram(image_url, tips):
    print("4. Creating media container...")
    caption = "Top 5 ATS Resume Tips! 🚀\n\n" + "\n".join([f"👉 {tip}" for tip in tips]) + "\n\n#ResumeTips #ATS #CareerAdvice #GetShortlisted"
    
    create_url = f"https://graph.instagram.com/v20.0/{IG_USER_ID}/media"
    payload = {'image_url': image_url, 'caption': caption, 'access_token': ACCESS_TOKEN}
    
    response = requests.post(create_url, data=payload).json()
    
    if 'id' not in response:
        print("❌ Error creating container:", response)
        return
        
    creation_id = response['id']
    print(f"✅ Container created! ID: {creation_id}")
    
    print("5. Waiting for Instagram to process (10 seconds)...")
    time.sleep(10) 
    
    print("6. Publishing post...")
    publish_url = f"https://graph.instagram.com/v20.0/{IG_USER_ID}/media_publish"
    publish_payload = {'creation_id': creation_id, 'access_token': ACCESS_TOKEN}
    
    publish_response = requests.post(publish_url, data=publish_payload).json()
    
    if 'id' in publish_response:
        print("🎉 Success! Post published successfully.")
    else:
        print("❌ Error publishing:", publish_response)

if __name__ == "__main__":
    image_path, chosen_tips = fetch_and_create_image()
    if image_path:
        public_image_url = upload_image_to_host(image_path)
        if public_image_url:
            post_to_instagram(public_image_url, chosen_tips)
        else:
            print("Script stopped because image upload failed.")
