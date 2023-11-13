import urllib.parse

from rabbitmq_api_client.base import BaseClient
from rabbitmq_api_client.schemas import CreateQueue, CreateUser, CreateVhost, Permissions


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

	def get_vhost(self, name: str) -> dict:
		"""Get a vhost on the RabbitMQ server.

		:param name: the name of the vhost
		:return: dict of vhost
		"""
		name = urllib.parse.quote(name, safe='')
		return self.get(f'/api/vhosts/{name}')

	def create_vhost(self, vhost: CreateVhost) -> dict:
		"""Create a new vhost on the RabbitMQ server.

		:param vhost: pydantic model of vhost
		:return: empty dict
		"""
		vhost_dict = vhost.model_dump(exclude_unset=True)
		name = vhost_dict.pop('name')
		name = urllib.parse.quote(name, safe='')
		return self.put(f'/api/vhosts/{name}', vhost_dict)

	def delete_vhost(self, name: str) -> dict:
		"""Delete a vhost on the RabbitMQ server.

		:param name: name of vhost
		:return: empty dict
		"""
		name = urllib.parse.quote(name, safe='')
		return self.delete(f'/api/vhosts/{name}')

	def get_queues(self) -> list[dict]:
		"""Get all queues on the RabbitMQ server.

		:return: a list of queues
		"""
		return self.get('/api/queues')

	def get_vhost_queues(self, name: str) -> list[dict]:
		"""Get all queues for a specific vhost on the RabbitMQ server.

		:param name: name of vhost
		:return: list of queues
		"""
		name = urllib.parse.quote(name, safe='')
		return self.get(f'/api/queues/{name}')

	def create_queue(self, vhost: str, queue: CreateQueue) -> dict:
		"""Create a new queue on a specific vhost on the RabbitMQ server.

		:param vhost: name of vhost
		:param queue: name of queue
		:return: empty dict
		"""
		queue_dict = queue.model_dump(exclude_unset=True)
		name = queue_dict.pop('name')
		name = urllib.parse.quote(name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.put(f'/api/queues/{vhost}/{name}', queue_dict)

	def get_vhost_queue(self, vhost: str, name: str) -> dict:
		"""
		Get a queue on a specific vhost on the RabbitMQ server.

		:param vhost: name of vhost
		:param name: name of queue
		:return: dict of queue
		"""
		name = urllib.parse.quote(name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/queues/{vhost}/{name}')

	def get_users(self) -> list:
		"""Get all users on the RabbitMQ server.

		:return: list of users
		"""
		return self.get('/api/users')

	def get_user(self, name: str) -> dict:
		"""Get a user on the RabbitMQ server.

		:param name: name of user
		:return: dict of user
		"""
		return self.get(f'/api/users/{name}')

	def create_user(self, user: CreateUser) -> dict:
		"""Create a new user on the RabbitMQ server.

		:param user:
		:return: empty dict
		"""
		return self.put(
			f'/api/users/{user.name}', {'password': user.password, 'tags': user.tags}
		)

	def delete_user(self, name: str) -> dict:
		"""Delete a user on the RabbitMQ server.

		:param name: name of user
		:return: empty dict
		"""
		return self.delete(f'/api/users/{name}')

	def get_user_permissions(self, name: str) -> dict:
		return self.get(f'/api/users/{name}/permissions')

	def get_user_topic_permissions(self, name: str) -> dict:
		return self.get(f'/api/users/{name}/topic-permissions')

	def get_users_without_permissions(self) -> list:
		return self.get('/api/users-without-permissions')

	def get_permissions(self) -> list:
		return self.get('/api/permissions')

	def get_user_permissions_on_vhost(self, name: str, vhost: str) -> dict:
		name = urllib.parse.quote(name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.get(f'/api/permissions/{vhost}/{name}')

	def create_user_permissions_on_vhost(self, name: str, vhost: str, permissions: Permissions) -> dict:
		name = urllib.parse.quote(name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.put(f'/api/permissions/{vhost}/{name}', permissions.model_dump())

	def delete_user_permissions_on_vhost(self, name: str, vhost: str) -> dict:
		name = urllib.parse.quote(name, safe='')
		vhost = urllib.parse.quote(vhost, safe='')
		return self.delete(f'/api/permissions/{vhost}/{name}')
