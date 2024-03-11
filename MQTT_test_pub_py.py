#!usr/bin/env python
# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
from time import sleep              # ウェイトのために使う
import json

ROBOT_ID="RMS-1000-AAH46"
ROBOT_IP_ADDRESS="192.168.212.1"
ROBOT_PORT_NUM="1883"
ROBOT_PORT_NUM=int(ROBOT_PORT_NUM)

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))
  client.subscribe(f"0/WHISPERER/{ROBOT_ID}/battery")

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, rc):
  if rc != 0:
     print("Unexpected disconnection.")

# publishが完了したときの処理
def on_publish(client, userdata, mid):
  # print("publish: {0}".format(mid))
  pass

# メイン関数   この関数は末尾のif文から呼び出される
def main():
  client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
  client.on_connect = on_connect         # 接続時のコールバック関数を登録
  client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
  client.on_publish = on_publish         # メッセージ送信時のコールバック
  client.username_pw_set("mqtt", "sI7G@DijuY")
  client.connect(ROBOT_IP_ADDRESS, ROBOT_PORT_NUM, 60)  # 接続先はロボット
  sleep(1)# 1秒待つ

  # 通信処理スタート
  client.loop_start()    # subはloop_forever()だが，pubはloop_start()で起動だけさせる
  sleep(1)# 1秒待つ

  client.publish(topic=f"0/THOUZER_HW/'{ROBOT_ID}'/exec/cmd", payload=json.dumps({"app":"app-whisperer"}))    # トピック名とメッセージを決めて送信
  print("start")
  print("running")
  try:
  # 永久に繰り返す
    while True:
        client.publish(topic=f"0/WHISPERER/'{ROBOT_ID}'/nav", payload=json.dumps({"v_mps":"0","w_degps":"0"}))    # v_mps:{"min":0.052}? # 最高速度と最高角速度を設定．道中に障害物がある場合も停止せず動く
        # client.publish(topic=f"0/WHISPERER/'{ROBOT_ID}'/nav", payload=json.dumps({"x_m":"1","y_m":"1"}))    # 現在のポジションを(0,0)として任意の座標へ移動．速度は自動設定．道中に障害物がある場合停止
        # client.publish(topic=f"0/WHISPERER/'{ROBOT_ID}'/nav", payload=json.dumps({"distance_m":"1","direction_deg":"0"}))    # 距離と角度を設定し移動．速度は自動設定．道中に障害物がある場合避けて移動
        sleep(1)# 1秒待つ
  except:
    client.publish(topic=f"0/THOUZER_HW/'{ROBOT_ID}'/exec/cmd", payload=json.dumps({"app":""}))    # トピック名とメッセージを決めて送信
    print("end")

if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
  main()    # メイン関数を呼び出す
  
  
