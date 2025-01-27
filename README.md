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
