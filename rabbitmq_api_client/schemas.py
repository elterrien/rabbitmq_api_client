from enum import Enum

from pydantic import BaseModel


class CreateUser(BaseModel):
	name: str
	password: str
	tags: str


class QueueType(str, Enum):
	classic = 'classic'
	quorum = 'quorum'
	stream = 'stream'


class CreateVhost(BaseModel):
	name: str
	tracing: bool = False
	tags: str = ''
	description: str = ''
	default_queue_type: QueueType = QueueType.quorum


class CreateQueue(BaseModel):
	name: str
	auto_delete: bool = False
	durable: bool = True
	arguments: dict = {}
	node: str = ''
