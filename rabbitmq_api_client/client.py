import urllib.parse

from rabbitmq_api_client.base import BaseClient
from rabbitmq_api_client.schemas import CreateQueue, CreateUser, CreateVhost, Permissions, Exchange, Binding


class RabbitMQClient(BaseClient):
	def __init__(self, base_url: str, username: str, password: str):
		"""Initialize a RabbitMQ client.

		:param base_url: the base url of the RabbitMQ server
		:param username: the username to use for authentication
		:param password: the password to use for authentication
		"""

		super().__init__(base_url, username, password)

	def get_overview(self) -> dict:
		"""Get an overview of the RabbitMQ server.

		:return: dict of overview information
		"""
		return self.get('/api/overview')

	def get_cluster_name(self) -> dict:
		"""Get the cluster name of the RabbitMQ server.

		:return: dict with cluster name
		"""
		return self.get('/api/cluster-name')

	def get_vhosts(self) -> list[dict]:
		"""Get all vhosts on the RabbitMQ server.

		:return: a list of vhosts
		"""
		return self.get('/api/vhosts')

	def get_vhost(self, vhost: str) -> dict:
		"""Get a vhost on the RabbitMQ server.

		:param name: the name of the vhost
		:return: dict of vhost
		"""
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/vhosts/{vhost}')

	def create_vhost(self, vhost: CreateVhost) -> dict:
		"""Create a new vhost on the RabbitMQ server.

		:param vhost: pydantic model of vhost
		:return: empty dict
		"""
		vhost_dict = vhost.model_dump(exclude_unset=True)
		vhost_name = urllib.parse.quote(vhost_dict.pop('name'), safe='')
		return self.put(f'/api/vhosts/{vhost_name}', vhost_dict)

	def delete_vhost(self, vhost: str) -> dict:
		"""Delete a vhost on the RabbitMQ server.

		:param vhost: name of vhost
		:return: empty dict
		"""
		vhost = urllib.parse.quote(vhost, safe='')
		return self.delete(f'/api/vhosts/{vhost}')

	def get_queues(self) -> list[dict]:
		"""Get all queues on the RabbitMQ server.

		:return: a list of queues
		"""
		return self.get('/api/queues')

	def get_vhost_queues(self, vhost: str) -> list[dict]:
		"""Get all queues for a specific vhost on the RabbitMQ server.

		:param vhost: name of vhost
		:return: list of queues
		"""
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/queues/{vhost}')

	def create_queue(self, vhost: str, queue: CreateQueue) -> dict:
		"""Create a new queue on a specific vhost on the RabbitMQ server.

		:param vhost: name of vhost
		:param queue: name of queue
		:return: empty dict
		"""
		queue_dict = queue.model_dump(exclude_unset=True)
		queue_name = urllib.parse.quote(queue_dict.pop('name'), safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.put(f'/api/queues/{vhost}/{queue_name}', queue_dict)

	def get_vhost_queue(self, vhost: str, queue_name: str) -> dict:
		"""
		Get a queue on a specific vhost on the RabbitMQ server.

		:param vhost: name of vhost
		:param queue_name: name of queue
		:return: dict of queue
		"""
		queue_name = urllib.parse.quote(queue_name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/queues/{vhost}/{queue_name}')

	def get_users(self) -> list:
		"""Get all users on the RabbitMQ server.

		:return: list of users
		"""
		return self.get('/api/users')

	def get_user(self, username: str) -> dict:
		"""Get a user on the RabbitMQ server.

		:param username: name of user
		:return: dict of user
		"""
		return self.get(f'/api/users/{username}')

	def create_user(self, user: CreateUser) -> dict:
		"""Create a new user on the RabbitMQ server.

		:param user:
		:return: empty dict
		"""
		return self.put(
			f'/api/users/{user.name}', {'password': user.password, 'tags': user.tags}
		)

	def delete_user(self, username: str) -> dict:
		"""Delete a user on the RabbitMQ server.

		:param username: name of user
		:return: empty dict
		"""
		return self.delete(f'/api/users/{username}')

	def get_user_permissions(self, username: str) -> list[dict]:
		"""
		Get the permissions of a user on the RabbitMQ server.
		:param username: the name of the user
		:return: list of permissions
		"""
		return self.get(f'/api/users/{username}/permissions')

	def get_user_topic_permissions(self, username: str) -> list[dict]:
		return self.get(f'/api/users/{username}/topic-permissions')

	def get_users_without_permissions(self) -> list[dict]:
		return self.get('/api/users-without-permissions')

	def get_permissions(self) -> list[dict]:
		return self.get('/api/permissions')

	def get_user_permissions_on_vhost(self, username: str, vhost: str) -> dict:
		username = urllib.parse.quote(username, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/permissions/{vhost}/{username}')

	def create_user_permissions_on_vhost(self, username: str, vhost: str, permissions: Permissions) -> dict:
		username = urllib.parse.quote(username, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.put(f'/api/permissions/{vhost}/{username}', permissions.model_dump())

	def delete_user_permissions_on_vhost(self, username: str, vhost: str) -> dict:
		username = urllib.parse.quote(username, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.delete(f'/api/permissions/{vhost}/{username}')

	def get_exchanges(self) -> list[dict]:
		"""
		Get all exchanges on the RabbitMQ server.
		:return: list of exchanges
		"""
		return self.get('/api/exchanges')

	def get_vhost_exchanges(self, vhost: str) -> list[dict]:
		"""
		Get all exchanges on a specific vhost on the RabbitMQ server.
		:param vhost: name of vhost
		:return: a list of exchanges
		"""
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/exchanges/{vhost}')

	def get_vhost_exchange(self, vhost: str, exchange_name: str) -> dict:
		"""
		Get an exchange on a specific vhost on the RabbitMQ server.
		:param vhost: name of vhost
		:param exchange_name: name of exchange
		:return: dict of exchange
		"""
		exchange_name = urllib.parse.quote(exchange_name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/exchanges/{vhost}/{exchange_name}')

	def create_exchange(self, vhost: str, exchange_name: str, exchange: Exchange) -> dict:
		"""
		Create an exchange on a specific vhost on the RabbitMQ server.
		:param vhost: name of vhost
		:param exchange_name: name of exchange
		:param exchange: body of exchange
		:return: empty dict
		"""
		exchange_name = urllib.parse.quote(exchange_name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.put(f'/api/exchanges/{vhost}/{exchange_name}', exchange.model_dump())

	def delete_exchange(self, vhost: str, exchange_name: str) -> dict:
		"""
		Delete an exchange on a specific vhost on the RabbitMQ server.
		:param vhost: name of vhost
		:param exchange_name: name of exchange
		:return: empty dict
		"""
		exchange_name = urllib.parse.quote(exchange_name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.delete(f'/api/exchanges/{vhost}/{exchange_name}')

	def get_bindings(self) -> list[dict]:
		"""
		Get the list of all bindings
		:return:
		"""
		return self.get('/api/bindings')

	def get_vhost_bindings(self, vhost: str) -> list[dict]:
		"""
		Get the list of all bindings for a vhost
		:param vhost: the name of vhost
		:return: list of dict
		"""
		return self.get(f'/api/bindings/{vhost}')

	def get_vhost_binding(self, vhost, exchange, queue: str):
		"""
		:param vhost:
		:param exchange:
		:param queue:
		:return:
		"""
		return self.get(f'/api/bindings/{vhost}/e/{exchange}/q/{queue}')

	def create_vhost_binding(self, vhost: str, exchange: str, queue: str, binding: Binding):
		return self.post(f'/api/bindings/{vhost}/e/{exchange}/q/{queue}', binding.model_dump())


