import requests
import json
import pandas as pd
import matplotlib.pyplot as plt


CURRENT_QUIZ_DATA_URL = "https://api.jsonserve.com/rJvd7g"
HISTORICAL_QUIZ_DATA_URL = "https://api.jsonserve.com/XgAgFJ"


def fetch_data(current_quiz_url, historical_quiz_url):
    current_quiz_response = requests.get(current_quiz_url)
    historical_quiz_response = requests.get(historical_quiz_url)

    if current_quiz_response.status_code == 200 and historical_quiz_response.status_code == 200:
        current_quiz_data = current_quiz_response.json()
        historical_quiz_data = historical_quiz_response.json()
        return current_quiz_data, historical_quiz_data
    else:
        raise Exception("Error fetching data from API endpoints")


def preprocess_data(current_quiz, historical_quiz):
    current_data = {
        'quiz_id': current_quiz['quiz_id'],
        'score': current_quiz['score'],
        'accuracy': float(current_quiz['accuracy'].strip('%')) / 100,
        'negative_score': float(current_quiz['negative_score']),
        'correct_answers': current_quiz['correct_answers'],
        'incorrect_answers': current_quiz['incorrect_answers'],
        'response_map': current_quiz['response_map'],
        'topic': current_quiz['quiz']['topic']
    }
    current_df = pd.DataFrame([current_data])

    historical_data = []
    for quiz in historical_quiz:
        historical_data.append({
            'quiz_id': quiz['quiz_id'],
            'score': quiz['score'],
            'accuracy': float(quiz['accuracy'].strip('%')) / 100,
            'negative_score': float(quiz['negative_score']),
            'correct_answers': quiz['correct_answers'],
            'incorrect_answers': quiz['incorrect_answers'],
            'response_map': quiz['response_map'],
            'topic': quiz['quiz']['topic']
        })
    historical_df = pd.DataFrame(historical_data)

    return current_df, historical_df


def analyze_performance(current_df, historical_df):
    combined_df = pd.concat([historical_df, current_df], ignore_index=True)

    numeric_columns = combined_df.select_dtypes(include=["number"])
    topic_performance = combined_df.groupby("topic")[numeric_columns.columns].mean()

    weak_topics = topic_performance[topic_performance["accuracy"] < 0.5]

    improvement_trends = combined_df.groupby("quiz_id")["accuracy"].mean()

    performance_gap = combined_df.groupby("topic")["accuracy"].agg(['max', 'min'])
    performance_gap["gap"] = performance_gap["max"] - performance_gap["min"]

    return weak_topics, improvement_trends, performance_gap


def define_student_persona(current_df, historical_df):
    combined_df = pd.concat([historical_df, current_df], ignore_index=True)

    average_accuracy = combined_df["accuracy"].mean()
    total_quizzes = len(combined_df)
    topics_attempted = combined_df["topic"].nunique()
    weak_topics = combined_df.groupby("topic")["accuracy"].mean().where(lambda x: x < 0.5).dropna().index.tolist()

    if average_accuracy > 0.8:
        persona = "High Performer"
        description = "Consistently performs well across topics with minimal weak areas."
    elif 0.5 <= average_accuracy <= 0.8:
        persona = "Moderate Performer"
        description = "Performs reasonably well but has room for improvement in specific areas."
    else:
        persona = "Struggler"
        description = "Faces significant challenges across topics and needs focused improvement."

    return {
        "persona": persona,
        "description": description,
        "average_accuracy": average_accuracy,
        "total_quizzes": total_quizzes,
        "topics_attempted": topics_attempted,
        "weak_topics": weak_topics
    }


def generate_recommendations(weak_topics, performance_gap, current_topic):
    recommendations = []

    for topic in weak_topics.index:
        recommendations.append({
            "topic": topic,
            "recommendation": "Focus more on this topic to improve accuracy."
        })

    if current_topic in weak_topics.index:
        recommendations.append({
            "topic": current_topic,
            "recommendation": "Pay extra attention to this topic based on recent performance."
        })

    for topic, row in performance_gap.iterrows():
        if row["gap"] > 0.3:  
            recommendations.append({
                "topic": topic,
                "recommendation": f"Your performance in {topic} is inconsistent. Try focusing on steady improvement."
            })

    return recommendations


def visualize_insights(weak_topics, improvement_trends, performance_gap):
    plt.figure(figsize=(10, 5))
    plt.bar(weak_topics.index, weak_topics['accuracy'], color='red')
    plt.title("Weak Topics")
    plt.xlabel("Topic")
    plt.ylabel("Average Accuracy")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(improvement_trends.index, improvement_trends.values, marker='o')
    plt.title("Improvement Trends")
    plt.xlabel("Quiz ID")
    plt.ylabel("Average Accuracy")
    plt.grid()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.bar(performance_gap.index, performance_gap['gap'], color='blue')
    plt.title("Performance Gaps by Topic")
    plt.xlabel("Topic")
    plt.ylabel("Accuracy Gap")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def recommend(current_quiz_url, historical_quiz_url):
    current_quiz_data, historical_quiz_data = fetch_data(current_quiz_url, historical_quiz_url)
    current_df, historical_df = preprocess_data(current_quiz_data, historical_quiz_data)

    weak_topics, improvement_trends, performance_gap = analyze_performance(current_df, historical_df)

    student_persona = define_student_persona(current_df, historical_df)

    recommendations = generate_recommendations(weak_topics, performance_gap, current_df.iloc[0]['topic'])

    visualize_insights(weak_topics, improvement_trends, performance_gap)

    print("\nStudent Persona:")
    print(f"- Persona: {student_persona['persona']}")
    print(f"- Description: {student_persona['description']}")
    print(f"- Average Accuracy: {student_persona['average_accuracy']:.2f}")
    print(f"- Total Quizzes Attempted: {student_persona['total_quizzes']}")
    print(f"- Topics Attempted: {student_persona['topics_attempted']}")
    print(f"- Weak Topics: {', '.join(student_persona['weak_topics']) if student_persona['weak_topics'] else 'None'}")

    print("\nPersonalized Recommendations:")
    for rec in recommendations:
        print(f"- {rec['recommendation']} (Topic: {rec['topic']})")



recommend(CURRENT_QUIZ_DATA_URL, HISTORICAL_QUIZ_DATA_URL)
