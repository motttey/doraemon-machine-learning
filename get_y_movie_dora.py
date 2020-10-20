import requests
from bs4 import BeautifulSoup

url_base = "https://movies.yahoo.co.jp/movie"
def get_rating(movie_url_list):
    for movie_url in movie_url_list:
        r = requests.get(url_base + movie_url)
        bs = BeautifulSoup(r.text, "html.parser")

        mv_div = bs.find("div", {"id": "mv"})
        mv_data = mv_div.find("div", {"class": "movie_data"})
        rader_label = mv_data.find("canvas", {"class": "rader-chart__figure"})

        print(rader_label.get("data-chart-label"))
        print(rader_label.get("data-chart-val-total"))
    return

def get_movies():
    movie_url_list = []

    for i in range(10):
        print(i)
        params = {
          "query" : "ドラえもん",
          "page" : i,
        }
        r = requests.get(url_base, params=params)
        if r.text == requests.codes.ok:
            break;
        bs = BeautifulSoup(r.text, "html.parser")

        movies = bs.findAll("div", {"class": "thumbnail__caption"})
        for movie in movies:
            m_url = movie.find("a").get("href")
            title = movie.find("h3").get("title")

            movie_url_list.append(m_url)
            print(title)
    return movie_url_list

if __name__ == "__main__":
    movie_url_list = get_movies()
    get_rating(movie_url_list)
