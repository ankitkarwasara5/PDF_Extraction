import logging
import uuid
import json
from logging.handlers import RotatingFileHandler


def create_logger(g):
	# Create a custom log record that includes the request ID
	class RequestFormatter(logging.Formatter):
	    def format(self, record):
	        try:
	            record.request_id = getattr(g, "request_id", "unknown")
	        except RuntimeError:
	            record.request_id = "unknown"
	        return super().format(record)

	#Setting basic logging system to store logs
	log_formatter = RequestFormatter("%(asctime)s [REQ:%(request_id)s] %(levelname)s %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
	log_file = "base.log"
	#Storing 5 files max size od 2MB each file
	handler = RotatingFileHandler(log_file, maxBytes=2*1024*1024, backupCount=5)
	handler.setFormatter(log_formatter)

	logging.getLogger().setLevel(logging.INFO)
	logging.getLogger().addHandler(handler)

	return logging