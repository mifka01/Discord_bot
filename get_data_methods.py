import requests
import datetime
from bs4 import BeautifulSoup
import os

def get_covid_data():
    result = requests.get("https://onemocneni-aktualne.mzcr.cz/covid-19")
    source = result.text
    soup = BeautifulSoup(source, 'lxml')
    test_count = soup.find(id="count-test")
    sick_count = soup.find(id="count-sick")
    dead_count = soup.find(id="count-dead")
    recovered_count = soup.find(id="count-recover")
    uptime = soup.find(id="last-modified-datetime")
    return {'test_count': test_count.text,
            'sick_count': sick_count.text,
            'recovered_count': recovered_count.text,
            'dead_count': dead_count.text,
            'uptime': str(uptime.text).strip()}

            
def get_rnumber_data():
    result = requests.get('https://www.seznamzpravy.cz/sekce/koronavirus-stopcovid')
    source = result.text
    soup = BeautifulSoup(source, 'lxml')
    reproduction_number = soup.find('h3')
    return str(reproduction_number.text)


def get_sport_data():
    articles = []
    result = requests.get('https://www.sport.cz/')
    source = result.text
    soup = BeautifulSoup(source, 'lxml')
    clanky = soup.find_all('span', {'class': 'next-article clearfix'})[0:4]

    for clanek in clanky:

        current_article = {}
        times = clanek.findChildren("span", {'class': 'next-article-time'})
        titles = clanek.findChildren("h3", {'class': 'next-article-title'})
        imgs = clanek.findChildren("img")
        url = f'https://www.sport.cz/{clanek.parent["href"]}'

        result = requests.get(url)
        source = result.text
        soup = BeautifulSoup(source, 'lxml')
        current_article["description"] = soup.find("div", id="perex").text

        for i in range(len(times)):
            current_article["time"] = times[i].text.strip().replace("  ", " ")
            current_article["title"] = titles[i].text
            current_article["image"] = imgs[i]["src"]
        articles.append(current_article)
    return articles


def get_news_data(url):
    articles = []
    result = requests.get(url)
    source = result.text
    soup = BeautifulSoup(source, 'lxml')
    sections = soup.find_all('section', {'class': 'n_hK'})
    section_divs = sections[1].find_all("div", recursive=False)
    top_new = {"title": section_divs[0].find('h3', {'class': 'd_r d_u f_bK'}).text.replace("\xa0", " "), 
               "time": section_divs[0].find('span', {'class': 'atm-date-formatted'}).text,
               'image': f'https:{section_divs[0].find("img")["src"]}',
               "url": section_divs[0].find('a')["href"]}

    result = requests.get(top_new['url'])
    source = result.text
    soup = BeautifulSoup(source, 'lxml')
    top_new['description'] = soup.find('p', {'class': 'd_cM'}).text.replace("\xa0", " ")

    articles.append(top_new)
    other_news = section_divs[1].find_all('li', {'class': 'd_dS g_fU'})[0:3]

    for new in other_news:
        article = {"title": new.find('h3', {'class': 'd_r d_u f_bK'}).text.replace("\xa0", " "), 
                   "time": new.find('span', {'class': 'atm-date-formatted'}).text,
                   'image': f'https:{new.find("img")["src"]}',
                   "url": new.find('a')["href"]}

        result = requests.get(article['url'])
        source = result.text
        soup = BeautifulSoup(source, 'lxml')
        article['description'] = soup.find('p', {'class': 'd_cM'}).text.replace("\xa0", " ")
        articles.append(article)
    return articles


def get_weather_data(city):
    result = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={str(os.environ.get("API_KEY"))}&units=metric')
    data = result.json()
    weather_data = {
        "city_name": data["name"],
        "city_state": data["sys"]["country"],
        "city_current_temp": data["main"]["temp"],
        "city_feels_like": data["main"]["feels_like"],
        "city_temp_min": data["main"]["temp_min"],
        "city_temp_max": data["main"]["temp_max"],
        "city_datetime": datetime.datetime.fromtimestamp(data["dt"]),
        "city_weather_status": data["weather"][0]["description"].capitalize(),
        "city_sunrise": datetime.datetime.fromtimestamp(data["sys"]["sunrise"]).time(),
        "city_sunset": datetime.datetime.fromtimestamp(data["sys"]["sunset"]).time()
    }
    return weather_data

