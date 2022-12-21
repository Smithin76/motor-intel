import requests
from bs4 import BeautifulSoup
from constants import SCRAPER_API_KEY


class ScrapeRedbook:

    def __init__(self):
        self.base_url = "https://www.redbook.com.au/cars/results?q=%28Make%3D%5B{}%5D%26Model%3D%5B{}%5D%29"

    # def fetch_html(self, file_name='redbook_home.html'):
    #     with open(f"{ROOT_DIR}/{DATA_FOLDER}/{file_name}") as fp:
    #         file = fp.read()
    #         return file


    def fetch_html_scraperapi(self):
        payload = {'api_key': f'{SCRAPER_API_KEY}', 'url': 'https://www.redbook.com.au/cars/results?q=%28Make%3D%5B{}%5D%26Model%3D%5B{}%5D%29', 'timeout': 30}
        response = requests.get('http://api.scraperapi.com', params=payload)
        html = response.text
        # print(html)
        ht = open('html_data.html', 'a')
        ht.write(html)
        return html

    def find_div(self, html, div_class):
        soup = BeautifulSoup(html, 'html.parser')
        divs_data = soup.find_all("div", {"class": div_class})
        return divs_data

    def fetch_models(self, html):
        # div_data = self.find_div(html=html, div_class=['refine-item Make', 'refine-item Make initially_hidden'])
        div_data = self.find_div(html=html, div_class=['multiselect-content h-100'])
        models = []
        print(div_data, 'dvvvdataaaaaaaaaaaaaaaaaaaaaa')
        # for data in div_data:
        #     doc = data.text.replace('(', '').replace(')', '')
        #     make = doc.split('\n')
        #     make.remove("")
        #     models.append(make)
        # models.pop()
        # return models


if __name__ == '__main__':
    scrape = ScrapeRedbook()
    content = scrape.fetch_html_scraperapi()
    models = scrape.fetch_models(html=content)


