# DescriBot

## Overview
This application integrates asynchronous tasks to enhance product descriptions as AI-powered agent. It fetches product data from an external ecommerce API, and leveraging a LLM evaluate and score the product descriptions and provide improvements suggestions also allows users to submit feedback on product descriptions. Negative feedback triggers an asynchronous process to regenerate the product description using OpenAI's language models.

## Features
- **Product Fetching**: Asynchronously fetches products from an external API and caches them for quick access.
- **Feedback Submission**: Provides an endpoint to submit user feedback on product descriptions.
- **Description Regeneration**: Uses AI to regenerate product descriptions based on user feedback.
- **Description Evaluation**: Utilizes an AI agent to evaluate and suggest improvements to product descriptions.
- **Asynchronous Processing**: Handles potentially long-running AI interactions asynchronously to maintain responsiveness.

## Technologies Used
- **Flask**: For the web server and to handle HTTP requests.
- **aiohttp**: For asynchronous HTTP requests to external APIs.
- **OpenAI's Language Models**: For generating and improving text via AI.
- **SSL**: For secure HTTP requests to external services.
- **Threading**: To manage asynchronous tasks within the Flask application.

## Setup and Installation

```bash
# Clone the repository:
git clone <repository-url>
```
## Install dependencies:
```bash
pip3 install -r requirements.txt
```
## Start the Flask server:

```bash
python3 app.py
```
This command runs the Flask app, which is configured to start an asynchronous loop for handling AI tasks.


## Submitting Feedback via curl command:
```bash
curl -X POST http://localhost:5000/submit_feedback \
-H "Content-Type: application/json" \
-d '{"product_id": "PRD_1", "rating": 2, "user_feedback": "Poor description. Needs improvement."}'
```
This endpoint accepts JSON data containing the product ID, user rating, and feedback text. If the rating indicates dissatisfaction (e.g., a rating less than 3), the application will asynchronously regenerate the product description.


