import data_gathering
import wb_connect
import schedule
from tqdm import tqdm
import time
import config
from loguru import logger


logger.add('main_log.log', level='DEBUG', format="{time} {level} {message}", rotation="10 MB")

def main():

    def update_price(api, table):
        for item in tqdm(table):
            #print(item[0])
            try:
                discounted_price, discount = wb_connect.get_discount(item[0])
                time.sleep(3)
                if discounted_price != -1:  # Значит товара нет в наличии
                    target_price = int(item[2])  # Цена из таблицы на которую нужно поменять
                    if discounted_price == target_price:  # Чтобы не грузить wb на берегу проверяем, а нужно ли менять цену
                        pass
                    else:
                        result = round((target_price) / (1 - discount), 0)
                        logger.debug(f'{item[0]}, discounted_price: {discounted_price}, discount: {discount}, Итоговая цена: {result}')
                        #print(result)
                        wb_connect.set_price(api, item[0], result)  # Меняем цену
                else:
                    logger.warning(f"Товара {item[0]} нет в наличии")
                    print(f"Товара {item[0]} нет в наличии")
            except IndexError:
                logger.error(f'Товара {item[0]} не существует!')
                print(f'Товара {item[0]} не существует!')
        print('Таблица закончилась')

    table1, table2 = data_gathering.DataGathering().main_parse()

    update_price(config.api_key_wb1, table1)
    update_price(config.api_key_wb2, table2)


if __name__ == '__main__':

    main()

    #schedule.every().day.at(config.start_time).do(main())

    #while True:
        #schedule.run_pending()
        #time.sleep(1)
