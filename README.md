                             🍽️ NutriChef AI – Healthy Recipes & Smart Grocery Planner
NutriChef AI is a smart web application that helps users generate recipes, plan healthier meals, and create budget‑friendly shopping lists using Artificial Intelligence.

The platform allows users to enter available ingredients and instantly receive AI‑generated recipes, health‑focused meal suggestions, and organized grocery lists.

🚀 Features
🤖 AI Recipe Generator
Generate complete recipes using AI based on the ingredients you already have.

🥗 Healthier Recipe Assistant
Get healthier alternatives and suggestions to improve your diet and nutrition.

🛒 Smart Shopping List Generator
Automatically create grocery lists based on selected recipes.

💾 Save Recipes
Users can save their favorite recipes for later use.

👤 User Authentication
Secure login and signup system for managing personal recipes.

📚 Cooking Tips & Blog
Helpful cooking tips and educational content for better cooking habits.

🛠️ Tech Stack
Backend

Python

Django

Frontend

HTML

CSS

Bootstrap

AI Integration

Groq API

Llama AI Model

Database

SQLite (default Django database)

📂 Project Structure
ai_meal_planner/
│
├── accounts/        # User authentication
├── recipes/         # Recipe generation and management
├── core/            # Main pages (home, blog, etc.)
│
├── templates/       # HTML templates
├── static/          # CSS and static files
│
├── manage.py
└── settings.py
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/nutrichef-ai.git
cd nutrichef-ai



2️⃣ Create virtual environment
python -m venv venv
Activate it:

Windows

venv\Scripts\activate
Mac/Linux

source venv/bin/activate
3️⃣ Install dependencies
pip install -r requirements.txt


4️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate


5️⃣ Run the server
python manage.py runserver
Open in browser:

http://127.0.0.1:8000/
🔑 Environment Variables
Create a .env file and add your API key:

GROQ_API_KEY=your_api_key_here
