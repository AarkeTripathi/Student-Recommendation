# Student-Recommendation

This project is a **Personalized Student Recommendation System** that analyzes quiz performance to provide personalized insights and recommendations for students. The system combines historical quiz data with current quiz data to define student personas, identify weak topics, and suggest actionable steps for improvement.

## Project Structure

### 1. `main.py`
- **Purpose**: Serves as the entry point for the FastAPI application.
- **Key Features**:
  - API Endpoint: `/recommendation` (POST)
    - Accepts current quiz data via form fields.
    - Fetches historical quiz data using the `data_extraction.py` module.
    - Uses `recommendation_analysis.py` for performance analysis and insights generation.
    - Returns personalized recommendations and base64-encoded visualizations as part of the response.

### 2. `data_extraction.py`
- **Purpose**: Handles data fetching and extraction.
- **Key Functions**:
  - `fetch_data(url)`: Fetches data from the given API endpoint.
  - `extract_data(data)`: Extracts relevant quiz details from the raw data.

### 3. `recommendation_analysis.py`
- **Purpose**: Performs analysis of quiz data and generates insights.
- **Key Functions**:
  - `analyze_performance(current_df, historical_df)`: Identifies weak topics, improvement trends, and performance gaps.
  - `define_student_persona(current_df, historical_df)`: Defines the student's persona based on their performance patterns.
  - `generate_recommendations(weak_topics, performance_gap, current_topic)`: Generates tailored recommendations for the student.
  - `visualize_insights(weak_topics, improvement_trends, performance_gap)`: Creates visualizations of insights and encodes them as base64 images.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies
Ensure you have Python 3.9+ installed. Install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Just run the main.py program from any IDE. The server will run on `http://127.0.0.1:8000`.

### 4. Test the API
You can use tools like Postman or cURL to test the `/recommendation` endpoint. 
Example request:
```bash
curl -X POST "http://127.0.0.1:8000/recommendation" \
    -F "quiz_id=123" \
    -F "topic=Biology" \
    -F "score=45" \
    -F "accuracy=0.9" \
    -F "negative_score=2.0" \
    -F "correct_answers=45" \
    -F "incorrect_answers=5" \
    -F "response_map={\"101\": \"1\", \"102\": \"4\"}"
```

## Approach

### 1. Data Extraction:
- Historical quiz data is fetched from the API and processed into a structured format.

### 2. Performance Analysis:
- Current and historical data are combined to:
    - Identify weak topics (low accuracy).
    - Analyze improvement trends over time.
    - Calculate performance gaps across topics.

### 3. Recommendations:
- Personalized recommendations are generated based on identified weaknesses and inconsistent performance.
### 4. Visualization:
- Insights such as weak topics, improvement trends, and performance gaps are visualized and encoded as base64 images for embedding in responses.

## Example Response:
```json
{
  "student_persona": {
    "persona": "Moderate Performer",
    "description": "Performs reasonably well but has room for improvement in specific areas.",
    "average_accuracy": 0.75,
    "total_quizzes": 5,
    "topics_attempted": 3,
    "weak_topics": ["Physics", "Chemistry"]
  },
  "recommendations": [
    {
      "topic": "Physics",
      "recommendation": "Focus more on this topic to improve accuracy."
    },
    {
      "topic": "Chemistry",
      "recommendation": "Pay extra attention to this topic based on recent performance."
    }
  ],
  "plots": {
    "weak_topics": "<base64-encoded-image>",
    "improvement_trends": "<base64-encoded-image>",
    "performance_gaps": "<base64-encoded-image>"
  }
}
```