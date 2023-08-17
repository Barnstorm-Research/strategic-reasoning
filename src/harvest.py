# using environment variables in the docker-compose.yml file, can access their values in the Python file using the os library
#docker-compose up -d
import os
from newscatcher.NewsAPI import NewsAPI
from datetime import datetime, timedelta
from helpers.s3Helper import s3Helper

# S3 bucket configuration
s3_key = os.environ.get('S3_KEY')
s3_secret = os.environ.get('S3_SECRET')
s3_endpoint = os.environ.get('S3_ENDPOINT')
s3_region = os.environ.get('S3_REGION')
s3_bucket = os.environ.get('S3_BUCKET')
api_key = os.environ.get('NEWSCATCHER_API_KEY')

if s3_key and s3_secret and s3_endpoint and s3_region and s3_bucket:
    s3 = s3Helper(s3_key, s3_secret, s3_endpoint, s3_region, s3_bucket)
else:
    print("Error: Missing S3 bucket configuration")


if api_key:
    news_api = NewsAPI(api_key)
    news_api.set_work_folder('/home')
else:
    print("Error: No NewsCatcher API key provided.") 

def get_monthly_date_ranges(start_date, end_date):
    date_ranges = []
    current_date = start_date
    while current_date < end_date:
        next_month = current_date.replace(day=1) + timedelta(days=32)
        last_day = next_month - timedelta(days=1)
        date_ranges.append((current_date, last_day))
        current_date = next_month
    return date_ranges

start_date = datetime(2023, 8, 1)
end_date = datetime.now()

date_ranges = get_monthly_date_ranges(start_date, end_date)

def get_articles_and_save_to_s3(news_api, s3_helper, queries, folder_name, from_date, to_date):
    while from_date <= to_date:
        #Get the end of the current month
        next_month = from_date.replace(day=28) + timedelta(days=32)
        last_day = next_month - timedelta(days=1)
        to_date_str = last_day.strftime("%Y%m%d")

        file_path = f"{folder_name}/{from_date.strftime('%m%d%Y')} - {to_date_str}.csv"
        print(file_path)
        news_api.make_requests(queries, from_date=from_date.strftime('%Y/%m/%d'), to_date=last_day.strftime('%Y/%m/%d'))

        #Generate DataFrame from dict
        df = news_api.generate_csv()
        # Save dataframe to s3
        s3_helper.writeFile(file_path, df)

        # Generate CSV file from dict and save to S3
        # news_api.generate_csv(file_path, s3_helper)
        # Move to the next month
        from_date = next_month



# Strategy: NATO/US
nato_us_queries = [
    ("Russian sanctions", "russian-sanctions"),
    ("F16 to Ukraine", "technology-trade"),
    ("tank to Ukraine", "technology-trade"),
    ("NATO expansion", "nato-expansion"),
    ("NATO Finland", "nato-expansion"),
    ("NATO Sweden", "nato-expansion")
]
for query, folder_name in nato_us_queries:
    for from_date, to_date in date_ranges:
        get_articles_and_save_to_s3(news_api, s3, [query], folder_name, from_date, to_date)

# Strategy Russia
russia_queries = [
    ("Russian shell stockpile", "russian-munitions"),
    ("Wagner in Ukraine", "wagner"),
    ("Wagner", "wagner"),
    ("Russian grain deal", "grain-deal")
]
for query, folder_name in russia_queries:
    for from_date, to_date in date_ranges:
        get_articles_and_save_to_s3(news_api, s3, [query], folder_name)