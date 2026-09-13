"""回归测试：外发渠道的「全文版」链接必须带当日日期。

背景：飞书推送两次把站点根链接当作全文版链接发出（2026-09-12/13），
根因是 render_feishu 复用了首页常量 SITE_URL 而非当日 permalink。
本测试锁定：任何日期下生成的推送文本，全文版链接必须是当日深链接。
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from daily_pipeline import render  # noqa: E402
from daily_pipeline.fetch import ContentItem  # noqa: E402


def _item() -> ContentItem:
    return ContentItem(
        title="t", url="https://example.com/x", src="X/@a", cat=1, score=6, category=1
    )


def test_daily_post_url_composes_date():
    assert render.daily_post_url("2026-09-13") == (
        "https://whitejadesoup.github.io/Horizon/daily/2026/09/13/summary-zh.html"
    )


def test_feishu_fulltext_link_has_date():
    text = render.render_feishu(
        [_item()], {}, {}, "2026-09-13", 100, 1, top_per_section=3
    )
    link_line = next(l for l in text.split("\n") if "全文版" in l)
    assert "daily/2026/09/13/summary-zh.html" in link_line
    # 不允许退化为站点根链接（以日期文件名结尾才算深链接）
    assert link_line.rstrip().endswith("summary-zh.html")


def test_feishu_link_tracks_different_date():
    text = render.render_feishu(
        [_item()], {}, {}, "2027-01-02", 100, 1, top_per_section=3
    )
    link_line = next(l for l in text.split("\n") if "全文版" in l)
    assert "daily/2027/01/02/summary-zh.html" in link_line
