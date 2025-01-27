import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


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


def plot_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return image_base64


def visualize_insights(weak_topics, improvement_trends, performance_gap):
    weak_topics_plot = plt.figure()
    plt.bar(weak_topics.index, weak_topics['accuracy'], color='red')
    plt.title("Weak Topics")
    plt.xlabel("Topic")
    plt.ylabel("Average Accuracy")
    weak_topics_image = plot_to_base64(weak_topics_plot)

    improvement_trends_plot = plt.figure()
    plt.plot(improvement_trends.index, improvement_trends.values, marker='o')
    plt.title("Improvement Trends")
    plt.xlabel("Quiz ID")
    plt.ylabel("Average Accuracy")
    improvement_trends_image = plot_to_base64(improvement_trends_plot)

    performance_gap_plot = plt.figure()
    plt.bar(performance_gap.index, performance_gap['gap'], color='blue')
    plt.title("Performance Gaps by Topic")
    plt.xlabel("Topic")
    plt.ylabel("Accuracy Gap")
    performance_gap_image = plot_to_base64(performance_gap_plot)

    return weak_topics_image, improvement_trends_image, performance_gap_image