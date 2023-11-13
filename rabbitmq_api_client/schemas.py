from enum import Enum

from pydantic import BaseModel
from pydantic import Field


class CreateUser(BaseModel):
    """
    Tags can be one of:
    - management : 	User can access the management plugin
    - policymaker : User can access the management plugin and manage policies and parameters for the vhosts
    they have access to.
    - monitoring:   User can access the management plugin and see all connections and channels as well as node-related
    information.
    - administrator: User can do everything monitoring can do, manage users, vhosts and permissions, close other user's
    connections, and manage policies and parameters for all vhosts.
    """
    name: str
    password: str
    tags: str = Field("",
                      description="Comma-separated list of tags to apply to the user.",
                      examples=["management,policymaker,monitoring,administrator,impersonator"])


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


class Permissions(BaseModel):
    configure: str = Field('^$', description="Configure permission")
    write: str = Field('^$', description="Write permission")
    read: str = Field('^$', description="Read permission")
