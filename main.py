import requests
import json
import time


class Parser:
    def __init__(self):
        self.pages = None
        self.query = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0',
            'Accept': '*/*',
            'x-queryid': 'qid99008530171869466120240618071135'
        }
        self.productsJson = {'products': {}}

    def saveToJson(self):
        with open('result.json', 'w', encoding='utf-8') as f:
                json.dump(self.productsJson, f, ensure_ascii=False, indent=4)

    def getUrl(self, page):
        return f'https://search.wb.ru/exactmatch/ru/common/v5/search?ab_testing=false&appType=1&curr=rub&dest=-1172839&query={self.query}&resultset=catalog&sort=popular&spp=30&suppressSpellcheck=false&page={page}'

    def getResponse(self, url):
        return requests.get(url=url, headers=self.headers)

    def setPages(self, pages):
        self.pages = pages

    def setQuery(self, query):
        self.query = query

    def parse(self):
        self.productsJson['products'][self.query] = {}
        for page in range(1, self.pages+1):
            print('\n'+'Page: '+str(page)+'\n')
            time.sleep(2)

            url = self.getUrl(page)
            searchResult = (self.getResponse(url)).json()
            products = searchResult['data']['products']
            for product in products:
                print('Article: '+str(product['id']))
                print('Brand: '+str(product['brand']))
                print('Name: '+str(product['name']))
                print('='*40)
                id = product['id']
                self.productsJson['products'][self.query][id] = {
                    'brand': product['brand'],
                    'name': product['name']
                }
                time.sleep(0.01)

def main():
    parser = Parser()
    while True:
        query = (input('\nВведите запрос(stop - сохранить и выйти): ')).lower()
        if query == 'stop':
            break
        pages = int(input('Сколько страниц парсить: '))

        parser.setPages(pages)
        parser.setQuery(query)
        parser.parse()

    parser.saveToJson()

if __name__ == '__main__':
    main()
