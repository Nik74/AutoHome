from loguru import logger

logger.add('./logs/logs.log', format="{time} {level} {message}", level="DEBUG", rotation="20 KB", compression="zip")
