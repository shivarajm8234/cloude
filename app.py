from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Mental health support prompts and resources
RESPONSES = {
    'negative': [
        "I hear that you're going through a difficult time. Your feelings are valid.",
        "It's okay to feel this way. Would you like to explore some coping strategies together?",
        "I'm here to support you. Would you like to talk more about what's troubling you?",
        "Remember that seeking help is a sign of strength. Would you like some information about professional resources?"
    ],
    'neutral': [
        "I'm here to listen. Would you like to share more about your experience?",
        "Your feelings matter. How can I support you today?",
        "Sometimes talking things through can help. What's on your mind?",
        "I'm interested in understanding your perspective better. Would you like to elaborate?"
    ],
    'positive': [
        "It's wonderful that you're feeling positive! How can we build on this momentum?",
        "I'm glad you're feeling this way. What has been helping you?",
        "Your resilience is inspiring. Would you like to share what strategies have been working for you?",
        "It's great to hear that! Remember these positive moments during challenging times."
    ],
    'crisis': [
        "I'm very concerned about what you're sharing. Your life matters.",
        "You don't have to go through this alone. Here are some immediate support resources:",
        "National Suicide Prevention Lifeline: 988 (24/7)",
        "Crisis Text Line: Text HOME to 741741",
        "Would you like help connecting with a mental health professional?"
    ]
}

def simple_sentiment_analysis(text):
    """Simple keyword-based sentiment analysis"""
    negative_words = ['sad', 'depressed', 'anxious', 'worried', 'angry', 'hurt', 'pain', 'lonely', 'hopeless']
    positive_words = ['happy', 'good', 'great', 'wonderful', 'excited', 'joy', 'love', 'peaceful', 'hopeful']
    crisis_words = ['suicide', 'kill', 'die', 'end it', 'no reason', 'worthless']
    
    text = text.lower()
    
    # Check for crisis keywords first
    if any(word in text for word in crisis_words):
        return 'crisis'
    
    # Count sentiment words
    negative_count = sum(1 for word in negative_words if word in text)
    positive_count = sum(1 for word in positive_words if word in text)
    
    # Determine sentiment
    if negative_count > positive_count:
        return 'negative'
    elif positive_count > negative_count:
        return 'positive'
    else:
        return 'neutral'

def get_response(sentiment):
    """Get a random response based on sentiment"""
    return random.choice(RESPONSES[sentiment])

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat interactions"""
    user_message = request.json.get('message', '')
    
    # Analyze sentiment and get appropriate response
    sentiment = simple_sentiment_analysis(user_message)
    response = get_response(sentiment)
    
    return jsonify({
        'message': response,
        'sentiment': sentiment
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
