from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import json
import pandas as pd
import requests
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import re
from dotenv import load_dotenv
import os
API_KEY_AI = os.getenv("API_KEY_AI")
API_KEY_GOOGLE = os.getenv("API_KEY_GOOGLE")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
# === Set up Flask app ===
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# === Load system instructions ===
with open(r'system_instruction.txt', 'r', encoding='utf-8') as file:
    system_instructions = file.read().strip()
with open(r'user_message.txt', 'r', encoding='utf-8') as file_u:
    user_message = file_u.read().strip()
# === Set up OpenAI client ===
client = openai.OpenAI(api_key=API_KEY_AI)  # Don’t hardcode in real apps
@app.route("/")
def index():
    return send_from_directory('static', 'main.html')

def chat(job_description):
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": job_description}
        ],
        temperature=0
    )
    response_text = response.choices[0].message.content.strip()
    return response_text

@app.route('/api/find-candidates', methods=['POST'])
def find_candidates():
    data = request.get_json()
    job_description = data['job_description']
    data_2 = []
    # Your AI processing logic here
    candidates_df_link = chat(job_description)

    # time.sleep(2)  # Wait for results to load
    API_KEY = API_KEY_GOOGLE
    SEARCH_ENGINE_ID = SEARCH_ENGINE_ID
    query = candidates_df_link

    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query
    }

    response = requests.get(url, params=params)

    results = response.json()
    with open('data.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)

    data = [
        {
            'name': 'Alice Kumar',
            'current_role': 'Data Engineer',
            'experience': '5 years',
            'location': 'Bangalore, India',
            'education': 'BTech Computer Science',
            'email': 'alice.kumar@example.com',
            'phone': '+91-9876543210',
            'skills': ['Python', 'Snowflake', 'ETL', 'SQL', 'AWS'],
            'match_score': 94
        },
        {
            'name': 'Bob Singh',
            'current_role': 'Data Analytics Engineer',
            'experience': '3 years',
            'location': 'Hyderabad, India',
            'education': 'MSc Data Science',
            'email': 'bob.singh@example.com',
            'phone': '+91-9988776655',
            'skills': ['SQL', 'Azure', 'Data Pipeline', 'ETL'],
            'match_score': 88
        },
        {
            'name': 'Catherine Lee',
            'current_role': 'ML Engineer',
            'experience': '4 years',
            'location': 'Delhi, India',
            'education': 'BSc Mathematics',
            'email': 'catherine.lee@example.com',
            'phone': '+91-9123456789',
            'skills': ['TensorFlow', 'Python', 'GCP', 'Machine Learning'],
            'match_score': 92
        }
    ]
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
    maindata=data['items']
    for item in maindata:
        text=item['pagemap']['metatags'][0]['og:description']
        first_line = text.split('\n\n')[0]

        # Use regex to find skill keywords typically separated by commas or pipes
        skills_pattern = r'[A-Za-z0-9\-#\(\)\/]+(?:, [A-Za-z0-9\-#\(\)\/ ]+)*'
        skills_list = re.findall(skills_pattern, first_line)

        # Clean skills list, split by comma and pipe
        skills_raw = first_line.split('|')
        skills_clean = []
        for part in skills_raw:
            part = part.strip()
            if part:
                for skill in part.split(','):
                    skill = skill.strip()
                    real_checck=skill.split(' ')
                    if skill and skill.lower() not in skills_clean and len(real_checck)<4:
                        skills_clean.append(skill)
        experience_description = '\n\n'.join(text.split('\n\n')[1:]).strip()
        curr_role=item['pagemap']['metatags'][0]["og:title"].split('|')[0].split('-')[1]
        parts = [part.strip() for part in text.split('\u00b7') if part.strip()]

        # Initialize empty strings
        experience = ''
        education = ''

        # Loop through parts to find Experience and Education
        for part in parts:
            if part.lower().startswith('experience:'):
                experience = part[len('experience:'):].strip()
            elif part.lower().startswith('education:'):
                education = part[len('education:'):].strip()

        dta={
            'name': item['pagemap']['metatags'][0]["profile:first_name"],
            'email': item['pagemap']['metatags'][0]["al:ios:url"],
            'skills': skills_clean,
            'experience': experience_description,
            'current_role': curr_role,
            'education': education,
            'curr_company':experience
        }
        data_2.append(dta)

    
    df = pd.DataFrame(data_2)
    print(df)

    # Convert DataFrame to JSON
    candidates_json = df.to_dict('records')
    
    return jsonify({"candidates": candidates_json})

# === Start the app ===
if __name__ == "__main__":
    app.run(debug=True)