import os
import requests
from bs4 import BeautifulSoup

# Configuration
SOURCE_URL = "https://sarkariresult.com.cm"
BLOG_ID = "4048403200960649077"
API_KEY = "AIzaSyCxEUZ-9yT174II3jXvXN2zk-aNgUYLOBw"

def fetch_latest_jobs():
    print("Fetching jobs from source...")
    response = requests.get(SOURCE_URL)
    if response.status_code != 200:
        print("Failed to fetch source website")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = []
    # Source website se links nikalne ka basic logic
    for link in soup.find_all('a', href=True):
        if 'job' in link['href'] or 'admission' in link['href']:
            title = link.text.strip()
            url = link['href']
            if title and url:
                jobs.append({'title': title, 'url': url})
    return jobs[:5] # Top 5 latest posts

def post_to_blogger(title, content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    # Custom Footer/Links Text
    footer_html = """
    <br><br>
    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 8px; border: 1px solid #b0e0e6; font-family: Arial, sans-serif;">
        <h3 style="color: #0073e6; margin-top: 0;">📢 KP JOB UPDATE</h3>
        <p>Aise hi aur job updates aur taiyari ke liye hamare channels se judein:</p>
        <ul>
            <li><b>WhatsApp Group:</b> <a href="#">Job Update 2026</a></li>
            <li><b>YouTube Channel:</b> <a href="#">KP JOB UPDATE</a></li>
        </ul>
    </div>
    """
    
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": f"{content}{footer_html}"
    }
    
    res = requests.post(url, json=data, headers=headers)
    if res.status_code == 200:
        print(f"Successfully posted: {title}")
    else:
        print(f"Failed to post: {res.text}")

if __name__ == "__main__":
    latest_jobs = fetch_latest_jobs()
    for job in latest_jobs:
        # Har job ke liye detailed content fetch karke post karne ka logic
        job_content = f"<p>Nayi vacancy ki jankari ke liye neeche diye gaye link par click karein:</p><br><a href='{job['url']}' style='display:inline-block; background-color:#28a745; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;'>Apply / Read More</a>"
        post_to_blogger(job['title'], job_content)
