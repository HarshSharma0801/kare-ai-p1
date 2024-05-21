from groq import Groq
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from newsapi import NewsApiClient
import time


class IndustryAnalysis:
    def __init__(self, api_key, grok_model, news_api_key):
        self.client = Groq(api_key=api_key)
        self.grok_model = grok_model
        self.newsapi = NewsApiClient(api_key=news_api_key)

    def get_articles(
        self,
        industry_sector,
        industry_subsector,
        region,
        language="en",
        sort_by="relevancy",
        page=1,
    ):
        current_date = datetime.now()
        formatted_current_date = current_date.strftime("%Y-%m-%d")
        two_weeks_ago = current_date - timedelta(weeks=1)
        formatted_two_weeks_ago = two_weeks_ago.strftime("%Y-%m-%d")
        all_articles = self.newsapi.get_everything(
            q=f"{industry_sector} {industry_subsector} {region}",
            from_param=formatted_two_weeks_ago,
            to=formatted_current_date,
            language=language,
            sort_by=sort_by,
            page=page,
        )
        articles_list = []
        for article in all_articles["articles"]:
            articles_list.append({"title": article["title"], "url": article["url"]})
        return articles_list

    def find_top_competitors(self, industry_sector, industry_subsector, region):
        query = f"{industry_sector} {industry_subsector} top competitors in {region}"
        results = DDGS().text(query, max_results=30)
        formattedText = ""
        webpage_text = []
        for result in results:
            formattedText += f'{result["title"]} - {result["body"]}\n'

        response = requests.get(results[0]["href"])
        soup = bs(response.content, "lxml")
        for script in soup(["script", "style", "a"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        webpage_text = "\n".join(chunk for chunk in chunks if chunk)

        ExampleJSON = [{"company": ""}, {"company": ""}, {"company": ""}, ...]

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You provide answers in JSON ${ExampleJSON}",
                    },
                    {
                        "role": "user",
                        "content": f"""This is a data of top competitors below:
                        \n{formattedText}\n
                        {webpage_text}
                        You have to return the response as a list of top 10 competitors in a list format only.
                        Do not provide any other details except the list of top 10 competitors in the sector of {industry_sector} and subsector of {industry_subsector} only in {ExampleJSON} json format, no other information or format.  do not give anything other than the json.
                        If you don't know the answer, just say that, do not make stuff up.""",
                    },
                ],
                model=self.grok_model,
            )
        except requests.exceptions.HTTPError as e:
            time.sleep(1)  # Wait for one second before retrying
            print("trying again")
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"""This is a data of top competitors below:
                        \n{formattedText}\n
                        You have to return the response as a list of top 10 competitors in a list format only.
                        Do not provide any other details except the list of top 10 competitors in the sector of {industry_sector} and subsector of {industry_subsector}only in {ExampleJSON} json format, no other information or format.
                        If you don't know the answer, just say that, do not make stuff up.""",
                    }
                ],
                model=self.grok_model,
            )
        return chat_completion.choices[0].message.content

    def find_technological_trends(self, industry_sector, industry_subsector, region):
        query = (
            f"{industry_sector} {industry_subsector} technological trends in {region}"
        )
        results = DDGS().text(query, max_results=30)
        formattedText = ""
        ExampleJSON = [{"point": ""}, {"point": ""}, {"point": ""}, ...]
        for result in results:
            formattedText += f'{result["title"]} - {result["body"]}\n'

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You provide answers in JSON ${ExampleJSON}",
                },
                {
                    "role": "user",
                    "content": f"""This is a data for technological trends for the industry sector
                    {industry_sector} and sub sector industry - {industry_subsector} below:
                    \n{formattedText}\n
                    You have to return the technological trends for the above sector and sub sector strictly in {ExampleJSON} json format. do not give anything other than the json.
                    If you don\'t know the answer, just say that, do not make stuff up.""",
                },
            ],
            model=self.grok_model,
        )
        return chat_completion.choices[0].message.content

    def find_industry_trends(self, industry_sector, industry_subsector, region):
        query = f"{industry_sector} {industry_subsector} industry trends in {region}"
        results = DDGS().text(query, max_results=30)
        formattedText = ""
        ExampleJSON = [{"point": ""}, {"point": ""}, {"point": ""}, ...]
        for result in results:
            formattedText += f'{result["title"]} - {result["body"]}\n'
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You provide answers in JSON ${ExampleJSON}",
                },
                {
                    "role": "user",
                    "content": f"""This is a data for industry trends for the industry sector - {industry_sector} and sub sector industry - {industry_subsector} below:
                    \n{formattedText}\nYou have to return the industry trends for the above sector and sub sector strictly in {ExampleJSON} json format. do not give anything other than the json.
                    If you don\'t know the answer, just say that, do not make stuff up.""",
                },
            ],
            model=self.grok_model,
        )
        return chat_completion.choices[0].message.content

    def find_key_takeways(
        self, industry_sector, industry_subsector, company_value_proposition, region
    ):
        ExampleJSON = [{"point": ""}, {"point": ""}, {"point": ""}, ...]
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You provide answers in JSON ${ExampleJSON}",
                },
                {
                    "role": "user",
                    "content": f"""Please analyze the industry sector and subsector for a company with the following value proposition:\nIndustry Sector:
                    {industry_sector}\nIndustry Subsector: {industry_subsector}\nCompany Value Proposition: {company_value_proposition}\n in {region}
                    Provide key takeaways strictly in {ExampleJSON} json format for the company within its specific sector. Exclude any unnecessary information from the answer.  do not give anything other than the json.
                    If you don\'t know the answer, just say that, do not make stuff up.""",
                },
            ],
            model=self.grok_model,
        )
        return chat_completion.choices[0].message.content

    def top_5_predictions(self, industry_sector, industry_subsector, region):
        query = f"{industry_sector} {industry_subsector} top predictions"
        results = DDGS().text(query, max_results=30)
        formattedText = ""
        for result in results:
            formattedText += f'{result["title"]}, {result["href"]} - {result["body"]}\n'
        ExampleJSON = [
            {"title": "", "href": "", "body": ""},
            {"title": "", "href": "", "body": ""},
            {"title": "", "href": "", "body": ""},
            ...,
        ]
        ResponseFormatJSON = [
            {"prediction": "", "source": ""},
            {"prediction": "", "source": ""},
            {"prediction": "", "source": ""},
            ...,
        ]
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You provide answers in JSON ${ResponseFormatJSON}",
                },
                {
                    "role": "user",
                    "content": f"""You have provided the data below for the Top predictions in the industry sector - {industry_sector} and subsector - {industry_subsector} based in {region}\n
                    {formattedText} in the form of json that contains title, url, body.\nExample of strictly JSON provided -{ExampleJSON} \nYou have to give a list of at least top 5 predictions for the give sector and sub sector.
                    Also include href for sources with each prediction. The format of response should be in {ResponseFormatJSON} json format in the form of a structured list.  do not give anything other than the json.
                    If you don\'t know the answer, just say that, do not make stuff up.""",
                },
            ],
            model=self.grok_model,
        )
        return chat_completion.choices[0].message.content

    def market_size_prediciton(self, industry_sector):
        renewable_graph = '<a href="https://www.statista.com/statistics/1094309/renewable-energy-market-size-global/" rel="nofollow"><img src="https://www.statista.com/graphic/1/1094309/renewable-energy-market-size-global.jpg" alt="Statistic: Renewable energy market size worldwide in 2021, with a forecast for 2022 to 2030 (in billion U.S. dollars) | Statista" style="width: 100%; height: auto !important; max-width:1000px;-ms-interpolation-mode: bicubic;"/></a><br />Find more statistics at  <a href="https://www.statista.com" rel="nofollow">Statista</a>'

        ai_graph = '<a href="https://www.statista.com/statistics/1256246/worldwide-explainable-ai-market-revenues/" rel="nofollow"><img src="https://www.statista.com/graphic/1/1256246/worldwide-explainable-ai-market-revenues.jpg" alt="Statistic: Size of explainable artificial intelligence (AI) market worldwide from 2022 to 2030 (in billion U.S. dollars) | Statista" style="width: 100%; height: auto !important; max-width:1000px;-ms-interpolation-mode: bicubic;"/></a><br />Find more statistics at  <a href="https://www.statista.com" rel="nofollow">Statista</a>'
        if industry_sector == "Renewable Energy":
            return renewable_graph
        elif industry_sector == "Artificial Intelligence":
            return ai_graph


if __name__ == "__main__":
    api_key = "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"
    grok_model = "mixtral-8x7b-32768"
    news_api_key = "2f4a447b4c3942b2bb0504ea778ee9cc"
    analysis = IndustryAnalysis(api_key, grok_model, news_api_key)

    industry_sector = "Technology"
    industry_subsector = "Artificial Intelligence"
    company_value_proposition = "Helping creating market research workflow"
    region = "India"

    print(analysis.get_articles(industry_sector, industry_subsector, region))
    print("-------------------------------------------------")
    print(analysis.find_top_competitors(industry_sector, industry_subsector, region))
    print("-------------------------------------------------")
    print(analysis.find_technological_trends(industry_sector, industry_subsector, region))
    print("-------------------------------------------------")
    print(analysis.find_industry_trends(industry_sector, industry_subsector, region))
    print("-------------------------------------------------")
    print(
        analysis.find_key_takeways(
            industry_sector, industry_subsector, company_value_proposition, region
        )
    )
    print("-------------------------------------------------")
    print(analysis.top_5_predictions(industry_sector, industry_subsector, region))
