import requests
from bs4 import BeautifulSoup

def get_movies():
    url = "https://movies.yahoo.co.jp/movie/"

    for i in range(10):
        print(i)
        params = {
          "query" : "ドラえもん",
          "page" : i,
        }
        r = requests.get(url, params=params)
        if r.text == requests.codes.ok:
            break;
        bs = BeautifulSoup(r.text, "html.parser")

        movies = bs.findAll("div", {"class": "thumbnail__caption"})
        for movie in movies:
            m_url = movie.find("a").get("href")
            title = movie.find("h3").get("title")

            print(m_url)
            print(title)

if __name__ == "__main__":
    get_movies()
