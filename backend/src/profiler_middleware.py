from typing import Callable
from fastapi import FastAPI, Request

def register_profiler_middleware(app: FastAPI, enabled: bool):
    """Middleware to user pyinstrument on FastAPI routes to profile application call stack"""

    if enabled:
        from pyinstrument import Profiler
        from pyinstrument.renderers.html import HTMLRenderer
        from pyinstrument.renderers.speedscope import SpeedscopeRenderer

        @app.middleware("http")
        async def profile_request(request: Request, call_next: Callable):
            """Profile the HTTP FastAPI request

            Derived by https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi

            By default profilling data is rendered to PyInstrument's HTML output. Query params
            on any FastAPI endpoint are enabled using ?profile=1;profile_format=html.
            """
            profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
            profile_type_to_renderer = {
                "html": HTMLRenderer,
                "speedscope": SpeedscopeRenderer,
            }

            if request.query_params.get("profile", False):
                profile_type = request.query_params.get("profile_format", "html")
                with Profiler(interval=0.001, async_mode="enabled") as profiler:
                    response = await call_next(request)

                extension = profile_type_to_ext[profile_type]
                renderer = profile_type_to_renderer[profile_type]()
                with open(f"profile.{extension}", "w") as out:
                    out.write(profiler.output(renderer=renderer))
                return response

            return await call_next(request)