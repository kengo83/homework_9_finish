import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'touch .env')
load_dotenv(dotenv_path)

ck = os.environ.get("consumer_key") # 環境変数の値をckに代入
cs = os.environ.get("consumer_secret")
at = os.environ.get("access_token")
ats = os.environ.get("access_token_secret")