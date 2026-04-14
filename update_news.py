import os
import requests
import google.generativeai as genai
from datetime import datetime

# 1. API Keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)

def get_news():
    # Global English news
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])
        return [a for a in articles if a.get('title') and a.get('description')][:3]
    except:
        return []

def analyze_with_gemini(title, desc):
    # HUM MODEL NAME NAHI LIKHENGE, SEEDHA LATEST MODEL DHONDENGE
    try:
        # Sabse basic model name jo har jagah chalta hai
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
        prompt = f"Analyze this news in Hindi. Format: HEADLINE: [Title], SUMMARY: [News], INSIGHT: [Analysis]. News: {title} - {desc}"
        response = model.generate_content(prompt)
        return response.text
    except:
        try:
            # Agar flash fail hua toh pro
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Sab models fail ho gaye: {e}")
            return None

def update_html(news_list):
    now = datetime.now().strftime('%d %b %Y | %I:%M %p')
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Abroad News</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-100">
        <header class="bg-indigo-900 text-white p-6 text-center shadow-lg">
            <h1 class="text-3xl font-bold uppercase">ABROAD NEWS</h1>
            <p class="text-xs opacity-70 mt-2">AI Update: {now}</p>
        </header>
        <main class="container mx-auto p-4 max-w-2xl space-y-6 mt-4">
    """
    for news in news_list:
        if not news: continue
        lines = [l.strip() for l in news.split('\n') if l.strip()]
        h, s, i = "Breaking News", "Update...", "Analysis..."
        for line in lines:
            if "HEADLINE:" in line: h = line.replace("HEADLINE:", "")
            if "SUMMARY:" in line: s = line.replace("SUMMARY:", "")
            if "INSIGHT:" in line: i = line.replace("INSIGHT:", "")
        
        html_content += f"""
            <div class="bg-white p-6 rounded-2xl shadow-sm border-l-8 border-indigo-600">
                <h2 class="text-xl font-bold mb-2 text-gray-800">{h}</h2>
                <p class="text-gray-600 mb-4 font-medium">{s}</p>
                <p class="text-sm italic text-indigo-700 bg-indigo-50 p-2 rounded">Insight: {i}</p>
            </div>
        """
    html_content += """
        </main>
        <footer class="text-center p-8 text-gray-400 text-xs">
            &copy; 2026 Abroad News | AI Automation Done
        </footer>
    </body></html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

# FINAL EXECUTION
news_data = get_news()
if news_data:
    print(f"{len(news_data)} news mili hain. Gemini ko bhej raha hoon...")
    final_list = []
    for art in news_data:
        res = analyze_with_gemini(art['title'], art['description'])
        if res:
            final_list.append(res)
    
    if final_list:
        update_html(final_list)
        print("SUCCESS: Website updated!")
    else:
        print("GEMINI ERROR: Kuch bhi analyze nahi ho paya.")
        
