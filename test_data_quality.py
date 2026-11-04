from unittest.mock import patch
import xml.etree.ElementTree as ET

import repo_vibe


def test_failed_commit_details_never_render_a_partial_total():
    commit = {"sha": "one", "commit": {"message": "Add feature"}}
    with patch.object(repo_vibe, "_get", side_effect=[
        {"stargazers_count": 4}, [commit], OSError("commit detail unavailable"),
        OSError("workflow lookup unavailable"),
    ]):
        stats = repo_vibe.fetch_stats("owner", "repo")

    assert stats["lines_today"] is None
    assert stats["activity_status"] == "INCOMPLETE"
    assert stats["build"] == "UNKNOWN"
    svg = repo_vibe.render_svg(stats)
    ET.fromstring(svg)
    assert "UNAVAILABLE" in svg
    assert "UNKNOWN" in svg
    assert ">0<" not in svg


def test_empty_successful_workflow_lookup_means_no_ci_runs():
    with patch.object(repo_vibe, "_get", side_effect=[
        {"stargazers_count": 0}, [], {"workflow_runs": []},
    ]):
        stats = repo_vibe.fetch_stats("owner", "repo")

    assert stats["build"] == "NO CI RUNS"
    assert stats["activity_status"] == "COMPLETE"


def test_missing_commit_statistics_are_not_counted_as_zero():
    commit = {"sha": "one", "commit": {"message": "Add feature"}}
    with patch.object(repo_vibe, "_get", side_effect=[
        {"stargazers_count": 0}, [commit], {}, {"workflow_runs": []},
    ]):
        stats = repo_vibe.fetch_stats("owner", "repo")

    assert stats["lines_today"] is None
    assert stats["activity_status"] == "INCOMPLETE"


def test_thirty_commit_ceiling_is_labeled_as_a_sample():
    commits = [
        {"sha": str(i), "commit": {"message": f"Commit {i}"}}
        for i in range(30)
    ]

    def response(path, token=None):
        if path == "/repos/owner/repo":
            return {"stargazers_count": 0}
        if path.startswith("/repos/owner/repo/commits?"):
            return commits
        if "/actions/runs?" in path:
            return {"workflow_runs": []}
        return {"stats": {"total": 2}}

    with patch.object(repo_vibe, "_get", side_effect=response):
        stats = repo_vibe.fetch_stats("owner", "repo")

    assert stats["lines_today"] == 60
    assert stats["activity_status"] == "SAMPLED"
    assert "LATEST 30 COMMITS" in repo_vibe.render_svg(stats)
