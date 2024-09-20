# Web-Scraping-AI-Bot

Unlock insights from the world’s most trusted news source with our **Web-Scraping-AI-Bot**! This project leverages cutting-edge technologies to extract, summarize, and analyze the latest articles from BBC News, providing you with concise insights and sentiment analysis at your fingertips.

## 🚀 Features

- **Automated Article Scraping**: Efficiently fetches the latest news articles directly from BBC's website using Selenium, ensuring you always have access to fresh content.
- **Intelligent Summarization**: Harness the power of the Pegasus model to generate succinct summaries of lengthy articles, making it easier to grasp essential information quickly.
- **Sentiment Analysis**: Utilize NLTK's SentimentIntensityAnalyzer to categorize articles as Positive, Negative, or Neutral, providing deeper insights into public sentiment.
- **Dual CSV Outputs**: Automatically generate two CSV files—one that contains the latest scraped data and another that appends new results with a timestamp, creating a comprehensive historical record.

## 🛠 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.6+**
- **Pip** (Python package installer)

## 📦 Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

2. **Install the required packages**:

   ```bash
   pip install -r requirements.txt

3. **Run the script with**:

   ```bash
   python main.py

4. After execution, two CSV files will be created in the project directory:

- **output.csv**: Contains the latest scraped articles and their summaries.
- **database.csv**: Continuously appends new entries with a date stamp for every run, allowing for easy historical tracking and creating a database.
