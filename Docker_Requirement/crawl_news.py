import requests
from bs4 import BeautifulSoup

def news_detail(link):
    if link==None:
        return {'news_type': '', 'category': [], 'title': '', 'location': '', 'description': '', 'content': [], 'author': '', 'media': [], 'raw_body': ''}
    news_type = 'text_paper'
    news = BeautifulSoup(requests.get(link).content, "html.parser")
    if news.find('article', class_='fck_detail')==None or news.find('h1', class_='title-detail')==None:
        # if news.find('section', class_='top_detail')==None:
        #     return {'news_type': '', 'title': '', 'location': '', 'description': '', 'content': [], 'author': '', 'media': [], 'raw_body': ''}
        # news_type = 'video'
        return {'news_type': '', 'category': [], 'title': '', 'location': '', 'description': '', 'content': [], 'author': '', 'media': [], 'raw_body': ''}
    
    article = news.find('article', class_='fck_detail')
    title = news.find('h1', class_='title-detail').text
    desc = news.find('p', class_='description')
    location = desc!=None and desc.find('span', class_='location-stamp')!=None and desc.find('span', class_='location-stamp').text or ''
    desc_text = desc.text[location and len(location) or 0:]
    category = [i.text or '' for i in news.find('ul', class_ ='breadcrumb').findAll('li')]
    
    content = []
    media = []
    author = ''
    if news.find('article', class_='fck_detail', id='lightgallery') != None:
        news_type = 'slide_show'
        for i in article.findAll('div', class_='item_slide_show'):
            media.append({'alt': '', 'src': i.find('source').attrs['data-srcset'].split()[-2]})
            content.append('<figure>')
            content.extend([a.text for a in i.find('div', class_='desc_cation').findAll('p')])
        author = article.find('div', class_='width-detail-photo').find('strong')!=None and article.find('div', class_='width-detail-photo').find('strong').text or ''
    else:
        content = [i.find('img') == None and i.text or '<figure>' for i in article.findAll(['p', 'figure'], class_=['Normal', 'tplCaption'])]
        author = article.find('p', class_='author_mail')!=None and article.find('p', class_='author_mail').find('strong').text or len(content)>0 and content.pop() or ''
        media = [{'alt': f.find('img').attrs['alt'], 'src': 'data-src' in f.find('img').attrs and f.find('img').attrs['data-src'] or f.find('img')['src']} for f in article.findAll('figure') if f.find('img')!=None]
        if len(content)==0 and len(media)==0:
            news_type = 'video'
    raw_body = 'str(article)'

    return {'news_type': news_type, 'category': category, 'title': title, 'location': location, 'description': desc_text, 'content': content, 'author': author, 'media': media, 'raw_body': raw_body}

def crawl_top_express_news():
    all_news = []
    urls = ['https://vnexpress.net/tin-tuc-24h', 'https://vnexpress.net/tin-tuc-24h-p2', 'https://vnexpress.net/tin-tuc-24h-p3']
    for url in urls:
        try:
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            
            container = soup.findAll('article', class_='item-news')
            for item in container:
                try:
                    content = item.find('h3', class_='title-news')
                    if content==None:
                        continue
                    title = content.find('a').attrs['title']
                    link = content.find('a').attrs['href']
                    datetime = item.find('span', class_='time-ago') and item.find('span', class_='time-ago').attrs['datetime'] or None
                    all_news.append({
                        'title': title,
                        'link': link,
                        'datetime': datetime
                    })
                except:
                    pass
        except:
            pass
    
    final_result = []
    for news in all_news:
        try:
            news['detail'] = news_detail(news['link'])
            final_result.append(news)
        except:
            pass
        
    return final_result

def update_vnexpress_news():
    all_news = []
    url= 'https://vnexpress.net/tin-tuc-24h'
    
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    
    container = soup.findAll('article', class_='item-news')
    for item in container:
        try:
            content = item.find('h3', class_='title-news')
            if content==None:
                continue
            title = content.find('a').attrs['title']
            link = content.find('a').attrs['href']
            datetime = item.find('span', class_='time-ago') and item.find('span', class_='time-ago').attrs['datetime'] or None
            all_news.append({
                'title': title,
                'link': link,
                'datetime': datetime
            })
        except:
            pass
        
    final_result = []
    for news in all_news:
        try:
            news['detail'] = news_detail(news['link'])
            final_result.append(news)
        except:
            pass
        
    return final_result



