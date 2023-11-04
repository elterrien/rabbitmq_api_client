import httpx

from rabbitmq_api_client.exceptions import RabbitMQAPIError


class BaseClient:
	def __init__(self, base_url: str, username: str, password: str):
		self.base_url = base_url
		self.username = username
		self.password = password
		self.client = httpx.Client(
			base_url=self.base_url, auth=(self.username, self.password)
		)

	def request(self, method: str, url: str, **kwargs):
		response = self.client.request(method, url, **kwargs)
		if not (200 <= response.status_code < 300):
			raise RabbitMQAPIError(response, response.status_code, response.text)
		if response.text.strip():
			try:
				return response.json()
			except ValueError:
				return response.text
		else:
			return {}

	def get(self, url: str, params: dict = None):
		return self.request('get', url, params=params)

	def post(self, url: str, data: dict = None):
		return self.request('post', url, json=data)

	def put(self, url: str, data: dict = None):
		return self.request('put', url, json=data)

	def delete(self, url: str):
		return self.request('delete', url)

	def close(self):
		self.client.close()

	def __del__(self):
		self.close()

	def __repr__(self):
		return f'<{self.__class__.__name__} {self.base_url}>'
