import requests
import psycopg2
import concurrent.futures
import threading
from pytube import YouTube


def get_service(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for dataout in data["results"]:
            pokemon = dataout["name"]
            write_db(pokemon)
    else:
        print(response.status_code)


def service_videos(link):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(get_videos, link)


def get_videos(link):
    video = YouTube(link)
    video.streams.filter(
        file_extension='mp4').get_by_itag(18).download()


def connect_db():
    try:
        connect = psycopg2.connect(
            "dbname=postgres user=postgres password=qwerty123")
        cur = connect.cursor()
        connection = [connect, cur]
        return connection
    except psycopg2.Error as error:
        print(error)


def write_db(pokemon):
    connection[1].execute(
        "INSERT INTO pokemons (name) VALUES (%(usr)s)", {"usr": pokemon})
    connection[0].commit()


if __name__ == "__main__":
    connection = connect_db()
    link = ["https://www.youtube.com/watch?v=4t91S0Cfl-4",
            "https://www.youtube.com/watch?v=20Ry1dxqxOg",
            "https://www.youtube.com/watch?v=KHV79cF0JKc",
            "https://www.youtube.com/watch?v=haujoh19QVk",
            "https://www.youtube.com/watch?v=k489L7IReiA"]
    url = "https://pokeapi.co/api/v2/pokemon?limit=100&offset=0"
    th1 = threading.Thread(target=service_videos, args=[link])
    th1.start()
    for x in range(0, 50):
        th2 = threading.Thread(target=get_service, args=[url])
        th2.start()
    # connection[1].close
    # connection[0].close
