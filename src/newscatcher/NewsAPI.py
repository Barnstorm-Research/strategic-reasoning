import time
import csv
import os
import json
import requests
import pandas as pd

class NewsAPI:
    def __init__(self, api_key):
        self.base_url = 'https://api.newscatcherapi.com/v2/search'
        self.headers = {'x-api-key': api_key}
        self.all_news_articles = []

    def set_work_folder(self, folder_path):
        self.work_folder = folder_path
        if not os.path.exists(self.work_folder):
            os.makedirs(self.work_folder)
        os.chdir(self.work_folder)

    def make_request(self, query, lang='en', to_rank=10000, page_size=100, from_date=None):
        params = {
            'q': query,
            'lang': lang,
            'to_rank': to_rank,
            'page_size': page_size,
            'page': 1,
            'from': from_date
        }
        self.all_news_articles = []  # Reset previous articles

        while True:
            time.sleep(1)
            response = requests.get(self.base_url, headers=self.headers, params=params)
            results = json.loads(response.text.encode())

            if response.status_code == 200:
                print(f'Done for page number => {params["page"]}')
                for article in results['articles']:
                    article['used_params'] = str(params)
                self.all_news_articles.extend(results['articles'])

                params['page'] += 1
                if params['page'] > results['total_pages']:
                    print("All articles have been extracted")
                    break
                else:
                    print(f'Proceed extracting page number => {params["page"]}')
            else:
                print(results)
                print(f'ERROR: API call failed for page number => {params["page"]}')
                break

        print(f'Number of extracted articles => {str(len(self.all_news_articles))}')

    def make_requests(self, queries, lang='en', to_rank=10000, page_size=100, from_date=None):
        for query in queries:
            self.make_request(query, lang, to_rank, page_size, from_date)

    def generate_csv(self, filename):
        field_names = list(self.all_news_articles[0].keys())
        with open(filename, 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=";")
            writer.writeheader()
            writer.writerows(self.all_news_articles)

    def generate_pandas_csv(self, filename):
        pandas_table = pd.DataFrame(self.all_news_articles)
        pandas_table.to_csv(filename, encoding='utf-8', sep=';')
