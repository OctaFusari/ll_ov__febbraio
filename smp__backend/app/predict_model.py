import pickle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import app.config as conf
from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import re


nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('punkt')

import requests

API_KEY = "d01247718bac41389c538614c1f0e9b4"

newsProva = ["We recently published a list of 12 Best Defensive Stocks To Buy Right Now. In this article, we are going to take a look at where Apple Inc. (NASDAQ:AAPL) stands against other best defensive stocks to buy right now.A notable event influencing current market sentiment is the recent selloff in technology stocks, primarily driven by speculations surrounding China’s DeepSeek AI model. This incident has underscored the market’s fragility, with key indicators pointing to potential instability. For instance, heavy betting on US tech stocks and rising bond yields have made equities less appealing compared to government debts, challenging the equity risk premium. In this context, the importance of defensive stocks becomes increasingly evident. Defensive stocks, also known as non-cyclical stocks, are those that provide consistent dividends and stable earnings regardless of the state of the overall market. They are typically found in sectors such as utilities, consumer staples, and healthcare.Read more about these developments by accessing 10 Best AI Data Center Stocks and 10 Buzzing AI Stocks According to Goldman Sachs.For example, companies that produce or distribute essential goods like food, beverages, and hygiene products tend to maintain steady cash flow and predictable earnings during both strong and weak economies. Dividends play a crucial role in investment strategies, offering both immediate income and long-term financial benefits. They represent a portion of a company’s earnings distributed to shareholders, typically on a quarterly basis. Historically, dividends have been a substantial component of total returns in the stock market. According to S&P Dow Jones Indices, since 1936, dividends have accounted for more than one-third of the total equity return of the S&P 500, with capital appreciation making up the other two-thirds.Read more about these developments by accessing 30 Most Important AI Stocks According to BlackRock and Beyond the Tech Giants: 35 Non-Tech AI Opportunities.For this article, we selected stocks that have solid businesses with recurring revenue streams, reliable dividend payouts, and burgeoning growth pipelines. These stocks are also popular among hedge funds. Why are we interested in the stocks that hedge funds pile into? The reason is simple: our research has shown that we can outperform the market by imitating the top stock picks of the best hedge funds. Our quarterly newsletter’s strategy selects 14 small-cap and large-cap stocks every quarter and has returned 275% since May 2014, beating its benchmark by 150 percentage points (see more details here).Is Apple Inc. (AAPL) the Best Defensive Stock to Buy Right Now? A wide view of an Apple store, showing the range of products the company offers.Apple Inc. (NASDAQ:AAPL) designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories. Apple has a history of returning value to shareholders through dividends and share repurchases. In the latest quarter, the company returned $30 billion to shareholders. The current annual dividend stands at $0.92 per share, yielding approximately 0.39%. Apple’s (NASDAQ:AAPL) substantial cash reserves, totaling $68 billion as of June 2024, support its capacity to maintain and potentially increase these returns. Apple’s diversified product portfolio and strong brand loyalty contribute to its resilience during economic downturns. The significant growth in its services segment, which boasts higher margins, enhances revenue stability. Overall, AAPL ranks 3rd on our list of best defensive stocks to buy right now. While we acknowledge the potential of AAPL as an investment, our conviction lies in the belief that some stocks hold greater promise for delivering higher returns, and doing so within a shorter time frame. If you are looking for a stock that is more promising than AAPL but that trades at less than 5 times its earnings, check out our report about the cheapest AI stock."]

def fetch_news(company):
    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={API_KEY}"
    response = requests.get(url)
    arrayNewsComp = []
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        print([article["url"] for article in articles if article["source"]["name"] in {"Yahoo Entertainment", "Gizmodo.com", "ABC News"}])
        
        for i in [{"url":article["url"], "sito":article["source"]["name"]} for article in articles if article["source"]["name"] in {"Yahoo Entertainment", "Gizmodo.com", "ABC News"}]:
            report_response = requests.get(i["url"])
            
            if report_response.status_code == 200:
                # Analizza il contenuto HTML
                report_response.encoding = 'utf-8-sig'
                soup = BeautifulSoup(report_response.text, "html.parser")

                if i["sito"] == "Yahoo Entertainment":
                    recirculation_elements = soup.find("div", attrs={"class":"article"})
                elif(i["sito"] == "Gizmodo.com"):
                    recirculation_elements = soup.find("article")
                elif(i["sito"] == "ABC News"):
                    recirculation_elements = soup.find("div", attrs={"class":"FITT_Article_main__body"})

                for unwanted in recirculation_elements.find_all(["script", "aside", "figure"]):
                    unwanted.decompose()

                text = recirculation_elements.get_text(separator="\n", strip=True)  # Rimuove i tag HTML
                """ text = re.sub(r'\s+', ' ', text)  # Rimuove spazi multipli
                text = re.sub(r'[^\w\s]', '', text)  # Rimuove simboli """
                arrayNewsComp.append(text) 

        #return [article["content"] for article in articles if article["source"]["name"] in {"Yahoo Entertainment", "Gizmodo.com", "ABC News"}]
        return arrayNewsComp

    return []

def predict_sentiment(news_list):
    with open(conf.MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    processed_news = [preprocess_text(news) for news in news_list]
    predictions = model.predict(processed_news)

    cv = CountVectorizer()
    cv.fit(newsProva)

    predictions__try = model.predict(newsProva)
    positive_indices = [x for x, x in enumerate(predictions) if x == "positive" or x == "negative"]
    
    return predictions.tolist()

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha() and word not in stop_words]
    return " ".join(tokens)