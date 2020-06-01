import requests
from schedule import Scheduler
import time
import threading

url_usd = 'https://free.currconv.com/api/v7/convert?q=USD_GEL&compact=ultra&apiKey=99fc939d3d1ffea41bee'
url_eur = 'https://free.currconv.com/api/v7/convert?q=EUR_GEL&compact=ultra&apiKey=99fc939d3d1ffea41bee'
url_gbp = 'https://free.currconv.com/api/v7/convert?q=GBP_GEL&compact=ultra&apiKey=99fc939d3d1ffea41bee'

usd_gel = None
eur_gel = None
gbp_gel = None

def run_continuously(self, interval=300):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously
def pr():
    global usd_gel
    global eur_gel
    global gbp_gel
    try:
        usd_gel = requests.get(url_usd).json()
        usd_gel = round(usd_gel['USD_GEL'], 3)
        eur_gel = requests.get(url_eur).json()
        eur_gel = round(eur_gel['EUR_GEL'], 3)
        gbp_gel = requests.get(url_gbp).json()
        gbp_gel = round(gbp_gel['GBP_GEL'], 3)
        print('CURRENCIES UPDATED! USD - GEL ' + str(usd_gel) + 'EUR - GEL ' + str(eur_gel) + 'GBP - GEL ' + str(gbp_gel))

    except Exception as err:
        print(f'Other error occurred: {err}')

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().second.do(pr)
    scheduler.run_continuously()


start_scheduler()