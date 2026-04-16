# 🌍 AbroadNews - AI Powered Global News Portal

**AbroadNews** ek fully automated news portal hai jo Google Gemini AI aur GitHub Actions ka use karke har 4 ghante mein duniya bhar ki badi khabrein fetch karta hai, unka analysis karta hai, aur unhe Hindi mein translate karke website par update kar deta hai.

## 🚀 Features

-   **Auto-Update:** GitHub Actions ki madad se har 4 ghante mein automatically update hota hai.
-   **AI Analysis:** Google Gemini 2.0 Flash model ka use karke news ka deep insight generate karta hai.
-   **Hindi Translation:** Global news ko asaan aur dumdaar Hindi headlines aur summaries mein badalta hai.
-   **Responsive Design:** Tailwind CSS ka use karke ek modern aur clean UI banaya gaya hai.
-   **Zero Maintenance:** Ek baar setup hone ke baad, bina kisi manual effort ke chalta rehta hai.

## 🛠️ Tech Stack

-   **Language:** Python 3.10
-   **AI Model:** Google Gemini 2.0 Flash (Latest Gen AI SDK)
-   **News Source:** NewsAPI.org
-   **Automation:** GitHub Actions
-   **Frontend:** HTML5, Tailwind CSS

## ⚙️ How It Works

1.  **Trigger:** GitHub Actions har 4 ghante mein (Cron Job) ya manual trigger par workflow start karta hai.
2.  **Fetch:** Python script NewsAPI se latest global headlines uthati hai.
3.  **Process:** Google Gemini AI un headlines ko padhta hai aur unka Hindi analysis taiyar karta hai.
4.  **Build:** Script automatically `index.html` file ko naye content ke saath overwrite kar deti hai.
5.  **Deploy:** GitHub Actions naye badlavon ko repository mein push karta hai aur GitHub Pages par site live ho jati hai.

## 📂 Folder Structure

-   `.github/workflows/main.yml`: Automation ka dimaag (Workflow configuration).
-   `update_news.py`: Python script jo AI aur News API ko handle karti hai.
-   `index.html`: Aapka live news dashboard.

---
*Created with ❤️ by Ankul Chaudhary using Gemini AI.*

