from dotenv_settings_handler import BaseSettingsHandler
from dotenv import load_dotenv


class MySettings(BaseSettingsHandler):
    """Settings definition"""
    light_cmd_topic: str
    light_stat_topic: str
    ldr_topic: str
    pir_topic: str
    ldr_threshold: float
    broker = "127.0.0.1"
    port = 1883

    class Config:
        env_prefix = "LC_"


load_dotenv()
settings = MySettings()
