#!usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
from time import sleep              # ウェイトのために使う
import json

ROBOT_ID="RMS-1000-AAH46"
ROBOT_IP_ADDRESS="192.168.212.1"
ROBOT_PORT_NUM="1883"
ROBOT_PORT_NUM=int(ROBOT_PORT_NUM)

# サーバーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))
  # client.subscribe(f"0/WHISPERER/{ROBOT_ID}/vel2D_DWO")
  # client.subscribe(f"0/WHISPERER/{ROBOT_ID}/battery")
  client.subscribe(f"0/WHISPERER/{ROBOT_ID}/pos2D_DWO")

# 切断したときの処理
def on_disconnect(client, userdata, rc):
  if rc != 0:
     print("Unexpected disconnection.")

def on_message(client, userdata, msg):
  # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
  print(f"Received message ':{str(msg.payload)}")

# メイン関数   この関数は末尾のif文から呼び出される
def main():
  client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
  client.on_connect = on_connect         # 接続時のコールバック関数を登録
  client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
  client.on_message = on_message         # メッセージ受信時のコールバック
  client.username_pw_set("mqtt", "sI7G@DijuY")
  client.connect(ROBOT_IP_ADDRESS, ROBOT_PORT_NUM, 60)  # 接続先はロボット

  # 通信処理スタート
  client.loop_forever()    # subはloop_forever()だが，pubはloop_start()で起動だけさせる
  sleep(1)# 1秒待つ

if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
  main()    # メイン関数を呼び出す
  
  
