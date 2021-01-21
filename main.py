from time import sleep
import datetime

from bs4 import BeautifulSoup
import requests
import pandas as pd

def main():
    url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13109&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&\
            shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1&page={}"
    csv = scraping(url)
    make_csv(csv)

def scraping(url):
    d_list = []

    for i in range(3):
        target_url = url.format(i+1)
        print("target_url = " , target_url)

        r = requests.get(target_url)

        if r.status_code == 200:
            print("Conected")
        else:
            print("Not Conected")
            break

        sleep(1)

        soup = BeautifulSoup(r.text)

        contents = soup.find_all('div', class_='cassetteitem')

        for content in contents:
            detail = content.find('div', class_='cassetteitem_content')
            table = content.find('table', class_='cassetteitem_other')

            title = detail.find('div', class_='cassetteitem_content-title').text
            address = detail.find('li', class_='cassetteitem_detail-col1').text
            access = detail.find('li', class_='cassetteitem_detail-col2').text
            age = detail.find('li', class_='cassetteitem_detail-col3').text

            tr_tags = table.find_all('tr', class_='js-cassette_link')

            for tr_tag in tr_tags:        
                floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]

                fee, management_fee = price.find_all('li')
                deposit, gratuity = first_fee.find_all('li')
                madori, menseki = capacity.find_all('li')

                d = {
                    'title': title,
                    'address': address,
                    'access': access,
                    'age': age,
                    'floor': floor.text,
                    'fee': fee.text,
                    'management_fee': management_fee.text,
                    'deposit': deposit.text,
                    'gratuity': gratuity.text,
                    'madori': madori.text,
                    'menseki': menseki.text
                }

                d_list.append(d)
    
    return d_list

def make_csv(list):
    df = pd.DataFrame(list)

    date_now = datetime.datetime.now()

    df.to_csv("suumo_info" + str(date_now.year) + "_" + str(date_now.month) + "_" + str(date_now.day) + "_" + \
               str(date_now.hour) + "_" + str(date_now.minute) + ".csv", index=None, encoding='utf-8-sig')

if __name__ == '__main__':
    main()