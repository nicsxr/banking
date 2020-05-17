import schedule
import time
import urllib.request

url_usd = 'https://api.businessonline.ge/api/rates/nbg/usd'
url_eur = 'https://api.businessonline.ge/api/rates/nbg/eur'
url_gbp = 'https://api.businessonline.ge/api/rates/nbg/gbp'

usd_gel = 0
eur_gel = 0
gbp_gel = 0

def update():
    usd_gel = urllib.request.urlopen(url_usd).read()
    eur_gel = urllib.request.urlopen(url_eur).read()
    gbp_gel = urllib.request.urlopen(url_gbp).read()

schedule.every().hour.do(update)

while True:
    schedule.run_pending()
    time.sleep(1) 