import hashlib
import logging

def email_hash(email):
	return hashlib.md5(email.lower().encode("utf-8")).hexdigest()

class StringFilter(logging.Filter):
	def filter(self, record):
		if record.msg.startswith("abc"):
			return False
		return True
	
