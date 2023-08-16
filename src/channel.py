import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    api_key: str = os.getenv('API_KEY_YT')
    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.__title = self.__channel['items'][0]['snippet']['title']
        self.__video_count = int(self.__channel['items'][0]['statistics']['videoCount'])
        self.__url = f"https://www.youtube.com/channel/{channel_id}"
        self.__description = self.__channel['items'][0]['snippet']['description']
        self.__subscribers_count = int(self.__channel['items'][0]['statistics']['subscriberCount'])
        self.__view_count = int(self.__channel['items'][0]['statistics']['viewCount'])

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel, indent=2, ensure_ascii=False))

    def to_json(self, filename):
        data = {
            "channel_id": self.__channel_id,
            "title": self.__title,
            "description": self.__description,
            "url": self.__url,
            "subscribers_count": self.__subscribers_count,
            "video_count": self.__video_count,
            "view_count": self.__view_count
        }

        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def __add__(self, other) -> int:
        self.__verify_classes(other)
        return self.__subscribers_count + other.__subscribers_count

    def __sub__(self, other) -> int:
        self.__verify_classes(other)
        return self.__subscribers_count - other.__subscribers_count

    def __eq__(self, other):
        self.__verify_classes(other)
        return self.__subscribers_count == other.__subscribers_count

    def __le__(self, other) -> bool:
        self.__verify_classes(other)
        return self.__subscribers_count <= other.__subscribers_count

    def __gt__(self, other):
        self.__verify_classes(other)
        return self.__subscribers_count > other.__subscribers_count

    def __str__(self) -> str:
        return f"{self.__title} ({self.__url})"

    @classmethod
    def __verify_classes(cls, other):
        if not isinstance(other, Channel):
            raise TypeError("Действие допустимо только для экземпляров класса Chanel")

    @classmethod
    def get_service(cls):
        return cls.__youtube

    @property
    def title(self):
        return self.__title

    @property
    def video_count(self):
        return self.__video_count

    @property
    def url(self):
        return self.__url

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def description(self):
        return self.__description

    @property
    def subscribers_count(self):
        return self.__subscribers_count

    @property
    def view_count(self):
        return self.__view_count