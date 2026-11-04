import io
from unittest.mock import patch

import app
from test_server_security import request


def test_setup_never_consumes_one_time_credentials():
    for path in ("/setup", "/manifest", "/setup/callback?code=synthetic-once-only"):
        handler = object.__new__(app.H)
        handler.path = path
        responses = []
        handler._send = lambda status, body, ctype=None: responses.append((status, body))
        with patch.object(app, "api") as upstream:
            handler.do_GET()
            assert responses[0][0] == 410
            upstream.assert_not_called()


def setup_function():
    app._cache.clear()


def test_expired_cache_refreshes_and_has_a_size_bound():
    with patch.object(app, "api", return_value={"private": False}), patch.object(app.repo_vibe, "fetch_stats", return_value={}) as fetch, patch.object(app.repo_vibe, "render_svg", side_effect=["first", "fresh", "second"]), patch.object(app.time, "monotonic", side_effect=[0, 1, 301, 302]), patch.object(app, "MAX_CACHE_ENTRIES", 1):
        assert request() == (200, "first")
        assert request() == (200, "first")
        assert request() == (200, "fresh")
        assert request(repo="another") == (200, "second")
        assert fetch.call_count == 3
        assert len(app._cache) == 1


def test_midnight_invalidates_today_activity():
    with patch.object(app, "api", return_value={"private": False}), patch.object(app.repo_vibe, "fetch_stats", return_value={}) as fetch, patch.object(app.repo_vibe, "render_svg", return_value="svg"), patch.object(app.time, "strftime", side_effect=["2026-11-04", "2026-11-05"]):
        request()
        request()
        assert fetch.call_count == 2


def test_missing_visibility_and_upstream_error_fail_closed():
    for info in ({}, {"private": "false"}):
        with patch.object(app, "api", return_value=info), patch.object(app.repo_vibe, "fetch_stats") as fetch:
            assert request()[0] == 404
            fetch.assert_not_called()
    with patch.object(app, "api", side_effect=RuntimeError("sensitive upstream text")):
        status, body = request()
        assert status == 503
        assert "sensitive" not in body


def test_invalid_name_is_rejected_before_network():
    with patch.object(app, "api") as api:
        assert request(repo="%2e%2e")[0] == 400
        assert request(owner="..")[0] == 400
        api.assert_not_called()


def test_bad_webhook_lengths_do_not_read_body():
    for value, expected in (("bad", 400), ("-1", 400), (str(app.MAX_WEBHOOK_BYTES + 1), 413)):
        handler = object.__new__(app.H)
        handler.path = "/webhook"
        handler.headers = {"Content-Length": value}
        handler.rfile = io.BytesIO(b"test")
        result = []
        handler._send = lambda status, *args: result.append(status)
        handler.do_POST()
        assert result == [expected]
        assert handler.rfile.tell() == 0
