import os
from unittest.mock import patch
from urllib.error import HTTPError
import app


def request(owner="example", repo="project"):
    handler = object.__new__(app.H)
    handler.path = f"/badge/{owner}/{repo}"
    result = []
    handler._send = lambda status, body, ctype=None: result.append((status, body))
    handler.do_GET()
    return result[0]


def setup_function():
    app._cache.clear()


def test_public_badge_uses_only_public_data():
    # Even with a privileged-looking token sitting in the environment, the
    # badge path must not use it: stats are fetched with token None, always.
    with patch.dict(os.environ, {"GITHUB_TOKEN": "synthetic-privileged-token"}), \
         patch.object(app, "api", return_value={"private": False}) as visibility, \
         patch.object(app.repo_vibe, "fetch_stats", return_value={"public": True}) as fetch, \
         patch.object(app.repo_vibe, "render_svg", return_value="<svg/>"):
        assert request() == (200, "<svg/>")
        visibility.assert_called_once_with("/repos/example/project")
        fetch.assert_called_once_with("example", "project", None)


def test_retired_app_auth_machinery_is_gone():
    # The GitHub App auth path (App JWT, installation tokens, env-token
    # fallback) and the App manifest builder were dead code since the setup
    # flow was retired behind 410 responses. They stay removed: no token
    # code path exists in the server to wire back up.
    for name in ("make_jwt", "installation_token", "token_for", "manifest",
                 "_installations"):
        assert not hasattr(app, name), name


def test_inaccessible_repository_never_returns_cached_badge():
    app._cache[("example", "project")] = "<svg>synthetic-private-data</svg>"
    denied = HTTPError("https://example.invalid", 404, "not found", {}, None)
    with patch.object(app, "api", side_effect=denied), \
         patch.object(app.repo_vibe, "fetch_stats") as fetch:
        status, body = request()
        assert status == 404
        assert "synthetic-private-data" not in body
        assert ("example", "project") not in app._cache
        fetch.assert_not_called()


def test_visibility_is_checked_on_every_cached_request():
    with patch.object(app, "api", side_effect=[{"private": False}, {"private": True}]), \
         patch.object(app.repo_vibe, "fetch_stats", return_value={"public": True}), \
         patch.object(app.repo_vibe, "render_svg", return_value="<svg/>"):
        assert request()[0] == 200
        assert request()[0] == 404
