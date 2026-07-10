# RaspberryPi_study Directory

## 📌 目的 (Objective)
千葉県立船橋テクノスクールにおける「Pythonプログラミング・IoT開発・Linuxインフラ構築」の学習記録コードを格納するディレクトリです。

## 🛠 学習している技術スタック (Tech Stack)
*   **Languages:** Python 3, HTML/CSS,
*   **OS & Infrastructure:** Linux (Raspberry Pi OS Bookworm), VNC, SSH
*   **Libraries/Frameworks:** Flask, BeautifulSoup4, RPi.GPIO, smbus2, urllib, re, subprocess
*   **Hardware/Sensors:** Raspberry Pi 5, I2C接続センサー (DHT20, BME280等), カメラモジュール
*   **External Tools:** mjpg-streamer, AquesTalkPi, Ambient (IoTデータ可視化)

## 📁 格納している主な学習記録

### 1. 監視カメラ・簡易Webページ (`/templates/04_02_scamera.py` など)
Flaskを用いてRaspberry Pi上にWebサーバーを構築し、ブラウザからハードウェアを操作するシステムの実装記録です。
*   `subprocess` モジュールを使用し、カメラストリーミング (`mjpg-streamer`) や音声合成 (`AquesTalkPi`) のコマンドをPythonから呼び出す処理を実装しています。
*   `smbus2` を用いて温湿度センサー (DHT20) から生のバイナリデータを取得し、ビット演算によって数値を復元する処理を試しました。

### 2. Webスクレイピングの学習記録
BeautifulSoup4と正規表現(`re`)などを組み合わせたデータ抽出のプログラム群です。
*   HTMLのツリー構造から特定のタグや属性(`href`, `src`)を抽出する練習を行っております。
*   取得先のサーバーに負荷をかけないための待機処理（`time.sleep`）や、User-Agentの記述など、相手方へ配慮した実装を心掛けております。

### 3. 植物の環境記録システム (開発中)
温湿度や土壌水分などの環境データを定期取得し、ローカルのCSVファイルへの記録、およびクラウドサービス (Ambient) へ自動送信してグラフ化するIoTシステムの実装に取り組んでいます。
