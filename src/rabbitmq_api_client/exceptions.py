import json


class RabbitMQAPIError(Exception):
	"""Base class for all RabbitMQ API errors."""

	def __init__(self, response, status_code, text):
		self.code = 0
		try:
			json_response = json.loads(text)
		except ValueError:
			self.message = f'Invalid JSON error message from RabbitMQ: {response.text}'
		else:
			self.error = json_response.get('error', 'Unknown error')
			self.reason = json_response.get('reason', 'Unknown reason')
		self.status_code = status_code
