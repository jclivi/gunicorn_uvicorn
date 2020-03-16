import sys
import traceback
import uvicorn
from log import log

class Service(object):
    def __init__(self, proto_adapter):
        self.proto_adapter = proto_adapter
        self._message = {}

    async def __call__(self, scope, receive, send):
        assert scope["type"] == "http"
        try:
            # build message for ASGI
            status,body = await self.proto_adapter.parse_request(scope, receive)
            self._message = {"status": status, "body": body}
            if status != 200:
                log.info("parse message failed:%s", body)
                await self._uvicorn_response(send, self._message)
                return

            # send response
            await self._uvicorn_response(send, self._message)
            length = (len(str(body)) if body else 0)
            log.debug("response raw data, len:%d", length)
        except GeneratorExit:
            log.warning("peer closed connection before respond")
            return
        except:
            log.debug(str(traceback.format_exc()))
            status = 500
            body = "Internal Server Error"
            await self._uvicorn_response(send, self._message)
            return
        finally:
            log.debug(e)

    async def _uvicorn_response(self, send, message):
        status = message.get("status")
        msg_body = message.get("body", None)
        await send({
            'type': 'http.response.start',
            'status': status,
            'headers': [
                [b'content-type', b'text/plain'],
            ]
        })
        
        if not msg_body:
            body = b""
        if not isinstance(msg_body, bytes):
            body = str(msg_body).encode()
        else:
            body = msg_body

        await send({
            'type': 'http.response.body',
            'body': body,
        })
