from flask import Flask, render_template, request, redirect
from datetime import datetime
import requests
from PIL import Image
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///forecast.db")

api_key = "3153108bd453dec78b9b437165cdb88c"

def date_conversion(date):
    today_date = datetime.fromtimestamp(date)
    today_date = today_date.strftime('%m-%d-%Y')
    return today_date

def get_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)
    if(response.status_code == 404):
        return "error"
    data = response.json()
    return data
def get_longrange_data(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)
    if(response.status_code == 404):
        return "error"
    data = response.json()
    return data

def hour_month_conversion(date):
    today_time = datetime.fromtimestamp(date)
    today_time = today_time.strftime(' %m-%d %I %p')
    return today_time


def standard_time_conversion(time):
      time = datetime.fromtimestamp(time)
      formatted_time = time.strftime('%I:%M %p')
      return formatted_time



def time_conversion(date):
    today_time = datetime.fromtimestamp(date)
    today_time = today_time.strftime('%H:%M:%S')
    return today_time

def weather_logo(sunrise_time, time, sunset_time, main_forecast):
    if(sunrise_time < time <= sunset_time and main_forecast == "Clear"):
         logo = "static/sun.png"
    elif (main_forecast == "Thunderstorm"):
            logo = "static/thunderstorm.png"
    elif (main_forecast == "Drizzle"):
            logo = "static/drizzle.png"
    elif (main_forecast == "Rain"):
            logo = "static/heavy-rain.png"
    elif (main_forecast == "Snow"):
            logo = "static/snowy.png"
    elif (main_forecast == "Atmosphere"):
            logo = "static/atmosphere.png"
    elif (main_forecast == "Clouds"):
            logo = "static/clouds.png"
    else:
          logo = "static/full-moon.png"

    return logo





@app.route("/")
def index():
    return render_template("index.html")


@app.route("/weather")
def weather():
    city_name = request.args.get("city")
    if(city_name == ""):
         return redirect("/")
    city_data = get_weather_data(city_name)

    if(city_data == "error"):
        return redirect("/")

    city_longrange_data = get_longrange_data(city_name)
    if(city_longrange_data == "error"):
        return redirect("/")
    print(city_longrange_data)

    temperature = round(city_data["main"]["temp"])
    feels_like = round(city_data["main"]["feels_like"])
    wind_speed = round(city_data["wind"]["speed"])
    date = date_conversion(city_data["dt"])
    time = time_conversion(city_data["dt"])
    sunrise_time = time_conversion(city_data["sys"]["sunrise"])
    sunset_time = time_conversion(city_data["sys"]["sunset"])
    sunrise = standard_time_conversion(city_data["sys"]["sunrise"])
    sunset = standard_time_conversion(city_data["sys"]["sunset"])
    icon_code = city_data["weather"][0]["icon"]
    main_forecast = city_data["weather"][0]["main"]
    forecast = city_data["weather"][0]["description"]
    humidity = city_data["main"]["humidity"]
    visibility = round(float(city_data["visibility"]) * 0.000621371, 2)
    pressure = round(float(city_data["main"]["pressure"]) * 0.029529983071445, 2)
    cloudiness = city_data["clouds"]["all"]

    for i in range(1, 41, 1):
         db.execute("INSERT INTO forecast (date, temperature, description, precipitation, wind_speed, icon_code) VALUES (NULL, NULL, NULL, NULL, NULL, NULL)")
    for i in range(1, 41, 1):
        db.execute(
            "UPDATE forecast SET date = ?, temperature = CAST(ROUND(?) AS INTEGER), description=?, precipitation=?, wind_speed=?, icon_code=?  WHERE id = ?",
            city_longrange_data["list"][i-1]["dt"],
            (city_longrange_data["list"][i-1]["main"]["temp"]),
            city_longrange_data["list"][i-1]["weather"][0]["description"],
            int(city_longrange_data["list"][i-1]["pop"]* 100),
            round(city_longrange_data["list"][i-1]["wind"]["speed"]),
            city_longrange_data["list"][i-1]["weather"][0]["icon"],
            i
    )
    db.execute("DELETE FROM forecast WHERE date IS NULL")

    future_data = db.execute("SELECT * FROM forecast")
    for row in future_data:
        row["date"] = hour_month_conversion(int(row["date"]))
        row["temperature"] = int(row["temperature"])
        row["wind_speed"] = int(row["wind_speed"])



    return render_template("weather.html", city_name=city_name, temperature=temperature, feels_like=feels_like,
                           wind_speed=wind_speed, date=date, icon_code=icon_code, forecast=forecast,
                           sunrise=sunrise, sunset=sunset, humidity=humidity, visibility=visibility, pressure=pressure,
                           cloudiness=cloudiness, future_data=future_data)



