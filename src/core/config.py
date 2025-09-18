from pathlib import Path
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from pydantic import SecretStr, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__name__).parent.parent.parent


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )


class BotSettings(BaseSettings):
    bot_token: SecretStr
    admin_id: int

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf8", extra="ignore"
    )


class Setting(BaseModel):
    bot: BotSettings = BotSettings()


setting = Setting()

bot = Bot(
    setting.bot.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher(storage=MemoryStorage())
