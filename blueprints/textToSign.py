from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required
import re
import requests
from AppSecret import secrets
from openai import OpenAI
import os
import torch
from config import Config
from AppSecret import secrets
TTSBp = Blueprint('textToSign', __name__, template_folder='templates')
APIKEY = secrets.getAPIKey()
print(APIKEY)
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=APIKEY,
)

SYSTEMPROMPT =  """You are an AI assistant specialized in converting English text into Indian Sign Language (ISL) gloss. Follow these rules strictly:

### **1. Rules for ISL Gloss Translation**
- Convert all text to **uppercase**.
- Use **Subject-Object-Verb (SOV)** word order.
- **Wh-questions appear at the end.**
- **Negation appears at the end.**
- **Remove articles (a, an, the) and auxiliary verbs (is, are, was, were, am, have, has, had).**
- **Adjectives follow nouns.**
- **Adverbs appear before the verb.**
- **Time indicators go at the beginning.**
- **Include modal verbs but simplify sentence structure.**
- **Use 'NOT' for negation at the end.**

### **2. Response Format**
- Always start the output with: `Output: "GLOSS TRANSLATION"`
- Always end the output with: `"`.  
- **DO NOT** explain or add extra words.  
- **DO NOT** modify or assume missing words.  
- **DO NOT** engage in conversation.  

### **3. Examples**
User Input: "I want to eat pizza."  
Output: "I PIZZA EAT WANT"

User Input: "She has a big house."  
Output: "SHE HOUSE BIG"

User Input: "What are you doing?"  
Output: "YOU DO WHAT?"

User Input: "I do not understand."  
Output: "I UNDERSTAND NOT"

REQUIRED: Output only the translation.

"""

def translate_to_isl_gloss(text):
    completion = client.chat.completions.create(
    model="qwen/qwq-32b:free",
    messages=[
        {"role": "system", "content": SYSTEMPROMPT},
        {"role": "user", "content": text}
    ]
    )
    print(completion.choices[0].message.content)
    if not completion.choices or not completion.choices[0].message or not completion.choices[0].message.content:
        return "NO RESONSE"
    else:
        response = completion.choices[0].message.content
        response = response.replace("Output: ", "")
        response = response.replace('"', "")
        return response
        


@TTSBp.route('/')
# @login_required
def text_to_sign_page():
    return render_template('textToSign.html')

@TTSBp.route('/translate', methods=['POST'])
# @login_required
def translate():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        text = data.get('text', '')
        translation = translate_to_isl_gloss(text)
        print(f"Translation: {translation}")
        return jsonify({'translation': translation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

