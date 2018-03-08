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
    ws = web.WebSocketResponse(heartbeat=30)
    await ws.prepare(request)
    init = json.loads((await ws.receive()).data)
    result = await db.initials.insert_one(init)
    async for msg in ws:
        if msg.type == WSMsgType.text:
            data = json.loads(msg.data)
            data['stamp'] = datetime.utcnow()
            data['init'] = result.insert_id
            await db.markings.insert_one(data)
    return ws


async def home(request):
    html = '''
    Squad Collection
    ================


    https://github.com/theSage21/SquadMarker


    Questions asked     : {q}
    Unique users        : {u}
    Pages covered       : {p}
    '''
    q = await db.markings.count()
    u, p = set(), set()
    async for i in db.markings.find(projection={"ident": 1}):
        if 'ident' in i:
            u.add(i['ident'])
        if 'url' in i:
            p.add(i['url'])
    html = html.format(q=q, u=len(u), p=len(p))
    return web.Response(text=html)


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/mark', mark)
    app.router.add_get('/', home)
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
