import json, xml.etree.ElementTree as ET
import repo_vibe, app

def test_mood():
    assert repo_vibe.mood_for(["Add verified receipts, tests pass"])[0] == "LOCKED IN"
    assert repo_vibe.mood_for(["Fix bug, revert broken crash"])[0] == "DEBUGGING"
    assert repo_vibe.mood_for(["Update training controls"])[0] == "GRINDING"
    assert repo_vibe.mood_for([])[0] == "IDLE"

def test_milestone():
    assert repo_vibe.next_milestone(0) == 10
    assert repo_vibe.next_milestone(9) == 10
    assert repo_vibe.next_milestone(10) == 25
    assert repo_vibe.next_milestone(1000) == 2500

def test_svg_is_valid_xml_with_real_numbers():
    stats = {"owner": "sa6ag9", "repo": "Savage-forge", "stars": 0,
             "lines_today": 8151, "commits_today": 5, "build": "SUCCESS",
             "messages": ["Add verified stdlib evaluation"]}
    svg = repo_vibe.render_svg(stats)
    ET.fromstring(svg)  # raises if malformed
    assert "8151" in svg and "SUCCESS" in svg and "Star Meter" in svg or "STAR METER" in svg

if __name__ == "__main__":
    test_mood(); test_milestone(); test_svg_is_valid_xml_with_real_numbers()
    print("all tests passed")
