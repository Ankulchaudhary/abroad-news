import os
import requests
import google.generativeai as genai
from datetime import datetime

# 1. API Keys (GitHub Secrets se automatic aayengi)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Setup - 'gemini-pro' use kar rahe hain stable connection ke liye
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def get_news():
    # Global English news fetch kar rahe hain taki results pakka milein
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=10&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('status') != 'ok':
            print(f"News API Error: {data.get('message')}")
            return []
            
        articles = data.get('articles', [])
        # Sirf wo news jinme Title aur Description dono ho
        valid_news = [a for a in articles if a.get('title') and a.get('description')]
        return valid_news[:3] 
    except Exception as e:
        print(f"Fetching Error: {e}")
        return []

def analyze_news(title, desc):
    prompt = f"""
    Tum ek expert news analyst ho. Is news ko Hindi mein analyze karo:
    Title: {title}
    Description: {desc}
    
    Format:
    HEADLINE: [Hindi Headline]
    SUMMARY: [Short Hindi Summary]
    INSIGHT: [1 Line Future Analysis in Hindi]
    """
    try:
        response = model.generate_content(prompt)
        # Check if response has text
        if response and response.text:
            return response.text
        return None
    except Exception as e:
        print(f"Gemini Analysis Error: {e}")
        return None

def update_html(news_list):
    # IST Time format
    now = datetime.now().strftime('%d %b %Y | %I:%M %p')
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Abroad News - AI Portal</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Noto Sans Devanagari', sans-serif; }}</style>
    </head>
    <body class="bg-gray-100">
        <header class="bg-indigo-900 text-white p-8 text-center shadow-2xl">
            <h1 class="text-4xl font-bold tracking-tight">ABROAD NEWS</h1>
            <p class="text-indigo-200 mt-2 font-mono text-sm underline">LAST UPDATED: {now}</p>
        </header>
        <main class="container mx-auto p-6 max-w-3xl space-y-8">
    """
    
    for news in news_list:
        lines = [l.strip() for l in news.split('\n') if l.strip()]
        h, s, i = "Breaking News", "Update ho raha hai...", "Analysis pending."
        
        for line in lines:
            if "HEADLINE:" in line: h = line.replace("HEADLINE:", "").strip()
            elif "SUMMARY:" in line: s = line.replace("SUMMARY:", "").strip()
            elif "INSIGHT:" in line: i = line.replace("INSIGHT:", "").strip()

        html_content += f"""
            <article class="bg-white p-8 rounded-3xl shadow-sm border-b-4 border-indigo-500">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">{h}</h2>
                <p class="text-gray-600 mb-6 leading-relaxed text-lg">{s}</p>
                <div class="bg-indigo-50 p-4 rounded-xl text-indigo-900 text-sm italic">
                    <strong>💡 AI Insight:</strong> {i}
                </div>
            </article>
        """
    
    html_content += """
        </main>
        <footer class="text-center p-12 text-gray-400 text-sm">
            &copy; 2026 Abroad News | Powered by Google Gemini Pro
        </footer>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

# Execution
print("Khabrein dhoond raha hoon...")
raw_news = get_news()

if not raw_news:
    print("API se news nahi mili. Key check karein.")
else:
    print(f"{len(raw_news)} khabrein mili hain. Gemini analyze kar raha hai...")
    analyzed_list = []
    for article in raw_news:
        res = analyze_news(article['title'], article['description'])
        if res:
            analyzed_list.append(res)
    
    if analyzed_list:
        update_html(analyzed_list)
        print("Success: Website update ho gayi!")
    else:
        print("Error: Gemini response khali hai.")
        
