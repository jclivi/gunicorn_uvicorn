from starlette.requests import Request

class AsgiJsonAdapter:
    @classmethod
    async def parse_request(cls, scope, receive):
        request = Request(scope, receive)

        # get url地址
        status,body = 200, (request.url.path).split("/")
        body = "SUCCESS! " + body[1]

        return status,body

    @classmethod
    def pack_response(cls, message):
        pass

