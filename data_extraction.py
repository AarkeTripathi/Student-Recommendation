import requests

def fetch_data(quiz_url):
    quiz_response = requests.get(quiz_url)
    if quiz_response.status_code == 200:
        quiz_data = quiz_response.json()
        return quiz_data
    else:
        raise Exception("Error fetching data from API endpoints")
    

def extract_data(quiz_data):
    extracted_quiz_data = {
        'quiz_id': quiz_data['quiz_id'],
        'score': quiz_data['score'],
        'accuracy': float(quiz_data['accuracy'].strip('%')) / 100,
        'negative_score': float(quiz_data['negative_score']),
        'correct_answers': quiz_data['correct_answers'],
        'incorrect_answers': quiz_data['incorrect_answers'],
        'response_map': quiz_data['response_map'],
        'topic': quiz_data['quiz']['topic']
    }
    return extracted_quiz_data