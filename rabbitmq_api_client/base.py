import httpx

from rabbitmq_api_client.exceptions import RabbitMQAPIError


class BaseClient:
	"""Base client for making HTTP requests with basic authentication.

	Args:
		base_url (str): The base URL of the API.
		username (str): The username for basic authentication.
		password (str): The password for basic authentication.

	Attributes:
		base_url (str): The base URL of the API.
		username (str): The username for basic authentication.
		password (str): The password for basic authentication.
		client (httpx.Client): The HTTP client for making requests.

	Methods:
		request: Make a generic HTTP request.
		get: Make a GET request.
		post: Make a POST request.
		put: Make a PUT request.
		delete: Make a DELETE request.
		close: Close the HTTP client.
		__del__: Destructor to automatically close the client on object deletion.
		__repr__: String representation of the BaseClient instance.

	Example:
		client = BaseClient("https://api.example.com", "user", "pass")
		response = client.get("/resource")
		print(response)
	"""
	def __init__(self, base_url: str, username: str, password: str):
		"""Initialize the BaseClient with the provided base URL, username, and password."""
		self.base_url = base_url
		self.username = username
		self.password = password
		self.client = httpx.Client(
			base_url=self.base_url, auth=(self.username, self.password)
		)

	def request(self, method: str, url: str, **kwargs):
		"""Make a generic HTTP request.
		Args:
			method (str): The HTTP method (e.g., 'get', 'post', 'put', 'delete').
			url (str): The URL for the request.
			**kwargs: Additional keyword arguments to pass to the request.

		Returns:
			dict or str: The JSON response if available, or the raw text response.

		Raises:
			RabbitMQAPIError: If the response status code is not in the 2xx range.
		"""
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
		"""Make a GET request.
		Args:
			url (str): The URL for the GET request.
			params (dict, optional): Additional parameters for the GET request.

		Returns:
			dict or str: The JSON response if available, or the raw text response.
		"""
		return self.request('get', url, params=params)

	def post(self, url: str, data: dict = None):
		"""Make a POST request.
		Args:
			url (str): The URL for the POST request.
			data (dict, optional): The JSON data to include in the POST request.

		Returns:
			dict or str: The JSON response if available, or the raw text response.
		"""
		return self.request('post', url, json=data)

	def put(self, url: str, data: dict = None):
		"""Make a PUT request.

		Args:
			url (str): The URL for the PUT request.
			data (dict, optional): The JSON data to include in the PUT request.

		Returns:
			dict or str: The JSON response if available, or the raw text response.
		"""
		return self.request('put', url, json=data)

	def delete(self, url: str):
		"""Make a DELETE request.

		Args:
			url (str): The URL for the DELETE request.

		Returns:
			dict or str: The JSON response if available, or the raw text response.
		"""
		return self.request('delete', url)

	def close(self):
		"""Close the HTTP client."""
		self.client.close()

	def __del__(self):
		"""Destructor to automatically close the client on object deletion."""
		self.close()

	def __repr__(self):
		"""String representation of the BaseClient instance."""
		return f'<{self.__class__.__name__} {self.base_url}>'
