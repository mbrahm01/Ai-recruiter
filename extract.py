import re
import json
with open('data.json', 'r') as json_file:
    data = json.load(json_file)
text = """AI/ML Engineer | Data Scientist | Python, TensorFlow, LLMs, RAG | Specialized in NLP, Computer Vision, Generative AI, | I Help Companies leveraging AI to Drive Innovation and Transform Complex Data into Intelligence · AI/ML Engineer | Data Scientist | Generative AI Specialist | MLOps Specialist

I’m an AI/ML Engineer with 4+ years of experience solving real-world problems across telecom, healthcare, insurance, and legal tech domains. I specialize in LLMs, RAG systems, NLP, computer vision, and MLOps, turning complex datasets into actionable intelligence at scale.

I’ve built and deployed production-ready solutions including:

NLP-based chatbots and document intelligence platforms
Time-series anomaly detection for network optimization
Predictive maintenance systems using ARIMA, LSTMs, and GBTs
LLM-powered assistants (GPT, LLaMA, Falcon) with RAG pipelines

I work with cross-functional teams to translate ideas into scalable systems using tools like Python, PyTorch, TensorFlow, MLflow, Docker, Kubernetes, a"""

# Extract skills from the first line (before the first paragraph break)
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
                if skill and skill.lower() not in skills_clean:
                    skills_clean.append(skill)

    # Extract experience description after skills (everything excluding first line)
    experience_description = '\n\n'.join(text.split('\n\n')[1:]).strip()

    print("Skills:")
    print(skills_clean)
    print("\nExperience Description:")
    print(experience_description)
