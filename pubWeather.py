#!/usr/bin/env python3
import json
from yr.libyr import Yr
import paho.mqtt.client as mqtt
from datetime import datetime
import dateutil.parser
import requests
import argparse
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument('-tanaman', action='store_true')
parser.add_argument('-lampu', action='store_true')
parser.add_argument('-pendingin', action='store_true')
args = parser.parse_args()

def extractTime(isodatestring):
    thisDate=dateutil.parser.parse(isodatestring)
    return(thisDate.time())

def extractDate(isodatestring):
    thisDate=dateutil.parser.parse(isodatestring)
    return(thisDate.date())
    

def main():
    
    while True:
        if args.tanaman:
            def on_publish_plant(client, userdata, mid):    
                print("mid: "+str(mid))

            client = mqtt.Client()
            client.on_publish = on_publish_plant


            client.username_pw_set("username","password")
            client.connect("broker.hivemq.com", 1883, 60)
            client.loop_start()
            lokasi = input("Masukan Lokasi yang ingin di prediksi cuacanya: ")
            
            # perulangan untuk mengirimkan data (publish) ke mqtt broker setiap detik
            while True:
                weather = Yr(location_name=lokasi, forecast_link='forecast_hour_by_hour')
                currentWeather = weather.now()
                minTemp=int(currentWeather['temperature']['@value'])
                maxTemp=int(currentWeather['temperature']['@value'])
                maxRain=float(currentWeather['precipitation']['@value'])
                
                
                tempMin = "Minimum Temperatur : " + str(minTemp)
                tempMax = "Maksimum Temperatur : " + str(maxTemp)
                rainMax = "Curah Hujan : " + str(maxRain)
                if maxRain < 0.5:
                    condition = "Siram Tanaman"
                if maxRain > 0.5:
                    condition = "Jangan Siram Tanaman"                
                
                client.publish("/temperatur_minimum",tempMin, qos=1)
                time.sleep(1)
                client.publish("/temperatur_maksimum",tempMax, qos=1)
                time.sleep(1)
                client.publish("/curah_hujan",rainMax, qos=1)
                time.sleep(1)
                client.publish("/kondisi_alat_siram",condition,qos=1)
                time.sleep(2)

        if args.lampu:
            def on_publish_light(client, userdata, mid):    
                print("mid: "+str(mid))

            client = mqtt.Client()
            client.on_publish = on_publish_light


            client.username_pw_set("username","password")
            client.connect("broker.hivemq.com", 1883, 60)
            client.loop_start()
            lokasi = input("Masukan Lokasi yang ingin di prediksi cuacanya: ")
            
            # perulangan untuk mengirimkan data (publish) ke mqtt broker setiap detik
            while True:
                weather = Yr(location_name=lokasi, forecast_link='forecast_hour_by_hour')
                currentWeather = weather.now()
                sunRise=extractTime(weather.dictionary['weatherdata']['sun']['@rise']).strftime("%H:%M")
                sunSet=extractTime(weather.dictionary['weatherdata']['sun']['@set']).strftime("%H:%M")
                today = datetime.now()
                timeToday = today.strftime("%H:%M")
                for forecast in weather.forecast():
                    condition = forecast['symbol']['@name']
                
                
                Risesun = "Matahari Terbit : " + str(sunRise)
                Setsun = "Matahari Terbenam : " + str(sunSet)
                timenow = "Waktu Sekarang : " + str(timeToday)
                conditionNow = "Kondisi Cuaca : " + str(condition)

                if Setsun > timeToday > sunRise and conditionNow != 'Cloudy' or conditionNow != 'Rain' or conditionNow != 'Heavy rain showers' :
                    condition = "Lampu Dimatikan"
                if Setsun < timeToday < sunRise and conditionNow != 'Cloudy' or conditionNow != 'Rain' or conditionNow != 'Heavy rain showers':
                    condition = "Lampu Dihidupkan"
                if Setsun > timeToday > sunRise and conditionNow == 'Cloudy' or conditionNow == 'Rain' or conditionNow == 'Heavy rain showers' :
                    condition = "Lampu Dimatikan"
                if Setsun < timeToday < sunRise and conditionNow == 'Cloudy' or conditionNow == 'Rain' or conditionNow == 'Heavy rain showers':
                    condition = "Lampu Dihidupkan"   
                
                client.publish("/matahari_terbit",Risesun, qos=1)
                time.sleep(1)
                client.publish("/matahari_terbenam",Setsun, qos=1)
                time.sleep(1)
                client.publish("/waktu_sekarang",timenow, qos=1)
                time.sleep(1)
                client.publish("/kondisi_sekarang",conditionNow, qos=1)
                time.sleep(1)
                client.publish("/kondisi_alat_lampu",condition,qos=1)
                time.sleep(2)
        
        if args.pendingin:
            def on_publish_cooler(client, userdata, mid):    
                print("mid: "+str(mid))

            client = mqtt.Client()
            client.on_publish = on_publish_cooler


            client.username_pw_set("username","password")
            client.connect("broker.hivemq.com", 1883, 60)
            client.loop_start()
            lokasi = input("Masukan Lokasi yang ingin di prediksi cuacanya: ")
            
            # perulangan untuk mengirimkan data (publish) ke mqtt broker setiap detik
            while True:
                url = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s"
                request = requests.get(url % (lokasi,'057928f69d86a90014a99e9b80269621'))
                response=json.loads(request.text)
                temp = round(response['main']['temp']-273)
                
                
                temperatur = "Suhu : " + str(temp)
                
                if temp >= 30:
                    condition = "Pendingin Dihidupkan"
                if 30 >= temp >= 21: 
                    condition = "Pendingin Dihidupkan" 
                if temp <= 21:
                    condition = "Pendingin Dimatikan"   
                
                client.publish("/temperatur",temperatur, qos=1)
                time.sleep(1)
                client.publish("/kondisi_alat_pendingin",condition,qos=1)
                time.sleep(2)

          
if __name__=='__main__':
    main()

