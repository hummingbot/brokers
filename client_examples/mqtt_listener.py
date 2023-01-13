#!/usr/bin/env python

import asyncio
from commlib.node import Node
from commlib.transports.mqtt import ConnectionParameters
from typing import Any, List, Optional, Tuple

from commlib.msg import PubSubMessage, RPCMessage, HeartbeatMessage


class MQTT_STATUS_CODE:
    ERROR: int = 400
    SUCCESS: int = 200


class NotifyMessage(PubSubMessage):
    seq: Optional[int] = 0
    timestamp: Optional[int] = -1
    msg: Optional[str] = ''


class EventMessage(PubSubMessage):
    timestamp: Optional[int] = -1
    type: Optional[str] = 'Unknown'
    data: Optional[dict] = {}


class LogMessage(PubSubMessage):
    timestamp: float = 0.0
    msg: str = ''
    level_no: int = 0
    level_name: str = ''
    logger_name: str = ''


class StartCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        log_level: Optional[str] = None
        restore: Optional[bool] = False
        script: Optional[str] = None
        is_quickstart: Optional[bool] = False

    class Response(RPCMessage.Response):
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class StopCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        skip_order_cancellation: Optional[bool] = False

    class Response(RPCMessage.Response):
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class ConfigCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        params: Optional[List[Tuple[str, Any]]] = []

    class Response(RPCMessage.Response):
        changes: Optional[List[Tuple[str, Any]]] = []
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class CommandShortcutMessage(RPCMessage):
    class Request(RPCMessage.Request):
        params: Optional[List[List[Any]]] = []

    class Response(RPCMessage.Response):
        success: Optional[List[bool]] = []
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class ImportCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        strategy: str

    class Response(RPCMessage.Response):
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''


class StatusCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        pass

    class Response(RPCMessage.Response):
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''
        data: Optional[str] = ''


class HistoryCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        days: Optional[float] = 0
        verbose: Optional[bool] = False
        precision: Optional[int] = None

    class Response(RPCMessage.Response):
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''
        trades: Optional[List[Any]] = []


class BalanceLimitCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        exchange: str
        asset: str
        amount: float

    class Response(RPCMessage.Response):
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''
        data: Optional[str] = ''


class BalancePaperCommandMessage(RPCMessage):
    class Request(RPCMessage.Request):
        asset: str
        amount: float

    class Response(RPCMessage.Response):
        status: Optional[int] = MQTT_STATUS_CODE.SUCCESS
        msg: Optional[str] = ''
        data: Optional[str] = ''


class HummingbotMQTTListener(Node):
    NOTIFY_URI = '/$instance_id/notify'
    HEARTBEAT_URI = '/$instance_id/hb'
    EVENTS_URI = '/$instance_id/events'
    LOGS_URI = '/$instance_id/log'

    def __init__(self,
                 host: str = 'localhost',
                 port: int = 1883,
                 username: str = '',
                 password: str = '',
                 bot_id: str = 'bot1',
                 namespace: str = 'hbot',
                 notifications: bool = True,
                 events: bool = True,
                 logs: bool = True,
                 heartbeats: bool = False):
        self._notifications = notifications
        self._events = events
        self._logs = logs
        self._heartbeats = heartbeats
        self._bot_id = bot_id
        self._ns = namespace

        self.HEARTBEAT_URI = self.HEARTBEAT_URI.replace('$instance_id', self._bot_id)
        self.HEARTBEAT_URI = f'{self._ns}{self.HEARTBEAT_URI}'
        self.NOTIFY_URI = self.NOTIFY_URI.replace('$instance_id', self._bot_id)
        self.NOTIFY_URI = f'{self._ns}{self.NOTIFY_URI}'
        self.EVENTS_URI = self.EVENTS_URI.replace('$instance_id', self._bot_id)
        self.EVENTS_URI = f'{self._ns}{self.EVENTS_URI}'
        self.LOGS_URI = self.LOGS_URI.replace('$instance_id', self._bot_id)
        self.LOGS_URI = f'{self._ns}{self.LOGS_URI}'

        conn_params = ConnectionParameters(
            host=host,
            port=int(port),
            username=username,
            password=password
        )

        super().__init__(
            node_name=f'{self._ns}.{self._bot_id}',
            connection_params=conn_params,
            heartbeats=False,
            debug=True
        )

    def _init_endpoints(self):
        if self._notifications:
            self.notify_sub = self.create_subscriber(msg_type=NotifyMessage,
                                                     topic=self.NOTIFY_URI,
                                                     on_message=self._on_notification)
            print(f'[*] Subscribed to NOTIFY topic: {self.NOTIFY_URI}')
        if self._events:
            self.events_sub = self.create_subscriber(msg_type=EventMessage,
                                                     topic=self.EVENTS_URI,
                                                     on_message=self._on_event)
            print(f'[*] Subscribed to EVENT topic: {self.EVENTS_URI}')
        if self._logs:
            self.logs_sub = self.create_subscriber(msg_type=LogMessage,
                                                   topic=self.LOGS_URI,
                                                   on_message=self._on_log)
            print(f'[*] Subscribed to LOG topic: {self.LOGS_URI}')
        if self._heartbeats:
            self.hb_sub = self.create_subscriber(msg_type=HeartbeatMessage,
                                                 topic=self.HEARTBEAT_URI,
                                                 on_message=self._on_hb)
            print(f'[*] Subscribed to HEARTBEAT topic: {self.LOGS_URI}')

    def _on_notification(self, msg):
        print(f'[NOTIFICATION] - {msg}')

    def _on_event(self, msg):
        print(f'[EVENT] - {msg}')

    def _on_log(self, msg):
        print(f'[LOG] - {msg}')

    def _on_hb(self, msg):
        print(f'[HEARTBEAT] - {msg}')

    def start(self):
        self._init_endpoints()
        self.run()

    async def run_forever(self):
        self.start()
        while True:
            await asyncio.sleep(0.01)


if __name__ == "__main__":
    import time
    client = HummingbotMQTTListener(
        host='localhost',
        port=1883,
        username='',
        password='',
        bot_id='bot1',
        notifications=True,
        events=True,
        logs=True,
        heartbeats=False
    )
    asyncio.new_event_loop().run_until_complete(client.run_forever())
