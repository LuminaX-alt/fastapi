import anyio
import signal

def run_app_with_reload(app, **kwargs):
    async def _runner():
        import uvicorn
        await anyio.to_thread.run_sync(uvicorn.run, app, **kwargs)

    async def _main():
        async with anyio.create_task_group() as tg:
            tg.start_soon(_runner)
            with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
                async for signum in signals:
                    tg.cancel_scope.cancel()
                    break

    anyio.run(_main)

try:
    from fastapi_cli.cli import main as cli_main

except ImportError:  # pragma: no cover
    cli_main = None  # type: ignore


def main() -> None:
    if not cli_main:  # type: ignore[truthy-function]
        message = 'To use the fastapi command, please install "fastapi[standard]":\n\n\tpip install "fastapi[standard]"\n'
        print(message)
        raise RuntimeError(message)  # noqa: B904
    cli_main()
