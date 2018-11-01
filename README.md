# Chatbot_Line_cc103
先

git clone https://github.com/iii-cutting-edge-tech-lab/Chatbot_Line_cc103.git

cd Chatbot_Line_cc103

開啟環境流程(只供開發使用，只開啟jupyter、ngrok、Redis的container，要再開出Chatbot_Dev環境才有五台container，Line server才能連動)

docker-compose up -d

透過瀏覽器訪問jupyter
http://本機ip:8888

程式碼都放在code內，可以用Jupyter編輯

要特別注意，要開出Chatbot_Dev環境才有五台container，Line server才能連動
ngrok server 有一個uri 要填入line@帳號管理界面中，否則Line server收不到line用戶端傳來的封包
詳情請去看dropbox paper
https://paper.dropbox.com/doc/Line--AN464_05O3RLSljySjwdJdBSAg-bPvrgUXIEdeYix5uKvP9k

底下是這個repo的資料夾結構

code/

#製作menu_id的程式碼
menu_id.ipynb
#運行line bot server的程式碼
app.ipynb
#方便devops啟動轉成py
app.py
#裝一些要呼叫的重要變數
secret_key

/mockapi #裝mockapi的程式碼

mockAPIserver.py #運行mockAPI的程式碼

/redis/data #讓redis鏡像裝data的資料夾

...

README.md # 一個說明文字檔

docker-compose.yml #裝了所有的環境所需

/dockerfile

#製作redis server要的image
dockerfile-redis
#製作ngrok server要的image
dockerfile-ngrok
#製作linebot server要的image
dockerfile-jupyter
#製作mockapi要的image
dockerfile-mockapi
