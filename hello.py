from flask import Flask, render_template
from flask import jsonify
import urllib.request
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

app = Flask(__name__)
# app.debug = True
@app.route('/')
def render_index():
   return render_template("index.html")

@app.route('/api/playbyplay/<game_id>')
def fetchPlaybyPlay(game_id):
    print("get here")
    print(game_id)
    url = f"http://stats.nba.com/stats/playbyplayv2/?GameID={game_id}&StartPeriod=1&EndPeriod=14"
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'stats.nba.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    req = urllib.request.Request(url, b"", headers)

    contents = requests.get(url, headers = headers) # urllib.request.urlopen(req)

    dictionary = json.loads(contents.text)
    return jsonify(dictionary)

@app.route('/api/highlights/<game_id>/<event_id>')
def fetchHighlights(game_id, event_id):
    #/api/highlights/0021700833/4
  #let highlightURL = await grabHighlight(0021700833, 4);
    chrome_exec_shim = os.environ.get("GOOGLE_CHROME_SHIM", "chromedriver")
    driver = webdriver.Chrome(executable_path=chrome_exec_shim)
    driver.implicitly_wait(60)
    print("searching")
    driver.get(f"https://stats.nba.com/events/?flag=1&GameID={game_id}&GameEventID={event_id}&Season=2017-18&sct=plot")
    video = driver.find_element_by_id("statsPlayer_embed_statsPlayer")
    print("found video")
    src = video.get_attribute("src")
    # time.sleep(2)
    while (src == "" or src == 'https://s.cdn.turner.com/xslo/cvp/assets/video/blank.mp4'):
        print("looking for source")
        src = video.get_attribute('src')
    driver.quit();

    return src;



@app.route('/api/games/<date>')
def fetchGames(date):
    print(f"http://data.nba.net/10s/prod/v1/2018{date}/scoreboard.json")
    contents = urllib.request.urlopen(f"http://data.nba.net/10s/prod/v1/2018{date}/scoreboard.json").read()
    dictionary = json.loads(contents)
    return jsonify(dictionary)




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 33507))
    app.run(host='0.0.0.0', port=port)
