import aiohttp
import random
import html
import asyncio

# Predefined fallback questions in case the API fails
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

    """
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                if data.get('response_code') != 0:
                    raise Exception("API returned non-zero response code")
                question_data = data['results'][0]
                
                # question and answers
                question = html.unescape(question_data.get('question', ''))
                correct_answer = html.unescape(question_data.get('correct_answer', ''))
                incorrect_answers = [html.unescape(ans) for ans in question_data.get('incorrect_answers', [])]
                
                # Combine and shuffle 
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
        # return a random fallback question
        return random.choice(fallback_questions)

# Test the module 
if __name__ == "__main__":
    trivia_question = asyncio.run(get_trivia_question_async())
    if trivia_question:
        print("Question:", trivia_question['question'])
        print("Choices:")
        for idx, choice in enumerate(trivia_question['choices']):
            print(f"{idx+1}. {choice}")
        print("Correct answer is:", trivia_question['correct_answer'])
