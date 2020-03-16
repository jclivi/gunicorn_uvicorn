import sys
import signal

import context
from standalone_app import StandaloneApp
from service import Service
from util import TryExcept as try_except
from log import log
from util import number_of_workers

@try_except("start gunicorn", True)
def start_gunicorn(framework_config,
                   dispatcher):
    signal.signal(signal.SIGINT, _graceful_exit)

    # get gunicorn options
    gunicorn_options = framework_config.get("gunicorn_options", None)
    if not gunicorn_options:
        log.error("missing gunicorn options config")
        sys.exit(-1)

    from asgi_json_adapter import AsgiJsonAdapter
    proto_adapter = AsgiJsonAdapter()

    # get workers
    gunicorn_options["workers"] = number_of_workers(gunicorn_options.get("workers"))

    app = StandaloneApp(gunicorn_options,
                        Service(proto_adapter))
    log.info("gunicorn starting...")
    app.run()

@try_except("ready framework config", True)
def ready_framework(etc, ctx, dispatcher):
    if not etc:
        print("empty etc")
        sys.exit(-1)

    context.context = context.Context(etc)
    ctx = context.context

    print("config", ctx.config)
    framework_config = ctx.config.get("framework", None)
    if not framework_config:
        print("missing framework config")
        sys.exit(-1)

    return framework_config

@try_except("start service entrance", True)
def start(etc,
          ctx=None,
          dispatcher=None):
    framework_config = ready_framework(etc, ctx, dispatcher)
    start_gunicorn(framework_config,  dispatcher)

def _graceful_exit(signum,
                   frame):
    if callable(context.context.cleanup):
        context.context.cleanup()
    log.debug("service exiting...")
    sys.exit(-1)

