from bs4 import BeautifulSoup
import requests
import time
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def find_renas(t_object):

    cnt = 0

    html_text1 = requests.get(f'https://www.conforama.pt/decoracao/objectos-de-decoracao').text

    soup1 = BeautifulSoup(html_text1,'lxml')
        
    spans = soup1.find_all('span', class_ = 'to')
    page_number = int(spans[1].text)

    for i in range(page_number):

        html_text = requests.get(f'https://www.conforama.pt/decoracao/objectos-de-decoracao?page={i}').text

        soup = BeautifulSoup(html_text,'lxml')

        renas = soup.find_all('div', class_ = 'product-container-wrapper')

        for index, rena in enumerate(renas):
            
                description = rena.find('h2', class_ = 'product-title').text.strip().lower()
        
                if t_object in description:

                    price = rena.find('div', class_ = 'selling-price').text.strip()
                    
                    link = rena.a['href']

                    with open(f'Searches/File_{index}_page_{i}.txt','w') as f:

                        f.write(f'''Conforama has the product {description}\nwith the price {price} rena\nwith the ulr {link}
                        ''')
                    
                    cnt = cnt + 1

                    if cnt == 1:

                        message = Mail(
                            from_email='luis.filipe.sf@gmail.com',
                            to_emails='luis.filipe.sf@gmail.com',
                            subject='Encontrei uma rena!',
                            html_content=f'''<strong>Conforama has the product {description}\nwith the price {price} rena\nwith the ulr {link}</strong>''')

                        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

                        response = sg.send(message)

                    print(f'File_{index}_page_{i}.txt saved!')


if __name__ == '__main__':

    print('Put some object that you want to find:')
    the_object = input('>').lower()

    #while True:

    find_renas(the_object)
        #print('Waiting for next search')
        #time_wait = 100
        #time.sleep(time_wait)