from flaskblog import app  

if __name__ == '__main__':  # 確保程式只有在直接執行時才會啟動伺服器
    app.run(debug=True)  # 啟動 Flask 內建的開發伺服器
