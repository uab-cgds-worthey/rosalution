# pylint: disable=import-outside-toplevel
# Disabling this rule to avoid relying on a global variable to enable the profiler. Keeping the profiler
# enabled only if its enabled as a method param for the time being for simplicity.

"""Module to enable PyInstrument to profile FastAPI routes"""
from typing import Callable
from fastapi import FastAPI, Request


def register_profiler_middleware(app: FastAPI, enabled: bool, output_renderer: str = "html"):
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
            profiler_output_file_extension = {"html": "html", "speedscope": "speedscope.json"}
            profiler_renderer = {
                "html": HTMLRenderer,
                "speedscope": SpeedscopeRenderer,
            }

            if request.query_params.get("profile", False):
                profile_type = request.query_params.get("profile_format", output_renderer)
                with Profiler(interval=0.001, async_mode="enabled") as profiler:
                    response = await call_next(request)

                file_extension = profiler_output_file_extension[profile_type]
                renderer = profiler_renderer[profile_type]()
                with open(f"profile.{file_extension}", mode="w", encoding="utf-8") as out:
                    out.write(profiler.output(renderer=renderer))
                return response

            return await call_next(request)
