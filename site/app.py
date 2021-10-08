'''

Предсказатель в определённое время анализирует тикеры из файла "ticker.json" и
создаёт прогнозы, после чего выгружает и их в базу данных, конфинурация которой
записана в файле "config.json", который директорией выше

Важно: тикеры цену которых по какой-то причине нельзя прогнозировать пропускаются и
не отображаются на сайте. В логах можно найти подробную информацию, они же хранятся на
момент написания этой документации по пути "/var/log/forecastsite/visor.out.log" и там
же "visor.err.log" с логами ошибок.

(c) Lamas's group 

Телефон:        +90-539-240-5639
Почта:          nsit2002@gmail.com

'''

from flask import Flask,request,render_template,redirect

from datetime import date
import json
import random
import pymysql.cursors

from objects.mybuiltins import ticker_data_generator, get_home, get_ticker, socket

app = Flask(__name__)

with open("../config.json") as file:
        CONFIG = json.loads(file.read())
with open("dates.json") as file:
        DATES = json.loads(file.read())

database = pymysql.connect(
        host = CONFIG['host'],
        user = CONFIG['user'],
        password = CONFIG['password'],
        database = CONFIG['database'],
        cursorclass = pymysql.cursors.DictCursor
)
cursor = database.cursor()

# Домашняя страница
@app.route("/")
@app.route("/home")
def home():
        pattern = None
        search = False
        if request.args.get("s"):
                pattern = request.args.get("s")
                search = True
        data = get_home(cursor,pattern=pattern)
        return render_template(
                'index.html',
                data=data,
                search=search,
                pattern=pattern,
                date=date.today()
        )

# Страница прогнозов тикера
@app.route("/ticker_<ticker>")
def ticker(ticker):
        data = get_home(cursor)
        ticker_data = get_ticker(cursor,ticker)

        try:
                ticker_data = ticker_data[0]
                ticker_data = ticker_data_generator(ticker_data)
        except:
                return redirect("/")

        return render_template(
                'ticker.html',
                data=data,
                date=date.today(),
                random_forecasts=random.choices(data,k=5),
                ticker_data=ticker_data,
                DATES = DATES,
        )


if __name__ == "__main__":
        with database:
                with database.cursor() as cursor:
                        app.run(debug=True)