import os
import requests
import google.generativeai as genai
from datetime import datetime

# 1. API Keys (GitHub Secrets se uthayi jayengi)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_news():
    # Sabse broad URL taki "No news found" ka khatra khatam ho jaye
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('status') != 'ok':
            print(f"API Error: {data.get('message')}")
            return []
            
        articles = data.get('articles', [])
        # Sirf wahi news lein jinme Title aur Description ho
        return [a for a in articles if a.get('title') and a.get('description')][:3]
    except Exception as e:
        print(f"Network Error: {e}")
        return []

def analyze_news(title, desc):
    prompt = f"""
    Tum ek expert news analyst ho. Is news ko analyze karke Hindi mein likho:
    Title: {title}
    Description: {desc}
    
    Format:
    HEADLINE: [Dumdaar Hindi Headline]
    SUMMARY: [2-3 lines mein news ka saar]
    INSIGHT: [Iska asar kya hoga - 1 line analysis]
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return None

def update_html(news_list):
    now = datetime.now().strftime('%d %b %Y | %I:%M %p')
    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Abroad News - Global Updates</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 text-slate-900">
        <header class="bg-gradient-to-r from-blue-700 to-indigo-800 text-white shadow-xl p-8 text-center">
            <h1 class="text-4xl font-black uppercase tracking-tighter">Abroad News</h1>
            <p class="text-sm opacity-90 mt-2 font-mono">AI AUTO-UPDATE: {now}</p>
        </header>
        <main class="container mx-auto p-4 max-w-3xl space-y-8 mt-6">
    """
    
    for news in news_list:
        if not news: continue
        lines = [l.strip() for l in news.split('\n') if l.strip()]
        
        h, s, i = "Breaking Update", "Processing news...", "AI analysis in progress."
        for line in lines:
            if "HEADLINE:" in line: h = line.replace("HEADLINE:", "").strip()
            elif "SUMMARY:" in line: s = line.replace("SUMMARY:", "").strip()
            elif "INSIGHT:" in line: i = line.replace("INSIGHT:", "").strip()

        html_content += f"""
            <article class="bg-white p-6 rounded-3xl shadow-sm border border-slate-200 hover:border-blue-400 transition-all">
                <h2 class="text-2xl font-bold text-slate-800 mb-4 leading-tight">{h}</h2>
                <p class="text-slate-600 mb-6 leading-relaxed text-lg">{s}</p>
                <div class="bg-blue-50 p-4 rounded-2xl text-blue-900 text-sm border-l-8 border-blue-600">
                    <strong>🔍 AI Insight:</strong> {i}
                </div>
            </article>
        """
    
    html_content += """
        </main>
        <footer class="text-center p-12 text-slate-400 text-sm">
            Powered by Gemini AI | Updated via GitHub Actions
        </footer>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

# Main Execution
print("Khabrein dhoond raha hoon...")
news_data = get_news()

if not news_data:
    print("Error: Koi news nahi mili! Pakka karein ki NEWS_API_KEY sahi hai.")
else:
    print(f"{len(news_data)} khabrein mili hain. Gemini analyze kar raha hai...")
    final_list = []
    for art in news_data:
        res = analyze_news(art['title'], art['description'])
        if res: final_list.append(res)
    
    if final_list:
        update_html(final_list)
        print("Success: Website update ho gayi!")
    else:
        print("Gemini response khali hai.")
        
