import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    Login = os.getenv('LOGIN')  # Адрес электронной почты, указанный при регистрации на сайте moex.com
    Password = os.getenv('PASSWORD')  # Пароль от учетной записи на сайте moex.com
