import urllib.parse

from rabbitmq_api_client.base import BaseClient
from rabbitmq_api_client.schemas import CreateQueue, CreateUser, CreateVhost, Permissions, Exchange, Binding


class RabbitMQClient(BaseClient):
	"""
	RabbitMQ client for interacting with the RabbitMQ server API.

	Args:
		base_url (str): The base URL of the RabbitMQ server.
		username (str): The username for authentication.
		password (str): The password for authentication.
	"""
	def __init__(self, base_url: str, username: str, password: str):
		"""Initialize a RabbitMQ client.

		Args:
			base_url (str): The base URL of the RabbitMQ server.
			username (str): The username to use for authentication.
			password (str): The password to use for authentication.
		"""
		super().__init__(base_url, username, password)

	def get_overview(self) -> dict:
		"""Get an overview of the RabbitMQ server.

		Returns:
			dict: Overview information.
		"""
		return self.get('/api/overview')

	def get_cluster_name(self) -> dict:
		"""Get the cluster name of the RabbitMQ server.

		Returns:
			dict: Cluster name information.
		"""
		return self.get('/api/cluster-name')

	def get_vhosts(self) -> list[dict]:
		"""Get all vhosts on the RabbitMQ server.

		Returns:
			list[dict]: A list of vhosts.
		"""
		return self.get('/api/vhosts')

	def get_vhost(self, vhost: str) -> dict:
		"""Get a vhost on the RabbitMQ server.

		Args:
			vhost (str): The name of the vhost.

		Returns:
			dict: Information about the specified vhost.
		"""
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/vhosts/{vhost}')

	def create_vhost(self, vhost: CreateVhost) -> dict:
		"""Create a new vhost on the RabbitMQ server.

		Args:
			vhost (CreateVhost): Pydantic model representing the vhost.

		Returns:
			dict: Empty dictionary.
		"""
		vhost_dict = vhost.model_dump(exclude_unset=True)
		vhost_name = urllib.parse.quote(vhost_dict.pop('name'), safe='')
		return self.put(f'/api/vhosts/{vhost_name}', vhost_dict)

	def delete_vhost(self, vhost: str) -> dict:
		"""Delete a vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.

		Returns:
			dict: Empty dictionary.
		"""
		vhost = urllib.parse.quote(vhost, safe='')
		return self.delete(f'/api/vhosts/{vhost}')

	def get_queues(self) -> list[dict]:
		"""Get all queues on the RabbitMQ server.

		Returns:
			list[dict]: A list of queues.
		"""
		return self.get('/api/queues')

	def get_vhost_queues(self, vhost: str) -> list[dict]:
		"""Get all queues for a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.

		Returns:
			list[dict]: List of queues for the specified vhost.
		"""
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/queues/{vhost}')

	def create_queue(self, vhost: str, queue: CreateQueue) -> dict:
		"""Create a new queue on a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.
			queue (CreateQueue): Pydantic model representing the queue.

		Returns:
			dict: Empty dictionary.
		"""
		queue_dict = queue.model_dump(exclude_unset=True)
		queue_name = urllib.parse.quote(queue_dict.pop('name'), safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.put(f'/api/queues/{vhost}/{queue_name}', queue_dict)

	def get_vhost_queue(self, vhost: str, queue_name: str) -> dict:
		"""Get a queue on a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.
			queue_name (str): Name of the queue.

		Returns:
			dict: Information about the specified queue.
		"""
		queue_name = urllib.parse.quote(queue_name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/queues/{vhost}/{queue_name}')

	def get_users(self) -> list:
		"""Get all users on the RabbitMQ server.

		Returns:
			list: List of users.
		"""
		return self.get('/api/users')

	def get_user(self, username: str) -> dict:
		"""Get a user on the RabbitMQ server.

		Args:
			username (str): Name of the user.

		Returns:
			dict: Information about the specified user.
		"""
		return self.get(f'/api/users/{username}')

	def create_user(self, user: CreateUser) -> dict:
		"""Create a new user on the RabbitMQ server.

		Args:
			user (CreateUser): Pydantic model representing the user.

		Returns:
			dict: Empty dictionary.
		"""
		return self.put(
			f'/api/users/{user.name}', {'password': user.password, 'tags': user.tags}
		)

	def delete_user(self, username: str) -> dict:
		"""Delete a user on the RabbitMQ server.

		Args:
			username (str): Name of the user.

		Returns:
			dict: Empty dictionary.
		"""
		return self.delete(f'/api/users/{username}')

	def get_user_permissions(self, username: str) -> list[dict]:
		"""Get the permissions of a user on the RabbitMQ server.

		Args:
			username (str): Name of the user.

		Returns:
			list[dict]: List of permissions for the specified user.
		"""
		return self.get(f'/api/users/{username}/permissions')

	def get_user_topic_permissions(self, username: str) -> list[dict]:
		"""Get the topic permissions of a user on the RabbitMQ server.

		Args:
			username (str): Name of the user.

		Returns:
			list[dict]: List of topic permissions for the specified user.
		"""
		return self.get(f'/api/users/{username}/topic-permissions')

	def get_users_without_permissions(self) -> list[dict]:
		"""Get all users without permissions on the RabbitMQ server.

		Returns:
			list[dict]: List of users without permissions.
		"""
		return self.get('/api/users-without-permissions')

	def get_permissions(self) -> list[dict]:
		"""Get all permissions on the RabbitMQ server.

		Returns:
			list[dict]: List of permissions.
		"""
		return self.get('/api/permissions')

	def get_user_permissions_on_vhost(self, username: str, vhost: str) -> dict:
		"""Get the permissions of a user on a specific vhost on the RabbitMQ server.

		Args:
			username (str): Name of the user.
			vhost (str): Name of the vhost.

		Returns:
			dict: Permissions for the specified user on the specified vhost.
		"""
		username = urllib.parse.quote(username, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/permissions/{vhost}/{username}')

	def create_user_permissions_on_vhost(self, username: str, vhost: str, permissions: Permissions) -> dict:
		"""Create permissions for a user on a specific vhost on the RabbitMQ server.

		Args:
			username (str): Name of the user.
			vhost (str): Name of the vhost.
			permissions (Permissions): Pydantic model representing the permissions.

		Returns:
			dict: Empty dictionary.
		"""
		username = urllib.parse.quote(username, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.put(f'/api/permissions/{vhost}/{username}', permissions.model_dump())

	def delete_user_permissions_on_vhost(self, username: str, vhost: str) -> dict:
		"""Delete permissions for a user on a specific vhost on the RabbitMQ server.
		Args:
			username (str): Name of the user.
			vhost (str): Name of the vhost.

		Returns:
			dict: Empty dictionary.
		"""
		username = urllib.parse.quote(username, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.delete(f'/api/permissions/{vhost}/{username}')

	def get_exchanges(self) -> list[dict]:
		"""Get all exchanges on the RabbitMQ server.
		Returns:
			list[dict]: A list of exchanges.
		"""
		return self.get('/api/exchanges')

	def get_vhost_exchanges(self, vhost: str) -> list[dict]:
		"""Get all exchanges for a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.

		Returns:
			list[dict]: List of exchanges for the specified vhost.
		"""
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/exchanges/{vhost}')

	def get_vhost_exchange(self, vhost: str, exchange_name: str) -> dict:
		"""Get an exchange on a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.
			exchange_name (str): Name of the exchange.

		Returns:
			dict: Information about the specified exchange.
		"""
		exchange_name = urllib.parse.quote(exchange_name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/exchanges/{vhost}/{exchange_name}')

	def create_exchange(self, vhost: str, exchange_name: str, exchange: Exchange) -> dict:
		"""Create a new exchange on a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.
			exchange_name (str): Name of the exchange.
			exchange (Exchange): Pydantic model representing the exchange.

		Returns:
			dict: Empty dictionary.
		"""
		exchange_name = urllib.parse.quote(exchange_name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.put(f'/api/exchanges/{vhost}/{exchange_name}', exchange.model_dump())

	def delete_exchange(self, vhost: str, exchange_name: str) -> dict:
		"""Delete an exchange on a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.
			exchange_name (str): Name of the exchange.

		Returns:
			dict: Empty dictionary.
		"""
		exchange_name = urllib.parse.quote(exchange_name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.delete(f'/api/exchanges/{vhost}/{exchange_name}')

	def get_bindings(self) -> list[dict]:
		"""Get all bindings on the RabbitMQ server.

		Returns:
			list[dict]: A list of bindings.
		"""
		return self.get('/api/bindings')

	def get_vhost_bindings(self, vhost: str) -> list[dict]:
		"""Get all bindings for a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.

		Returns:
			list[dict]: List of bindings for the specified vhost.
		"""
		return self.get(f'/api/bindings/{vhost}')

	def get_vhost_binding(self, vhost: str, exchange: str, queue: str) -> dict:
		"""Get a binding for a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.
			exchange (str): Name of the exchange.
			queue (str): Name of the queue.

		Returns:
			dict: Information about the specified binding.
		"""
		return self.get(f'/api/bindings/{vhost}/e/{exchange}/q/{queue}')

	def create_vhost_binding(self, vhost: str, exchange: str, queue: str, binding: Binding):
		"""Create a new binding for a specific vhost on the RabbitMQ server.

		Args:
			vhost (str): Name of the vhost.
			exchange (str): Name of the exchange.
			queue (str): Name of the queue.
			binding (Binding): Pydantic model representing the binding.

		Returns:
			dict: Empty dictionary.
		"""
		return self.post(f'/api/bindings/{vhost}/e/{exchange}/q/{queue}', binding.model_dump())


