import uvicorn
import gunicorn.app.base
from gunicorn.six import iteritems


class StandaloneApp(gunicorn.app.base.BaseApplication):
    def _default_handler(self, environ, start_response):
        response_body = b'Service NOT Imlemented'
        status = '501 Not Implemented'
        response_headers = [
            ('Content-Type', 'text/plain'),
        ]
        start_response(status, response_headers)
        return iter([response_body])

    async def _async_handler(message, channels):
         content = b'<h1>Service NOT Imlemented</h1>'
         resp = {
             'status': 501,
             'headers': [[b'content-type', b'text/html'],],
             'content': content,
         }
         await channels['reply'].send(resp)

    async def _uvicorn_async_handler(self, scope, receive, send):
        assert scope['type'] == 'http'
        await send({
            'type': 'http.response.start',
            'status': 501,
            'headers': [
                [b'content-type', b'text/plain'],
            ]
        })
        await send({
            'type': 'http.response.body',
            'body': b'Service NOT Imlemented',
        })

    def __init__(self, options=None, app=None):
        self.options = options or {}
        self.application = app or self._uvicorn_async_handler
        super(StandaloneApp, self).__init__()

    def load(self):
        return self.application

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def set_config(self, options):
        self.options = options or {}
        self.load_config()
