from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import os
import nltk
import re
import datetime
nltk.download('vader_lexicon')

def append_to_csv(data, file_path):
    # Check if the file already exists
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(['Date', 'Text', 'Link', 'Summarized_Data', 'Sentiment'])

        for row in data:
            writer.writerow(row)


def get_html(url):
    # Use Selenium to render JavaScript content
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode

    # Create a Service object with ChromeDriver path
    service = Service(ChromeDriverManager().install())

    # Initialize the WebDriver with Service and Options
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    driver.implicitly_wait(5)  # Implicit wait for page to load
    html = driver.execute_script('return document.documentElement.outerHTML')
    driver.quit()
    return(html)



def summarize_text(text, max_length=1024):
    # Load the pre-trained Pegasus model and tokenizer
    tokenizer = PegasusTokenizer.from_pretrained('DunnBC22/pegasus-multi_news-NewsSummarization_BBC')
    model = PegasusForConditionalGeneration.from_pretrained('DunnBC22/pegasus-multi_news-NewsSummarization_BBC')

    # Tokenize the input text
    inputs = tokenizer.encode(text, truncation=True, max_length=1024, padding='longest', return_tensors='pt')

    # Generate the summary
    with torch.no_grad():
        summary_ids = model.generate(inputs, max_length=max_length, num_beams=4, early_stopping=True)

    # Decode the generated summary
    summary = tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)

    return summary

def analyze_sentiment(article_text):
    # Create a SentimentIntensityAnalyzer object
    sid = SentimentIntensityAnalyzer()

    # Perform sentiment analysis
    sentiment_scores = sid.polarity_scores(article_text)
    # Classify sentiment based on the compound score
    compound_score = sentiment_scores['compound']
    if compound_score >= 0.05:
        sentiment = "Positive"
    elif compound_score <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment


def get_article_text(url):
    response = get_html(url)
    soup = BeautifulSoup(response , 'html.parser') 
    article_texts = []
    article_links = []
    check_links = []
    # Extract the dynamic class name out of the website
    head = soup.head
    if head: 
        head.extract()     # Remove the head contents from the extracted html response  
    str_s = soup
    str_soup = str(str_s) 
    pattern = r'"[^\s]*\/news\/articles\/[^\s]*"'
    match = re.search(pattern,str_soup).group(0).strip('"')
    class_name = soup.find('a', href=match)['class']
    class_name = ' '.join(class_name)
    count = 0

    # Find all the article elements on the page
    articles = soup.find_all('a', class_= class_name)
    #print(articles)
    for article in articles:
        flag = article.get('href')      # Flag to address non-articles in the soup
        if flag and '/news/' in flag and flag not in check_links:
            text_elements = article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            article_text = ' '.join([element.text.strip() for element in text_elements])
            if pd.isnull(article_text) or article_text.strip() == '': continue          # to remove empty or null headings
            article_texts.append(article_text)
            check_links.append(flag)
            article_link = flag

            if "https://www.bbc." in article_link : 
                article_links.append(article_link)
            else:
                url_part_1 = 'https://www.bbc.com'
                article_link = url_part_1 + article_link
                article_links.append(article_link)
            count=count+1    
        if(count==10):    
            break    
    
    # Visit each link and scrape the article data
    article_data = []
    for link in article_links:
        response = get_html(link)
        soup = BeautifulSoup(response, 'html.parser')
        text_elements = soup.find_all(attrs={'data-component': 'text-block'})
        if not text_elements : 
             text_elements = soup.find_all('p')
             article_text = ' '.join([element.text.strip() for element in text_elements])
             article_data.append(article_text)
        else:
            article_text = ' '.join([element.text.strip() for element in text_elements])
            article_data.append(article_text)  

    # Get the summary of each data element and sentiment of article
       
    summarized_data = []
    sentiment = []
    
    for sum in article_data:
        summarized_data.append(summarize_text(sum))

    for sen in summarized_data:
        sentiment.append(analyze_sentiment(sen))

    return article_texts, article_links , summarized_data , sentiment




url = 'https://www.bbc.com/news'
article_texts, article_links,article_data,sentiment = get_article_text(url)

# Get the directory path of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the file path
file_path = os.path.join(script_directory, 'output.csv')

# Define the file path for the appended CSV
append_file_path = os.path.join(script_directory, 'database.csv')

with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the headings to the CSV file
    writer.writerow(['Text', 'Link', 'Summarized_Data', 'Sentiment'])

    # Iterate over the data and write each row to the CSV file
    for text, link, data, sen in zip(article_texts, article_links, article_data, sentiment):
        writer.writerow([text, link, data, sen])

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
data_to_append = [(current_date, text, link, data, sen) for text, link, data, sen in zip(article_texts, article_links, article_data, sentiment)]
append_to_csv(data_to_append, append_file_path)


"""
for text, link , data , sen in zip(article_texts, article_links, article_data,sentiment):
    print('Text:', text)
    print('Link:', link)
    print('Summarized Data:', data)
    print('Sentiment:',sen)
    print('-' * 50)
"""