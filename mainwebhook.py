import aiohttp
import asyncio
import random
import html
import json
import requests

# Predefined fallback questions 
fallback_questions = [
    {
        'question': 'What is the capital of France?',
        'choices': ['Berlin', 'Madrid', 'Paris', 'Rome'],
        'correct_index': 2,
        'correct_answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'choices': ['Earth', 'Mars', 'Jupiter', 'Saturn'],
        'correct_index': 1,
        'correct_answer': 'Mars'
    },
    {
        'question': 'What is the largest ocean on Earth?',
        'choices': ['Atlantic Ocean', 'Indian Ocean', 'Arctic Ocean', 'Pacific Ocean'],
        'correct_index': 3,
        'correct_answer': 'Pacific Ocean'
    }
]

async def get_trivia_question_async():
    """
    Fetch a trivia question from the Open Trivia Database API.
    
    Returns:
        dict: Contains the following keys:
            - question (str): The trivia question text.
            - choices (list): A list of answer choices (shuffled).
            - correct_index (int): The index of the correct answer in the choices list.
            - correct_answer (str): The text of the correct answer.
    """
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if data.get('response_code') != 0:
                    raise Exception("API returned non-zero response code")
                question_data = data['results'][0]
                
                # Decode HTML entities
                question = html.unescape(question_data.get('question', ''))
                correct_answer = html.unescape(question_data.get('correct_answer', ''))
                incorrect_answers = [html.unescape(ans) for ans in question_data.get('incorrect_answers', [])]
                
                # Combine and shuffle answers 
                all_answers = incorrect_answers + [correct_answer]
                random.shuffle(all_answers)
                correct_index = all_answers.index(correct_answer)
                
                return {
                    'question': question,
                    'choices': all_answers,
                    'correct_index': correct_index,
                    'correct_answer': correct_answer
                }
    except Exception as e:
        print("Error fetching trivia question from API:", e)
        # If API fails, return a random fallback question
        return random.choice(fallback_questions)

def send_trivia_to_discord(trivia, webhook_url):
    """
    Send a formatted trivia question to a Discord channel using a webhook.
    
    Args:
        trivia (dict): A dictionary containing the trivia question details with keys:
            - question (str): The trivia question text.
            - choices (list): A list of answer choices.
            - correct_index (int): The index of the correct answer in the choices list.
            - correct_answer (str): The text of the correct answer.
        webhook_url (str): The Discord webhook URL to which the message is sent.
    """
    
    message = f"**Trivia Time!**\n\n"
    message += f"**Question:** {trivia['question']}\n\n"
    message += "**Choices:**\n"
    for i, choice in enumerate(trivia['choices']):
        message += f"{i+1}. {choice}\n"
    
    
    
    data = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    # Send POST request
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    
    if response.status_code == 204:
        print("Trivia question sent successfully!")
    else:
        print(f"Failed to send trivia question. HTTP {response.status_code}: {response.text}")

if __name__ == "__main__":
    WEBHOOK_URL = "https://discord.com/api/webhooks/1339672836087873606/mWa4yzPn4uCrbZkpXV5rCNxKuniGJI6K1YgeWulq9hJoeH_2DdURdub_XmbiYls3JK0K"
    
    trivia_question = asyncio.run(get_trivia_question_async())
    send_trivia_to_discord(trivia_question, WEBHOOK_URL)
