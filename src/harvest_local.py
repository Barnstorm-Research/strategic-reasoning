import os
from NewsAPI import NewsAPI
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

api_key = ''

news_api = NewsAPI(api_key)

work_folder = '/Users/marjanabdollahi/Desktop/BRC/Barnstorm_project_23/IRAD'
news_api.set_work_folder(work_folder)

start_date = datetime(2022, 1, 1)
# end_date = datetime(2023, 3, 31)
end_date = datetime.now()
date_ranges = [(start_date, end_date)]

def get_articles_and_save_locally(news_api, queries, folder_name, from_date, to_date):
    for query, _ in queries:
        while from_date <= to_date:
            next_month = from_date + relativedelta(months=1) # calculate next month
            last_day_current_month = next_month - timedelta(days=1)

            last_day = min(last_day_current_month, to_date)
            file_path = os.path.join(work_folder, f"{folder_name}_{from_date.strftime('%Y%m%d')}_to_{last_day.strftime('%Y%m%d')}.csv")

            if not os.path.exists(file_path):
                news_api.make_requests([query], from_date=from_date.strftime('%Y-%m-%d'), to_date=to_date.strftime('%Y-%m-%d'))
            # df = news_api.generate_csv()
            
                news_api.generate_csv(file_path)
            # df.to_csv(file_path, sep=';', index=False)
            from_date = next_month
# Strategy: NATO/US
nato_us_queries = [
    ("Russian sanctions", "russian_sanctions"),
    ("F16 to Ukraine", "technology_trade"),
    ("tank to Ukraine", "technology_trade"),
    ("NATO expansion", "nato_expansion"),
    ("NATO Finland", "nato_expansion"),
    ("NATO Sweden", "nato_expansion")
]

# Strategy Russia
russia_queries = [
    ("Russian shell stockpile", "russian_munitions"),
    ("Wagner in Ukraine", "wagner"),
    ("Wagner", "wagner"),
    ("Russian grain deal", "grain_deal")
]

# Combine both query lists
all_queries = nato_us_queries + russia_queries

for query, folder_name in all_queries:
    get_articles_and_save_locally(news_api, [(query, folder_name)], folder_name, start_date, end_date)