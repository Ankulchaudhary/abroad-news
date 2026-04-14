import os
import requests
import google.generativeai as genai
from datetime import datetime

# 1. API Keys (GitHub Secrets se automatic aayengi)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_news():
    # Category ko 'general' rakha hai taki news pakka mile
    url = f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        articles = data.get('articles', [])
        # Sirf wahi articles lein jinme title aur description dono ho
        valid_articles = [a for a in articles if a.get('title') and a.get('description')]
        return valid_articles[:3] # Top 3 news
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def analyze_news(title, desc):
    prompt = f"""
    Tum ek expert news analyst ho. Is news ko analyze karo:
    Title: {title}
    Description: {desc}
    
    Format (Strictly follow this):
    HEADLINE: [Hindi Headline]
    SUMMARY: [Short Hindi Summary]
    INSIGHT: [Hindi Analysis in 1 line]
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None

def update_html(news_list):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Abroad News - AI Portal</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50 text-gray-900">
        <header class="bg-indigo-700 text-white shadow-lg p-6 text-center">
            <h1 class="text-3xl font-extrabold uppercase tracking-widest">Abroad News</h1>
            <p class="text-sm opacity-90 mt-2">AI Powered News Update | {now} (IST)</p>
        </header>
        <main class="container mx-auto p-4 max-w-4xl space-y-6">
    """
    
    for news in news_list:
        if not news: continue
        lines = [l.strip() for l in news.split('\n') if l.strip()]
        
        # Default values agar parsing mein dikat ho
        h, s, i = "Breaking News", "Khabar jald update hogi.", "AI analysis process ho raha hai."
        
        for line in lines:
            if "HEADLINE:" in line: h = line.replace("HEADLINE:", "").strip()
            elif "SUMMARY:" in line: s = line.replace("SUMMARY:", "").strip()
            elif "INSIGHT:" in line: i = line.replace("INSIGHT:", "").strip()

        html_content += f"""
            <article class="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 hover:shadow-lg transition-shadow">
                <h2 class="text-xl font-bold text-indigo-900 mb-3">{h}</h2>
                <p class="text-gray-700 leading-relaxed mb-4 font-medium">{s}</p>
                <div class="bg-indigo-50 p-4 rounded-xl text-indigo-800 text-sm border-l-4 border-indigo-700">
                    <strong>💡 AI Insight:</strong> {i}
                </div>
            </article>
        """
    
    html_content += """
        </main>
        <footer class="text-center p-10 text-gray-500 text-xs">
            &copy; 2026 Abroad News - AI Automation Successful
        </footer>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

# Main Execution
print("Checking for news...")
raw_articles = get_news()

if not raw_articles:
    print("No news found! Check your NEWS_API_KEY or NewsAPI limits.")
else:
    print(f"Found {len(raw_articles)} articles. Analyzing with Gemini...")
    processed_news = []
    for art in raw_articles:
        analysis = analyze_news(art['title'], art['description'])
        if analysis:
            processed_news.append(analysis)
    
    if processed_news:
        update_html(processed_news)
        print("Success: Website updated!")
    else:
        print("Error: Gemini could not analyze news.")
        
