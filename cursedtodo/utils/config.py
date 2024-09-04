import configparser


class Config:
    # _instance = None
    _config = None

    def __init__(self):
        raise RuntimeError("Config cannot be instanciated")

    @classmethod
    def get(cls, *args) -> str | None:
        if cls._config == None:
            cls._config = configparser.ConfigParser()
            cls._config.read("config.ini")
        try:
            value = cls._config.get(*args)
            return value
        except:
            return None

    @classmethod
    def getint(cls, default: int = 0, *args) -> int:
        if cls._config == None:
            cls._config = configparser.ConfigParser()
            cls._config.read("config.ini")
        try:
            value = cls._config.getint(*args)
            return value
        except:
            return default

    @classmethod
    def getboolean(cls, *args) -> bool:
        if cls._config == None:
            cls._config = configparser.ConfigParser()
            cls._config.read("config.ini")
        try:
            value = cls._config.getboolean(*args)
            return value
        except:
            return False

    # @classmethod
    # def get_instance(cls):
    #     if cls._instance == None:
    #         cls._instance = cls.__new__(cls)
    #     return cls._instance
    #
