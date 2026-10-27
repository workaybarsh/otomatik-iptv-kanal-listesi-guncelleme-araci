# -*- coding: utf-8 -*-
"""Ag gerektirmeyen eslesme testleri."""

import argparse
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import kanal_guncelle as kg  # noqa: E402


def make_channel(tvg_id: str, name: str, url: str) -> kg.Channel:
    return kg.Channel(
        extinf_idx=0,
        url_idx=0,
        extra_idxs=[],
        tvg_id=tvg_id,
        name=name,
        url=url,
    )


def base_source() -> kg.SourceData:
    src = kg.SourceData()
    src.by_channel["ShowTV.tr"] = [
        {
            "channel": "ShowTV.tr",
            "feed": "SD",
            "quality": "1080p",
            "labels": [],
            "url": "http://tr.example/show.m3u8",
        }
    ]
    src.by_channel["ShowTV.pr"] = [
        {
            "channel": "ShowTV.pr",
            "feed": "SD",
            "quality": "1080p",
            "labels": [],
            "url": "http://pr.example/show.m3u8",
        }
    ]
    src.by_name[("TR", "showtv")] = "ShowTV.tr"
    src.by_name[("PR", "showtv")] = "ShowTV.pr"
    return src


def test_no_cross_country_match() -> None:
    src = base_source()
    ch = make_channel("ShowTV.tr@SD", "Show TV", "http://tr.example/show.m3u8")
    keys = kg.resolve_keys(ch, src, allow_name=True)
    assert keys == ["ShowTV.tr"], keys

    args = argparse.Namespace(name_match=True, siblings=False, max_candidates=10)
    urls = [c["url"] for c in kg.gather_candidates(ch, src, args)]
    assert all("pr.example" not in u for u in urls), urls


def test_name_match_is_off_by_default() -> None:
    src = base_source()
    ch = make_channel("ShowTV.tr@SD", "Show TV", "http://tr.example/show.m3u8")
    assert kg.resolve_keys(ch, src, allow_name=False) == ["ShowTV.tr"]


def test_name_match_requires_country() -> None:
    src = base_source()
    ch = make_channel("", "Show TV", "http://tr.example/show.m3u8")
    assert kg.resolve_keys(ch, src, allow_name=True) == []


def test_ambiguous_names_are_ignored() -> None:
    channels = [
        {"id": "A.tr", "name": "Show TV", "country": "TR"},
        {"id": "B.tr", "name": "Show TV", "country": "TR"},
    ]
    index = kg.build_name_index(channels)
    assert ("TR", "showtv") not in index


def test_unique_name_is_indexed() -> None:
    channels = [{"id": "ShowTV.tr", "name": "Show TV", "country": "TR"}]
    index = kg.build_name_index(channels)
    assert index[("TR", "showtv")] == "ShowTV.tr"


def test_same_feed_is_preferred() -> None:
    src = kg.SourceData()
    src.by_channel["ShowTV.tr"] = [
        {
            "channel": "ShowTV.tr",
            "feed": "SD",
            "quality": "1080p",
            "labels": [],
            "url": "http://tr.example/sd1080.m3u8",
        },
        {
            "channel": "ShowTV.tr",
            "feed": "HD",
            "quality": "720p",
            "labels": [],
            "url": "http://tr.example/hd720.m3u8",
        },
    ]
    args = argparse.Namespace(name_match=False, siblings=False, max_candidates=10)
    ch = make_channel("ShowTV.tr@HD", "Show TV", "http://tr.example/old.m3u8")
    cands = kg.gather_candidates(ch, src, args)
    assert cands[0]["feed"] == "HD", cands


def test_keyword_guard() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "other.m3u").write_text("#EXTM3U\n", encoding="utf-8")
        (base / "guncel-test.m3u").write_text("#EXTM3U\n", encoding="utf-8")

        old_config = kg.PLAYLIST_CONFIG
        kg.PLAYLIST_CONFIG = base / "playlist.txt"
        try:
            chosen = kg.find_target_playlist(None, base)
            assert chosen.name == "guncel-test.m3u", chosen
        finally:
            kg.PLAYLIST_CONFIG = old_config


def test_keyword_guard_refuses_other_playlists() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "other.m3u").write_text("#EXTM3U\n", encoding="utf-8")

        old_config = kg.PLAYLIST_CONFIG
        kg.PLAYLIST_CONFIG = base / "playlist.txt"
        try:
            try:
                kg.find_target_playlist(None, base)
            except SystemExit:
                pass
            else:
                raise AssertionError("keyword olmayan playlist kabul edilmemeliydi")
        finally:
            kg.PLAYLIST_CONFIG = old_config


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests:
        test()
        print(f"OK  {test.__name__}")
    print(f"\n{len(tests)} test gecti.")
