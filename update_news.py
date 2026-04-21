from google import genai
import os

# Get the API key from GitHub Secrets
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY is missing.")
    exit(1)

# Initialize the NEW client
client = genai.Client(api_key=api_key)

def generate_news_summary():
    try:
        # Using the simplified call for the latest library
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Provide a summary of the top 5 international news stories for today in a professional format."
        )
        
        # Save the result
        with open("latest_news.md", "w", encoding="utf-8") as f:
            f.write("# Daily Abroad News Update\n\n")
            f.write(response.text)
            
        print("Success: News file created!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_news_summary()
    
