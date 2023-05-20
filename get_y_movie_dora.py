import requests
import json
from bs4 import BeautifulSoup

url_base = "https://movies.yahoo.co.jp"
def get_rating(movie_url_list):
    movie_rating_list = []
    for movie_url in movie_url_list:
        movie_rating = {}

        r = requests.get(url_base + movie_url)
        bs = BeautifulSoup(r.text, "html.parser")

        mv_div = bs.find("div", {"id": "mv"})
        mv_data = mv_div.find("div", {"class": "movie_data"})
        movie_title = mv_div.find("h1").find("span").text

        rader_label = mv_data.find("canvas", {"class": "rader-chart__figure"})

        chart_label = rader_label.get("data-chart-label").split(",")
        chart_val = rader_label.get("data-chart-val-total").split(",")

        movie_rating["title"] = movie_title
        movie_rating["rate"] = {}
        for lavel, val in zip(chart_label, chart_val):
            movie_rating["rate"][lavel] = float(val) if val != '' else 0

        movie_rating_list.append(movie_rating)
    return movie_rating_list

def get_movies():
    movie_url_list = []

    for i in range(10):
        print(i)
        params = {
          "query" : "ドラえもん",
          "page" : i,
        }
        r = requests.get(url_base + '/find', params=params)
        if r.text == requests.codes.ok:
            break;
        bs = BeautifulSoup(r.text, "html.parser")

        movies = bs.findAll("div", {"class": "riff-mt-3"})
        for movie in movies:
            if (movie.find("a") is None): continue
            m_url = movie.find("a").get("href")
            title = movie.find("a").get_text()

            movie_url_list.append(m_url)
            print(m_url)
            print(title)
    return movie_url_list

if __name__ == "__main__":
    movie_url_list = get_movies()
    movie_rating_list = get_rating(movie_url_list)
    print(movie_rating_list)

    with open("dora_movies.json", "w", encoding= "utf-8") as f:
        f.write(json.dumps(movie_rating_list))
