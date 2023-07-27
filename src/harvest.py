import os
from newscatcher.NewsAPI import NewsAPI
from helpers.s3Helper import s3Helper

api_key = os.environ.get('NEWSCATCHER_API_KEY')

def main():
    if api_key:
        news_api = NewsAPI(api_key)
        news_api.set_work_folder('/app')  # Set the working folder to '/app' inside the container

        queries = ['Ukraine war', 'Russia invasion', 'Conflict in Ukraine', 'Nato initial agreements', 'Countries helping Ukraine', 'Russia allies', 'Kremlin invasion']

        news_api.make_requests(queries, from_date='2023/06/27')

        # Generate CSV file from dict
        news_api.generate_csv('/app/extracted_news_articles.csv')

        # Generate CSV file from pandas table
        news_api.generate_pandas_csv('/app/extracted_news_articles_pandas.csv')
    else:
        print("Error: No NewsCatcher API key provided.")

if __name__=='__main__':
    main()