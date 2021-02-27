"""
This script is used to create models
Author:
Date: 11/02/2021

"""
import requests
from requests.exceptions import HTTPError
from core.celery import app
from records.models import Record, RecordHistory
import cfscrape
from django.utils import timezone
import datetime
torport = 9150




@app.task
def add(x, y):
    return x + y

@app.task(bind=True, default_retry_delay=30 * 60)
def send_request_cfscrape(self):
    proxies = {
            'http':"socks5h://tor:{}".format(torport),
            'https':"socks5h://tor:{}".format(torport)
        }
    headers = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0'
        }    
    s = cfscrape.create_scraper()
    s.proxies = proxies
    scraper = cfscrape.create_scraper(sess=s, delay=10)
    try:
        url = 'http://o3shuzjrnpzf2aiq.onion/'
        response = scraper.get(url, headers=headers)
        print(response)
    except requests.ConnectionError as e:
        print("OOPS! Connection error", e)
    except requests.exceptions.RequestException as ec:
        print("OOPS! Request Exception error", ec)
    except Exception as exc:
        print("OOPS! Something bad happened", exc)


@app.task(bind=True, default_retry_delay=60 * 60)
def delete_old_history(self):
    three_days_ago = timezone.now() - datetime.timedelta(days=3)
    RecordHistory.objects.filter(created__lt=three_days_ago).delete()


@app.task(bind=True, default_retry_delay=30 * 60)
def send_request(self):
    try:
        connect_timeout, read_timeout = 300.05, 120.0
        session = requests.Session()
        # session.proxies = {}
        # session.proxies['http'] = 'socks5h://127.0.0.1:9150'
        # session.proxies['https'] = 'socks5h://127.0.0.1:9150'
        proxies = {
            'http':"socks5h://tor:{}".format(torport),
            'https':"socks5h://tor:{}".format(torport)
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:78.0) Gecko/20100101 Firefox/78.0'
        }
        records = Record.objects.all()

        for rec in records:
            try:
                onion = session.get(rec.url,timeout=(connect_timeout, read_timeout),proxies=proxies, headers=headers)
                onion_resp = onion.status_code
                print(onion_resp)
                hist_obj = RecordHistory.objects.create(response=onion_resp, record=rec)
                    
            except requests.exceptions.ConnectionError as errc: 
                print("An Connection Error occurred:", errc)
                onion_resp = 666
                hist_obj = RecordHistory.objects.create(response=onion_resp, record=rec)
                continue
            except requests.exceptions.RequestException as errr:
                print("An Request Error occurred:", errr)
                onion_resp = "Request Error occured"
                continue


        # url="https://google.com"
        # url_two="http://matangacepd2bx4e.onion"
        # res = session.get(url, timeout=(connect_timeout, read_timeout))
        # res_two = session.get(url_two, timeout=(connect_timeout, read_timeout),proxies=proxies, headers=headers)
        # res_session = session.get(url, timeout=(connect_timeout, read_timeout))
        # code = res.status_code
        # code_two = res_two.status_code
        # code_session = res_session.ok
        #print(code, code_two)
    except requests.exceptions.HTTPError as errh:
        print("An HTTP Error occurred:", errh)    
    except requests.exceptions.ProxyError as errp:
        print("An Proxy Error occurred:", errp)     
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10 * 60)






 