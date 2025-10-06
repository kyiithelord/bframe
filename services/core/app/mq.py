import asyncio
import json
from typing import Optional
import aio_pika
from .config import settings

RABBIT_EXCHANGE = "bframe.events"
RABBIT_QUEUE = "bframe.events.queue"

_connection: Optional[aio_pika.RobustConnection] = None
_channel: Optional[aio_pika.abc.AbstractChannel] = None
_exchange: Optional[aio_pika.abc.AbstractExchange] = None

async def connect():
    global _connection, _channel, _exchange
    if _connection and not _connection.is_closed:
        return _connection
    _connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    _channel = await _connection.channel()
    await _channel.set_qos(prefetch_count=10)
    _exchange = await _channel.declare_exchange(RABBIT_EXCHANGE, aio_pika.ExchangeType.TOPIC, durable=True)
    queue = await _channel.declare_queue(RABBIT_QUEUE, durable=True)
    await queue.bind(_exchange, routing_key="#")
    return _connection

async def publish(routing_key: str, payload: dict):
    await connect()
    body = json.dumps(payload).encode()
    message = aio_pika.Message(body, content_type="application/json")
    assert _exchange is not None
    await _exchange.publish(message, routing_key=routing_key)

async def consume(handler):
    await connect()
    assert _channel is not None
    queue = await _channel.declare_queue(RABBIT_QUEUE, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    data = json.loads(message.body)
                except Exception:
                    data = {"raw": message.body.decode(errors="ignore")}
                await handler(message.routing_key, data)

async def default_handler(routing_key: str, payload: dict):
    print(f"[event] {routing_key}: {payload}")

async def start_background_consumer(loop: asyncio.AbstractEventLoop, handler=default_handler):
    loop.create_task(consume(handler))
