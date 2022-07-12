from vnexpressAPI.crawl_data import crawl_news
from vnexpressAPI.models import News, Media, NewsCategory, detail_news
import re
import unidecode

# import setting
from src.settings import TYPE_SERVER
# from datetime import datetime

# def to_timestamp(text, format='%Y-%m-%dT%H:%M:%S'):
#     return int(datetime.timestamp(datetime.strptime(text.split('.')[0], format)))
import time
# Run in update_news server only
def auto_update_news():
    while True:
        update_news()
        print('Sleep for 10 minutes!')
        time.sleep(600)

def to_url_param(text):
    if type(text)==str:
        return re.sub(r'\s+', '_', re.sub(r'\W+', ' ', unidecode.unidecode(text)).strip().lower())
    elif type(text)==list:
        return '__'.join([to_url_param(i) for i in text])


def delete_all_news():
    print('Delete all news!')
    detail_news.objects.all().delete()
    NewsCategory.objects.all().delete()
    # Media.objects.all().delete()
    # News.objects.all().delete()

def save_news(news):
    temp = News.objects.filter(news_url_param=to_url_param(news.get('title')), link=news.get('link'))
    if len(temp) > 0:
        print('News already exists!')
        return
    n_ctgr = NewsCategory.objects.filter(name='_'.join(news['detail']['category']))
    if len(n_ctgr) == 0:
        n_ctgr = NewsCategory(param_name=to_url_param(news['detail']['category']), name='_'.join(news['detail']['category']))
        n_ctgr.save()
    else:
        n_ctgr = n_ctgr.first()
    
    detail = news['detail']
    media_instance = [Media.objects.create(**i) for i in detail['media']]
    del detail['media'], detail['category']
    detail_instance = detail_news.objects.create(**detail)
    detail_instance.media.set(media_instance)
    
    print('Saving news! +1')
    return News.objects.create(
        title=news.get('title'),
        news_url_param=to_url_param(news.get('title')),
        # datetime=to_timestamp(news.get('datetime')),
        link=news.get('link'),
        category=n_ctgr,
        detail=detail_instance
    )

def update_news():
    print('Crawl data!')
    all_news = crawl_news.update_vnexpress_news()
    
    print('Updating!')
    for news in all_news:
        save_news(news)

def refresh_top_news():
    delete_all_news()
    
    print('Crawl data!')
    all_news = crawl_news.crawl_top_express_news()
    
    print('Saving!')
    for news in all_news:
        save_news(news)


# For test server only
if TYPE_SERVER == 'LOAD_DATA':
    auto_update_news()
