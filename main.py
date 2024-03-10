from datetime import datetime
import requests
import time
import config


def main():
    while True:
        todayDate = datetime.now().strftime('%d.%m.%Y')
        symbolAndPriceList = requests.get(f"{config.URL}?symbol={config.SYMBOL}")
        
        if symbolAndPriceList.status_code == 200:
            nowPrice = float(symbolAndPriceList.json()['price'])
            result = f"{config.SYMBOL}: {nowPrice}"
            
            try: # Если файл существует, то посчитает процент от полседней цены
                with open(f"{todayDate} {config.SYMBOL}.txt", 'r', encoding='utf-8') as file:
                    fileText = file.read()
                    file.close()

                LastPriceSymbol = float(fileText.split('*')[-2].split()[1]) # Получение последней цены из файла
                procent = round(100 * (nowPrice - LastPriceSymbol) / LastPriceSymbol, 4) # Сравнение настоящей цены с последней
                result += f' {procent}% *\n'
                print(result)

                with open(f"{todayDate} {config.SYMBOL}.txt", 'w', encoding='utf-8') as file: # Запись настоящей цены в файл
                    file.write(str(fileText) + str(result))
                    file.close()
            except BaseException: # Если файла нет, то создаст его
                result += ' | +0% *\n'
                with open(f"{todayDate} {config.SYMBOL}.txt", 'w', encoding='utf-8') as file:
                    file.write(result)
                    file.close()
        else:
            print(f"{config.ERROR_MESSAGE} | {symbolAndPriceList.text}")

        time.sleep(config.TIMEOUT)


main()
