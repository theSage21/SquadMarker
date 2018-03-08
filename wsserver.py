import os
import ujson as json
from motor import motor_asyncio
import aiohttp_cors
from datetime import datetime
from aiohttp import web, WSMsgType


MONGO_URL = os.environ.get('MONGODB_URI')
PORT = os.environ.get("PORT")
PORT = PORT if PORT else 8000
client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
dbname = MONGO_URL.split('/')[-1]
db = client[dbname]


async def mark(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ident = (await ws.receive()).data
    html = (await ws.receive()).data
    async for msg in ws:
        if msg.type == WSMsgType.text:
            data = json.loads(msg.data)
            data['html'] = html
            data['stamp'] = datetime.utcnow()
            data['ident'] = ident
            await db.markings.insert_one(data)
    return ws


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/mark', mark)
    corsconfig = {"*": aiohttp_cors.ResourceOptions(allow_credentials=True,
                                                    expose_headers="*",
                                                    allow_headers="*")}
    cors = aiohttp_cors.setup(app, defaults=corsconfig)
    cors = aiohttp_cors.setup(app, defaults=corsconfig)
    for route in list(app.router.routes()):
        try:
            cors.add(route)
        except Exception as e:
            print(e)  # /register will be added twice and will raise error
    web.run_app(app, host='0.0.0.0', port=PORT)
