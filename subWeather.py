#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import requests
import argparse
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument('-tanaman', action='store_true')
parser.add_argument('-lampu', action='store_true')
parser.add_argument('-pendingin', action='store_true')
args = parser.parse_args()



def main():
    
    while True:
        if args.tanaman:


            # fungsi yang dipanggil pertama untuk melakukan subscribe ke mqtt broker
            def on_subscribe_plant(client, userdata, mid, granted_qos):
                print("Subscribed: "+str(mid)+" "+str(granted_qos))

            # fungsi yang bertujuan untuk menampilkan data yang berhasil diterima subscriber
            def on_message_plant(client, userdata, msg):
                print(str(msg.payload))


            client = mqtt.Client()
            client.on_subscribe = on_subscribe_plant
            client.on_message = on_message_plant

            # client.username_pw_set("username","password")
            client.connect("broker.hivemq.com", 1883, 60)
            client.subscribe([("/temperatur_minimum",1),("/temperatur_maksimum",1),("/curah_hujan",1),("/kondisi_alat_siram",1)],qos=2)
            client.loop_forever()
        
        if args.lampu:


            # fungsi yang dipanggil pertama untuk melakukan subscribe ke mqtt broker
            def on_subscribe_lamp(client, userdata, mid, granted_qos):
                print("Subscribed: "+str(mid)+" "+str(granted_qos))

            # fungsi yang bertujuan untuk menampilkan data yang berhasil diterima subscriber
            def on_message_lamp(client, userdata, msg):
                print(str(msg.payload))


            client = mqtt.Client()
            client.on_subscribe = on_subscribe_lamp
            client.on_message = on_message_lamp

            # client.username_pw_set("username","password")
            client.connect("broker.hivemq.com", 1883, 60)
            client.subscribe([("/matahari_terbit",1),("/matahari_terbenam",1),("/waktu_sekarang",1),("/kondisi_sekarang",1),("/kondisi_alat_lampu",1)],qos=2)
            client.loop_forever()
        
        if args.pendingin:


            # fungsi yang dipanggil pertama untuk melakukan subscribe ke mqtt broker
            def on_subscribe_cooler(client, userdata, mid, granted_qos):
                print("Subscribed: "+str(mid)+" "+str(granted_qos))

            # fungsi yang bertujuan untuk menampilkan data yang berhasil diterima subscriber
            def on_message_cooler(client, userdata, msg):
                print(str(msg.payload))


            client = mqtt.Client()
            client.on_subscribe = on_subscribe_cooler
            client.on_message = on_message_cooler

            # client.username_pw_set("username","password")
            client.connect("broker.hivemq.com", 1883, 60)
            client.subscribe([("/temperatur",1),("/kondisi_alat_pendingin",1)],qos=2)
            client.loop_forever()
        
       
          
if __name__=='__main__':
    main()

