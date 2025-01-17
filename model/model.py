from groq import Groq
import requests
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import time


class IndustryAnalysis:
    def __init__(self, api_key_1, api_key_2 , grok_model):
        self.client1 = Groq(api_key=api_key_1)
        self.client2 = Groq(api_key=api_key_2)
        self.grok_model = grok_model

    def get_articles(
        self,
        industry_sector,
        industry_subsector,
        region,
    ):

        all_articles = DDGS().news(
            f"{industry_sector} {industry_subsector} {region} news", max_results=5
        )
        articles_list = []
        for article in all_articles:
            articles_list.append(
                {
                    "title": article["title"],
                    "url": article["url"],
                    "body": article["body"],
                    "image": article["image"],
                }
            )
        # for article in articles_list:
        #     print(article)
        #     print("\n")
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
            chat_completion = self.client1.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You provide answers in JSON {ExampleJSON}",
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
            chat_completion = self.client1.chat.completions.create(
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

        chat_completion = self.client1.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You provide answers in JSON {ExampleJSON}",
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
        chat_completion = self.client1.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You provide answers in JSON {ExampleJSON}",
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
        chat_completion = self.client1.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You provide answers in JSON {ExampleJSON}",
                },
                {
                    "role": "user",
                    "content": f"""Please analyze the industry sector and subsector for a company with the following value proposition:\nIndustry Sector:
                    {industry_sector}\nIndustry Subsector: {industry_subsector}\nCompany Value Proposition: {company_value_proposition}\n in {region}
                    Provide key takeaways strictly in {ExampleJSON} json format for the company within its specific sector. The Key Takeaways should be descriptive, useful, and helpful for the company to improve or grow better. Exclude any unnecessary information from the answer.do not give anything other than the json.
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
        chat_completion = self.client2.chat.completions.create(
        messages=[
                {
                    "role": "system",
                    "content": f'You provide answers in JSON format as specified in {ResponseFormatJSON}.',
                },
                {
                    "role": "user",
                    "content": f"""You have provided data on the top predictions for the industry sector - {industry_sector} and subsector - {industry_subsector} in the region - {region}.\n
                    {formattedText}\n
                    The data should be in JSON format containing fields for title, url, and body.\n
                    Example JSON format: {ExampleJSON}\n
                    Provide a list of at most the top 5 predictions for the given sector and subsector, including a href link to the sources for each prediction. Ensure the response strictly adheres to the JSON format specified in {ResponseFormatJSON}.\n
                    Do not include any information other than the JSON response.\n
                    If you do not know the answer, simply state that you do not know; do not fabricate information.""",
                },
            ],
            model=self.grok_model,
        )
        return chat_completion.choices[0].message.content

    # def market_size_prediciton(self, industry_sector):
    #     renewable_graph = '<a href="https://www.statista.com/statistics/1094309/renewable-energy-market-size-global/" rel="nofollow"><img src="https://www.statista.com/graphic/1/1094309/renewable-energy-market-size-global.jpg" alt="Statistic: Renewable energy market size worldwide in 2021, with a forecast for 2022 to 2030 (in billion U.S. dollars) | Statista" style="width: 100%; height: auto !important; max-width:1000px;-ms-interpolation-mode: bicubic;"/></a><br />Find more statistics at  <a href="https://www.statista.com" rel="nofollow">Statista</a>'

    #     ai_graph = '<a href="https://www.statista.com/statistics/1256246/worldwide-explainable-ai-market-revenues/" rel="nofollow"><img src="https://www.statista.com/graphic/1/1256246/worldwide-explainable-ai-market-revenues.jpg" alt="Statistic: Size of explainable artificial intelligence (AI) market worldwide from 2022 to 2030 (in billion U.S. dollars) | Statista" style="width: 100%; height: auto !important; max-width:1000px;-ms-interpolation-mode: bicubic;"/></a><br />Find more statistics at  <a href="https://www.statista.com" rel="nofollow">Statista</a>'
    #     if industry_sector == "Renewable Energy":
    #         return renewable_graph
    #     elif industry_sector == "Artificial Intelligence":
    #         return ai_graph

    def market_size(self, industry_sector, industry_subsector, company_value_proposition):
        query = f"{industry_sector} {industry_subsector} market size data yearly"
        results = DDGS().text(query, max_results=30)
        # print(results)
        formattedText = ""
        for result in results:
            formattedText += f'${result["title"]} - ${result["body"]}\n'
        ExampleJSON = [{'title': "", 'body': ""}, {'title': "", 'body': ""}, {'title': "", 'body': ""}]
        year = "2030"
        ResponseFormatJSON = [
            {"source": [
                {"link": ""},
                {"link": ""},
                {"link": ""}
            ] 
                
                },
            {
                "chart_data": [
                {"year": "YYYY", "market_size": "X.XX", "unit": "billion USD"},
                {"year": "YYYY", "market_size": "X.XX", "unit": "billion USD"},
                ...
            ]
            }
        ]
        chat_completion = self.client2.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"You provide answers in JSON format as specified in {ResponseFormatJSON}.",
                },
                {
                    "role": "user",
                    "content": f"""Please provide the market size data for the industry sector {industry_sector} and subsector {industry_subsector} in JSON format. The JSON should contain fields for title, href, and body. An example of the JSON structure is as follows: {ExampleJSON}.\nOutput a list of market sizes for all years up to {year} for the specified sector and subsector. Provide only relevant source links and do not exceed 5 sources. The response format should strictly adhere to the following JSON format: {ResponseFormatJSON}.\nEnsure the market size unit is consistently stated in billion USD for each response. Include market sizes starting from the year 2012. Only provide the market size data as stated. Avoid including any unnecessary data. Include future market size predictions if available. If you do not know the answer, simply state that you do not know; do not provide any inaccurate information."""
                }
            ],
            model=self.grok_model,
        )
        return chat_completion.choices[0].message.content



if __name__ == "__main__":
    api_key_1 = "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"
    api_key_2 = "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"
    grok_model = "mixtral-8x7b-32768"
    analysis = IndustryAnalysis(api_key_1, api_key_2 , grok_model)

    industry_sector = "Healthcare"
    industry_subsector = "Digital Health"
    company_value_proposition = (
        "Helping patients with special cases to doctors in india and worldwide"
    )
    region = "worldwide"

    print(analysis.get_articles(industry_sector, industry_subsector, region))
    # print("-------------------------------------------------")
    # print(analysis.find_top_competitors(industry_sector, industry_subsector, region))
    # print("-------------------------------------------------")
    # print(
    #     analysis.find_technological_trends(industry_sector, industry_subsector, region)
    # )
    # print("-------------------------------------------------")
    # print(analysis.find_industry_trends(industry_sector, industry_subsector, region))
    # print("-------------------------------------------------")
    # print(
    #     analysis.find_key_takeways(
    #         industry_sector, industry_subsector, company_value_proposition, region
    #     )
    # )
    # print("-------------------------------------------------")
    # print(analysis.top_5_predictions(industry_sector, industry_subsector, region))
