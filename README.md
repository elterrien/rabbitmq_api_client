# Python library to interact with the RabbitMQ Admin API.

## Description

This package provides a simple http client to manage Rabbitmq admin api.

The package is based on [httpx](https://www.python-httpx.org/).

It also provides [pydantic](https://docs.pydantic.dev/latest/) models for request.

## Installation

```bash
pip install rabbitmq-api-client
```

## Usage

```python
from rabbitmq_api_client.client import RabbitMQClient
from rabbitmq_api_client.schemas import CreateUser

# Initialize client with url and credentials
client = RabbitMQClient('http://localhost:15672', 'user', 'password')

# Define a user with pydantic model
user = CreateUser(username='test', password='test', tags='administrator')

# Create user
client.create_user(user)

# Get user by name
user_dict = client.get_user('test')
```


