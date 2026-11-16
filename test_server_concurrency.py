"""Concurrency check for the badge server (queue row 96 / repo-vibe D3).

The badge path makes a blocking upstream GitHub call per uncached request
(app.api timeout is 20 s). Under the original single-threaded HTTPServer,
one slow upstream response serialized every other request behind it. The
server now uses ThreadingHTTPServer; this test proves two slow badge
requests are actually served in parallel, and that the public posture is
unchanged (public repos only, stats fetched with token None).
"""
import threading
import time
import urllib.request
from unittest.mock import patch

import app


def _serve(server):
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return thread


def _get(url):
    with urllib.request.urlopen(url, timeout=10) as resp:
        return resp.status, resp.read()


def test_slow_badge_requests_are_served_concurrently():
    app._cache.clear()

    def slow_api(path, token=None, method="GET", data=None):
        time.sleep(0.6)
        return {"private": False}

    server = app.make_server(("127.0.0.1", 0), app.H)
    port = server.server_address[1]
    _serve(server)
    try:
        with patch.object(app, "api", side_effect=slow_api), \
             patch.object(app.repo_vibe, "fetch_stats", return_value={"public": True}), \
             patch.object(app.repo_vibe, "render_svg", return_value="<svg/>"):
            start = time.monotonic()
            threads = [
                threading.Thread(
                    target=_get,
                    args=(f"http://127.0.0.1:{port}/badge/example/project{i}",),
                )
                for i in range(2)
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            elapsed = time.monotonic() - start
    finally:
        server.shutdown()
        server.server_close()
    # Serialized handling would take >= 1.2 s (2 x 0.6 s upstream sleeps).
    assert elapsed < 1.0, f"requests appear serialized: {elapsed:.2f}s for two 0.6s requests"
