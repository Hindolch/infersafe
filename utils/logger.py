import logging

#configure the logger
logger = logging.getLogger("inference_logger")
logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler("inference.log")
file_handler.setLevel(logging.INFO)

#formatter for readibility
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
# Add the file handler to the logger
logger.addHandler(file_handler)