import requests


# https://openapi.wildberries.ru/prices/api/ru/

def get_discount(nmID):

        url = f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={nmID}'

        response = requests.get(url)

        js = response.json()

        try:
                basic_price = int(js['data']['products'][0]['sizes'][0]['price']['basic'])/100
                discounted_price = int(js['data']['products'][0]['sizes'][0]['price']['product'])/100
                discount = (basic_price - discounted_price)/basic_price
        except KeyError:
                discounted_price = -1
                discount = 1

        return discounted_price, discount


def set_price(api_key, nmID, price):
        url = 'https://discounts-prices-api.wb.ru/api/v2/upload/task'
        data = {'data': [{
                "nmID": int(nmID),
                "price": int(price),
                "discount": 0}]}

        header = {'Authorization': api_key, "Content-Type": 'application/json'}

        response = requests.post(url, json=data, headers=header)
        if response != '<Response [200]>':
                print("set_price:", response)


if __name__ == '__main__':
        print(get_discount(95101603))
        #set_price()