import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import tweepy
from requests.exceptions import ConnectionError
import schedule
import settings

class Tweet_bot:
    def __init__(self):
        pass

    def Tweet(self,text):
        # Twitterオブジェクトの生成
        consumer_key = settings.ck
        consumer_secret = settings.cs
        access_token = settings.at
        access_token_secret = settings.ats
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth,wait_on_rate_limit = True)
        api.update_status(text)

    def set_driver(self, driver_path, headless_flg):
        # Chromeドライバーの読み込み
        options = ChromeOptions()

        # ヘッドレスモード（画面非表示モード）をの設定
        if headless_flg == True:
            options.add_argument('--headless')

        # 起動オプションの設定
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
        # options.add_argument('log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--incognito')          # シークレットモードの設定を付与

        # ChromeのWebDriverオブジェクトを作成する。
        driver_path = ChromeDriverManager().install()
        return Chrome(driver_path,options=options)

    def main(self):
        url_list = []
        url = "https://www.amazon.co.jp/%E3%82%B7%E3%83%A3%E3%83%BC%E3%83%97-SHARP-SJ-AF50G-R-%E3%83%97%E3%83%A9%E3%82%BA%E3%83%9E%E3%82%AF%E3%83%A9%E3%82%B9%E3%82%BF%E3%83%BC-%E3%82%B0%E3%83%A9%E3%83%87%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%AC%E3%83%83%E3%83%89/dp/B08KJ85RJ5?ref_=fspcr_pl_dp_2_2272928051"
        date = datetime.datetime.now()
        # driverを起動
        if os.name == 'nt': #Windows
            driver = self.set_driver("chromedriver.exe", False)
        elif os.name == 'posix': #Mac
            driver = self.set_driver("chromedriver", False)
        # Webサイトを開く
        driver.get(url)
        product_name = driver.find_elements_by_id("productTitle")
        add_cart_button = driver.find_elements_by_id("add-to-cart-button")
        print(len(add_cart_button))
        with open('amazon.txt', "r") as f:
            lines = f.readlines()
        for line in lines:
            a = line.strip('\n')
            url_list.append(a)
        if url in url_list:
            if len(add_cart_button) >= 1:
                print('商品在庫あり(ツイートなし)')
                self.Tweet(f"{date}:{product_name[0].text}の在庫はあります") #問６の場合はツイートする　問5の場合はツイートしない
            else:
                print('商品の在庫はありません。')
                self.Tweet(f"{date}:{product_name[0].text}の在庫はありません") #問5の場合はツイートする 問6の場合はツイートしない
        elif url not in url_list:
            try:
                if len(add_cart_button) >= 1:
                    print('商品の在庫はあります(ツイートあり)')
                    self.Tweet(f"{date}:{product_name[0].text}の在庫はあります")
                    with open('amazon.txt','a') as f:
                        f.write(url + '\n')
                else:
                    print('商品の在庫はありません。')
                    self.Tweet(f"{date}:{product_name[0].text}の在庫はありません")
            except ConnectionError:
                print('エラーが発生しました。')
        
    def roop(self):
        schedule.every(1).minutes.do(self.main)
        while True:
            schedule.run_pending()
            time.sleep(1)

def main():
    twiiter = Tweet_bot()
    twiiter.roop()


if __name__ == "__main__":
    main()