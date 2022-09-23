from threading import Thread, Semaphore
from pytube import YouTube

semaforo = Semaphore(1)


def get_videos(link):
    video = YouTube(link)
    file = video.streams.filter(
        file_extension='mp4').get_by_itag(18)
    file.download("semaphore/videos")


class Hilo(Thread):
    def __init__(self, link):
        Thread.__init__(self)
        self.link = link

    def run(self):
        semaforo.acquire()
        get_videos(self.link)
        semaforo.release()


links = ["https://www.youtube.com/watch?v=4t91S0Cfl-4",
         "https://www.youtube.com/watch?v=20Ry1dxqxOg",
         "https://www.youtube.com/watch?v=KHV79cF0JKc",
         "https://www.youtube.com/watch?v=haujoh19QVk",
         "https://www.youtube.com/watch?v=k489L7IReiA"]
threads_semaphore = []
for l in links:
    threads_semaphore.append(Hilo(l))
for t in threads_semaphore:
    t.start()
