import os
import requests
from bs4 import BeautifulSoup

# आपके ब्लॉगर और टेलीग्राम (या अन्य) क्रेडेंशियल्स जो आपने सेट किए होंगे
# (यह स्क्रिप्ट आपके एनवायरनमेंट वेरिएबल्स का इस्तेमाल करेगी)
BLOG_ID = os.environ.get('BLOGGER_BLOG_ID')
API_KEY = os.environ.get('BLOGGER_API_KEY')

def get_existing_posts():
    """ब्लॉगर से पहले से मौजूद पोस्ट्स के टाइटल्स की लिस्ट लाता है ताकि डुप्लीकेट न हो"""
    existing_titles = set()
    if not BLOG_ID or not API_KEY:
        return existing_titles
    
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}&maxResults=50"
    try:
        response = requests.get(url).json()
        if 'items' in response:
            for item in response['items']:
                existing_titles.add(item['title'].strip().lower())
    except Exception as e:
        print(f"Error fetching existing posts: {e}")
    return existing_titles

def post_to_blogger(title, content, labels):
    """ब्लॉगर पर पोस्ट पब्लिश करने का फंक्शन"""
    # यहाँ आपका ब्लॉगर API पोस्टिंग का लॉजिक या ईमेल/एपीआई कोड काम करेगा
    print(f"Posting: {title} with labels {labels}")
    # (बाकी का ब्लॉगर एपीआई/ईमेल कोड जो आपने पहले सेट किया था, वह यहाँ रन होगा)

def scrape_sarkari_result():
    existing_titles = get_existing_posts()
    
    # सरकारी रिजल्ट होमपेज स्क्रैप करना
    url = "https://www.sarkariresult.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # मुख्य बॉक्सेस (Result, Admit Card, Latest Jobs) को खोजना
        sections = {
            'Latest Jobs': soup.find('id', 'post'), # या जो भी स्पेसिफिक ID/Class हो
            'Admit Card': soup.find('id', 'admit'),
            'Result': soup.find('id', 'result')
        }
        
        # अगर आईडी से न मिले तो लिंक्स के टेक्स्ट से कैटेगरी पहचानना
        all_links = soup.find_all('a')
        
        for link in all_links:
            title_text = link.text.strip()
            href = link.get('href', '')
            
            if not title_text or len(title_text) < 5 or 'sarkariresult' not in href:
                continue
                
            # तय करना कि पोस्ट किस कैटेगरी (Label) की है
            label = "Latest Jobs"
            if "admit" in href.lower() or "admit" in title_text.lower():
                label = "Admit Card"
            elif "result" in href.lower() or "result" in title_text.lower():
                label = "Result"
            elif "admission" in href.lower():
                label = "Admission"

            # अगर यह टाइटल पहले से वेबसाइट पर नहीं है, तभी पोस्ट करे
            if title_text.lower() not in existing_titles:
                # यहाँ कन्टेंट का फॉर्मेट तैयार करना (आपकी डिटेल्स और लिंक्स के साथ)
                post_content = f"""
                <p><strong>{title_text}</strong></p>
                <p>सरकारी रिजल्ट की नई अपडेट आ चुकी है। पूरी जानकारी और टेबल देखने के लिए नीचे दिए गए लिंक पर जाएं:</p>
                <br>
                <div style="text-align: center;">
                    <a href="{href}" style="background-color: #008CBA; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Click Here for Full Details & Table</a>
                </div>
                <br>
                <p>हमारे WhatsApp Group और YouTube Channel (KP JOB UPDATE) से जुड़ना न भूलें।</p>
                """
                
                post_to_blogger(title_text, post_content, [label])
                print(f"Successfully added new post: {title_text}")
            else:
                print(f"Already exists, skipping: {title_text}")
                
    except Exception as e:
        print(f"Error scraping website: {e}")

if __name__ == "__main__":
    scrape_sarkari_result()
