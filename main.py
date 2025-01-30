from fastapi import FastAPI, Form
import uvicorn
import pandas as pd
import json
from recommendation_analysis import analyze_performance, define_student_persona, generate_recommendations, visualize_insights
from data_extraction import fetch_data, extract_data

# CURRENT_QUIZ_DATA_URL = "https://api.jsonserve.com/rJvd7g"
HISTORICAL_QUIZ_DATA_URL = "https://api.jsonserve.com/XgAgFJ"

app = FastAPI()

@app.post("/recommendation")
async def get_recommendations(
    quiz_id: int = Form(...),
    topic: str = Form(...),
    score: int = Form(...),
    accuracy: float = Form(..., ge=0.0, le=1.0),
    negative_score: float = Form(...),
    correct_answers: int = Form(...),
    incorrect_answers: int = Form(...),
    response_map: str = Form(...), 
):
    historical_quiz_data = fetch_data(HISTORICAL_QUIZ_DATA_URL)

    extracted_data_list=[]
    for quiz_data in historical_quiz_data:
        extracted_data_list.append(extract_data(quiz_data))

    historical_df= pd.DataFrame(extracted_data_list)

    response_map_dict = json.loads(response_map)
    current_df = pd.DataFrame([{  
        'quiz_id': quiz_id,
        'score': score,
        'accuracy': accuracy,
        'negative_score': negative_score,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'response_map': json.dumps(response_map_dict),
        'topic': topic
    }])

    combined_df = pd.concat([historical_df, current_df], ignore_index=True)

    weak_topics, improvement_trends, performance_gap = analyze_performance(combined_df)

    student_persona = define_student_persona(combined_df)

    recommendations = generate_recommendations(weak_topics, performance_gap, topic)

    weak_topics_image, improvement_trends_image, performance_gap_image = visualize_insights(weak_topics, improvement_trends, performance_gap)

    response = {
        "student_persona": student_persona,
        "recommendations": recommendations,
        "plots": {
            "weak_topics": weak_topics_image,
            "improvement_trends": improvement_trends_image,
            "performance_gaps": performance_gap_image
        }
    }
    return response


if __name__=='__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)