import unittest
from unittest import TestCase

from rabbitmq_api_client.client import RabbitMQClient
from rabbitmq_api_client.exceptions import RabbitMQAPIError
from rabbitmq_api_client.schemas import CreateUser, CreateVhost


class TestBaseClient(TestCase):
	def setUp(self):
		self.client = RabbitMQClient('http://localhost:15672', 'user', 'password')


class TestClientCommon(TestBaseClient):
	def tearDown(self):
		list_vhosts = self.client.get_vhosts()
		for vhost in list_vhosts:
			self.client.delete_vhost(vhost['name'])
		self.client.close()

	def test_get_overview(self):
		response = self.client.get_overview()
		self.assertIs(type(response), dict)

	def test_get_cluster_name(self):
		response = self.client.get_cluster_name()
		self.assertIs(type(response), dict)


class TestClientUser(TestBaseClient):

	def tearDown(self):
		list_users = self.client.get_users()
		for user in list_users:
			if user['name'] != 'user':
				self.client.delete_user(user['name'])
		self.client.close()

	def test_get_users(self):
		users = self.client.get_users()
		self.assertIs(type(users), list)
		self.assertEqual(len(users), 1)
		self.assertEqual(users[0]['name'], 'user')
		self.assertEqual(users[0]['tags'], ['administrator'])

	def test_create_user(self):
		user = CreateUser(name='test', password='test', tags='administrator,management')
		response = self.client.create_user(user)
		self.assertEqual({}, response)

	def test_delete_user(self):
		user = CreateUser(name='test', password='test', tags='administrator,management')
		response = self.client.create_user(user)
		self.assertEqual({}, response)
		response = self.client.delete_user('test')
		self.assertEqual({}, response)
		with self.assertRaises(RabbitMQAPIError) as context:
			self.client.get_user('test')

	def test_get_user_not_found(self):
		with self.assertRaises(RabbitMQAPIError) as context:
			self.client.get_user('wrong_user')
		self.assertEqual(context.exception.status_code, 404)
		self.assertEqual(context.exception.error, 'Object Not Found')
		self.assertEqual(context.exception.reason, 'Not Found')


class TestClientVhost(TestBaseClient):
	def tearDown(self):
		response = self.client.get_vhosts()
		for vhost in response:
			self.client.delete_vhost(vhost['name'])

	def test_get_vhosts(self):
		list_vhosts = self.client.get_vhosts()
		self.assertIs(type(list_vhosts), list)
		self.client.create_vhost(CreateVhost(name='test', default_queue_type='quorum'))
		list_vhosts = self.client.get_vhosts()
		self.assertIs(type(list_vhosts), list)
		self.assertEqual(len(list_vhosts), 1)

	def test_get_vhost(self):
		vhost = CreateVhost(
			name='test',
			default_queue_type='quorum',
			tags='test,test2',
			description='description',
		)
		self.client.create_vhost(vhost)
		response = self.client.get_vhost('test')
		self.assertEqual(response['name'], 'test')
		self.assertEqual(response['tracing'], False)
		self.assertEqual(response['tags'], vhost.tags.split(','))
		self.assertEqual(response['description'], vhost.description)
		self.assertEqual(response['default_queue_type'], vhost.default_queue_type)

	def test_get_vhost_not_found(self):
		with self.assertRaises(RabbitMQAPIError) as context:
			self.client.get_vhost('wrong_user')
		self.assertEqual(context.exception.status_code, 404)
		self.assertEqual(context.exception.error, 'Object Not Found')
		self.assertEqual(context.exception.reason, 'Not Found')

	def test_create_vhost(self):
		vhost = CreateVhost(name='test', default_queue_type='quorum')
		response = self.client.create_vhost(vhost)
		self.assertEqual({}, response)

	def test_delete_vhost(self):
		vhost = CreateVhost(name='test2', default_queue_type='quorum')
		response = self.client.create_vhost(vhost)
		self.assertEqual({}, response)
		response = self.client.delete_vhost('test2')
		self.assertEqual({}, response)
		with self.assertRaises(RabbitMQAPIError):
			self.client.get_vhost('test2')


if __name__ == '__main__':
	unittest.main()