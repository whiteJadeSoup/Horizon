"""Horizon 聚合台 · 抓取层
拉取多信源资讯为统一 ContentItem 列表。
信源: HN RSS / Product Hunt RSS / Reddit sub RSS / 中文科技 RSS / X (twitterapi.io)
"""
from __future__ import annotations

import asyncio
import datetime as dt
import html
import json
import logging
import os
import re
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Any, Optional

import feedparser
import httpx

log = logging.getLogger("horizon_daily.fetch")


def _clean_tweet_title(text: str, limit: int = 90) -> str:
    """推特文本 → 单行标题：去换行、去 t.co 链接、压缩空白、截断。"""
    s = re.sub(r"https?://t\.co/\S+", "", text)
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        s = text.strip()
    return s[:limit].rstrip() + ("…" if len(s) > limit else "")

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
REDDIT_RSS = "https://www.reddit.com/r/{sub}/{sort}/.rss"

# 五板块编号
CAT_TECH, CAT_PRODUCT, CAT_TREND, CAT_MONEY, CAT_WORKFLOW = 1, 2, 3, 4, 5
CAT_NAMES = {1: "技术前沿", 2: "创业产品", 3: "创业动态", 4: "赚钱模式", 5: "AI工作流"}


@dataclass
class ContentItem:
    title: str
    url: str
    src: str          # 来源名
    cat: int          # 初始板块归类（可被 LLM 打分覆盖）
    published: Optional[dt.datetime] = None
    score: Optional[float] = None    # LLM 打分后填充
    category: Optional[int] = None   # LLM 归入板块后填充
    extra: dict = field(default_factory=dict)


class SourceConfig:
    """信源配置。默认按已对齐清单。"""

    def __init__(
        self,
        reddit_subs: Optional[list[str]] = None,
        reddit_sorts: Optional[dict[str, str]] = None,
        twitter_queries: Optional[list[str]] = None,
        twitter_handles: Optional[list[str]] = None,
        fetch_hn: bool = True,
        fetch_ph: bool = True,
        cn_feeds: Optional[list[tuple[str, str]]] = None,
    ):
        self.reddit_subs = reddit_subs or [
            "SideProject", "SaaS", "Entrepreneur", "entrepreneurship",
            "startups", "LocalLLaMA", "MachineLearning", "artificial",
            "Startup_Ideas", "sidehustle", "EntrepreneurRideAlong", "juststart",
        ]
        self.reddit_sorts = reddit_sorts or {"default": "top", "LocalLLaMA": "new"}
        # 早期生意信号词(英文)：搜的是「跑通/首客/闷声」瞬间，不是品类词(中转/代充=红海存量)
        self.twitter_queries = twitter_queries or [
            'first paying customer', 'just hit MRR', 'boring business AI',
            'silent cash flow', 'nobody knows this', 'found 10 customers',
            'AI side hustle', 'unsexy business', 'making money with AI',
        ]
        # 实战派优先：砍纯宏观大V(sama/pmarca/tszzl)，换 build-in-public 独立开发者
        self.twitter_handles = twitter_handles or [
            "levelsio", "marc_louvion", "dannypostma", "yongfook",
        ]
        self.fetch_hn = fetch_hn
        self.fetch_ph = fetch_ph
        self.cn_feeds = cn_feeds or [
            ("机器之心", "https://www.jiqizhixin.com/rss"),
            ("量子位", "https://www.qbitai.com/feed"),
            ("V2EX分享创造", "https://www.v2ex.com/feed/create.xml"),
            ("V2EX奇思妙想", "https://www.v2ex.com/feed/ideas.xml"),
        ]


def _strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()


def _parse_dt(s: Optional[str]) -> Optional[dt.datetime]:
    """解析日期字符串为 UTC-aware datetime。feedparser 6.x 移除了 _parse_date，
    改为三层兕底：email.utils(RFC822/RSS 标准) → ISO8601 → feedparser.datetimes。
    解析失败返回 None（调用方按无日期处理）。"""
    if not s:
        return None
    s = s.strip()
    p: Optional[dt.datetime] = None
    try:
        from email.utils import parsedate_to_datetime
        p = parsedate_to_datetime(s)
    except Exception:
        pass
    if p is None:
        try:
            p = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except Exception:
            pass
    if p is None:
        try:
            from feedparser.datetimes import parse_date as _fp_parse
            p = _fp_parse(s)
        except Exception:
            return None
    if p is None:
        return None
    if p.tzinfo is None:
        p = p.replace(tzinfo=dt.timezone.utc)
    return p.astimezone(dt.timezone.utc)


async def fetch_all(cfg: SourceConfig, hours: int = 48) -> list[ContentItem]:
    """抓取所有源。串行执行（Reddit 限流 + 外部源稳定优先）。"""
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)
    items: list[ContentItem] = []
    transport = httpx.AsyncHTTPTransport(retries=2, trust_env=False)
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(30.0), follow_redirects=True,
        headers={"User-Agent": USER_AGENT}, transport=transport,
    ) as client:
        if cfg.fetch_hn:
            await _fetch_hn(client, since, items)
            await asyncio.sleep(1)
        if cfg.fetch_ph:
            await _fetch_ph(client, since, items)
            await asyncio.sleep(1)
        # Reddit 串行（走本地 redlib，无需长冷却；RSS 回退时由 _fetch_reddit_via_rss 自行处理 429）
        for sub in cfg.reddit_subs:
            await _fetch_reddit(client, sub, cfg, since, items)
            await asyncio.sleep(2)
        for name, url in cfg.cn_feeds:
            await _fetch_rss(client, url, name, since, items)
        # YC 孵化器 launches（用户 2026-09-14 指定信源：新入选/新发布公司名单）
        await _fetch_yc_launches(client, since, items)
    # X: twitterapi.io（有 key 才启，401 静默跳过）在 client 生命周期内单独跑
    if os.environ.get("TWITTERAPI_IO_KEY"):
        await _fetch_twitter(cfg, since, items)
    # 去重
    seen: set[str] = set()
    uniq: list[ContentItem] = []
    for it in items:
        k = it.title.lower()[:80]
        if k in seen:
            continue
        seen.add(k)
        uniq.append(it)
    log.info("fetched %d raw items -> %d unique", len(items), len(uniq))
    return uniq


def fetch_all_sync(cfg: SourceConfig, hours: int = 48) -> list[ContentItem]:
    """同步入口：跑事件循环。"""
    return asyncio.run(fetch_all(cfg, hours))


async def _fetch_hn(client: httpx.AsyncClient, since: dt.datetime, out: list[ContentItem]) -> None:
    urls = [
        "https://hnrss.org/frontpage?count=30",
        "https://hnrss.org/newest?q=%22Show%20HN%22&count=20",
    ]
    for u in urls:
        try:
            r = await client.get(u)
            r.raise_for_status()
        except Exception as e:
            log.warning("HN fetch fail %s: %s", u, e)
            continue
        feed = feedparser.parse(r.text)
        for e in feed.entries[:30]:
            p = _parse_dt(e.get("published"))
            if p and p < since:
                continue
            title = html.unescape(e.get("title") or "").strip()
            if not title:
                continue
            is_show = "Show HN" in title
            out.append(ContentItem(
                title=title,
                url=e.get("link", ""),
                src="Show HN" if is_show else "Hacker News",
                cat=CAT_PRODUCT if is_show else CAT_TECH,
                published=p,
            ))
        await asyncio.sleep(1)


async def _fetch_ph(client: httpx.AsyncClient, since: dt.datetime, out: list[ContentItem]) -> None:
    try:
        r = await client.get("https://www.producthunt.com/feed")
        r.raise_for_status()
    except Exception as e:
        log.warning("PH fetch fail: %s", e)
        return
    feed = feedparser.parse(r.text)
    for e in feed.entries[:30]:
        p = _parse_dt(e.get("published"))
        if p and p < since:
            continue
        title = html.unescape(e.get("title") or "").strip()
        if not title:
            continue
        out.append(ContentItem(title=title, url=e.get("link", ""), src="Product Hunt",
                               cat=CAT_PRODUCT, published=p))


async def _fetch_reddit(
    client: httpx.AsyncClient, sub: str, cfg: SourceConfig,
    since: dt.datetime, out: list[ContentItem],
) -> None:
    """优先走本地 redlib（绕 IP 风控 + 缓存），失败回退官方 RSS。"""
    sort = cfg.reddit_sorts.get(sub, cfg.reddit_sorts.get("default", "top"))
    default_cat = CAT_MONEY if sub in ("SaaS", "Entrepreneur", "entrepreneurship", "sidehustle") else (
        CAT_WORKFLOW if sub in ("LocalLLaMA", "cursor", "AI_Agents", "MachineLearning") else CAT_TREND
    )
    redlib_url = os.environ.get("REDLIB_URL", "http://localhost:8080")
    ok = await _fetch_reddit_via_redlib(client, redlib_url, sub, sort, since, default_cat, out)
    if ok:
        return
    # 回退：官方 RSS（串行 + 60s 冷却，限流时降级）
    await _fetch_reddit_via_rss(client, sub, sort, since, default_cat, out)


async def _fetch_reddit_via_redlib(
    client: httpx.AsyncClient, base: str, sub: str, sort: str,
    since: dt.datetime, cat: int, out: list[ContentItem],
) -> bool:
    """从本地 redlib 抓 sub 页面并解析帖子。返回 True 表示成功（即使 0 新帖）。"""
    try:
        url = f"{base}/r/{sub}/{sort}"
        r = await client.get(url, timeout=20.0)
        if r.status_code != 200:
            log.warning("Redlib r/%s http %s; fallback RSS", sub, r.status_code)
            return False
        html_text = r.text
    except Exception as e:
        log.warning("Redlib r/%s fail: %s; fallback RSS", sub, e)
        return False
    # 解析 redlib HTML：h2.post_title > a[href]，作者 u/xxx，created title="... UTC"
    import re as _re
    # 每个 href 在全文中的位置窗口内找 created 时间戳（避免在紧凑页面中张冠李戴）
    _ts_re = _re.compile(r'title="([A-Z][a-z]{2} [ A-Z0-9:]{2,11}[0-9]{4}, [0-9:]{8} UTC)"')
    titles = _re.findall(
        r'<a[^>]*href="(/r/[^"]+/comments/[^"]+)"[^>]*>(.*?)</a>', html_text, _re.S)
    seen_url: set[str] = set()
    count = 0
    for href, title_html in titles:
        title = html.unescape(_re.sub(r'<[^>]+>', ' ', title_html)).strip()
        # 过滤评论计数条目（redlib 把 “N comments” 也渲染成链接）
        if not title or _re.fullmatch(r'\d+\s+comments?', title, _re.I):
            continue
        if title in seen_url:
            continue
        seen_url.add(title)
        full_url = f"https://www.reddit.com{href}" if href.startswith("/") else href
        p = None
        pos = html_text.find(href)
        if pos >= 0:
            m = _ts_re.search(html_text[max(0, pos - 500):pos + 400])
            if m:
                try:
                    p = dt.datetime.strptime(m.group(1), "%b %d %Y, %H:%M:%S UTC").replace(tzinfo=dt.timezone.utc)
                except ValueError:
                    p = None
        if p is None:
            # 解析不出日期的条目（如 top 页面的老贴）一律丢弃，防止多年旧文混入日报
            log.info("Redlib r/%s: drop no-date item %s", sub, title[:40])
            continue
        if p < since:
            continue
        out.append(ContentItem(title=title, url=full_url, src=f"r/{sub}", cat=cat, published=p))
        count += 1
        if count >= 15:
            break
    log.info("Redlib r/%s: %d items", sub, count)
    return True


async def _fetch_reddit_via_rss(
    client: httpx.AsyncClient, sub: str, sort: str,
    since: dt.datetime, cat: int, out: list[ContentItem],
) -> None:
    url = REDDIT_RSS.format(sub=sub, sort=sort)
    for attempt in range(2):
        try:
            r = await client.get(url, headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/atom+xml,application/xml,text/xml,*/*",
            })
            r.raise_for_status()
            break
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429 and attempt < 1:
                wait = 60
                log.warning("Reddit r/%s 429; retry in %ds", sub, wait)
                await asyncio.sleep(wait)
                continue
            log.warning("Reddit r/%s fail: %s", sub, e)
            return
        except Exception as e:
            log.warning("Reddit r/%s fail: %s", sub, e)
            return
    feed = feedparser.parse(r.text)
    for e in feed.entries[:15]:
        p = _parse_dt(e.get("published"))
        if p and p < since:
            continue
        title = html.unescape(e.get("title") or "").strip()
        if not title:
            continue
        out.append(ContentItem(title=title, url=e.get("link", ""), src=f"r/{sub}", cat=cat, published=p))
    # Reddit IP 限流由外层串行+间隔负责


async def _fetch_rss(
    client: httpx.AsyncClient, url: str, name: str, since: dt.datetime, out: list[ContentItem],
) -> None:
    try:
        r = await client.get(url)
        r.raise_for_status()
    except Exception as e:
        log.warning("RSS %s fail: %s", name, e)
        return
    feed = feedparser.parse(r.text)
    for e in feed.entries[:20]:
        p = _parse_dt(e.get("published"))
        if p and p < since:
            continue
        title = html.unescape(e.get("title") or "").strip()
        if not title:
            continue
        out.append(ContentItem(title=title, url=e.get("link", ""), src=name,
                               cat=CAT_TECH, published=p))


async def _fetch_yc_launches(client: httpx.AsyncClient, since: dt.datetime, out: list[ContentItem]) -> None:
    """YC 孵化器 launches：新入选/新发布公司名单（用户 2026-09-14 指定信源）。
    页面内嵌 {"hits":[...]} JSON：title/tagline/batch/created_at/company，每页20条。
    注意：无参数首页=最新排序；?page=N 是另一套排序(旧数据)，不得用翻页参数。
    初始归类 cat=CAT_PRODUCT，由 LLM 打分时再归入 cat2/cat3。"""
    try:
        r = await client.get("https://www.ycombinator.com/launches")
        r.raise_for_status()
    except Exception as e:
        log.warning("YC launches fail: %s", e)
        return
    i = r.text.find('{"hits":')
    if i < 0:
        log.warning("YC launches: no hits JSON")
        return
    try:
        obj, _ = json.JSONDecoder().raw_decode(r.text[i:])
    except ValueError as e:
        log.warning("YC launches JSON parse fail: %s", e)
        return
    for h in obj.get("hits", []):
        try:
            p = dt.datetime.fromisoformat(str(h.get("created_at", "")).replace("Z", "+00:00"))
        except ValueError:
            continue
        if p < since:
            continue
        title = (h.get("title") or "").strip()
        tagline = (h.get("tagline") or "").strip()
        if not title:
            continue
        slug = h.get("slug") or ""
        url = f"https://www.ycombinator.com/launches/{slug}" if slug else "https://www.ycombinator.com/launches"
        batch = (h.get("batch") or "").strip()
        text = f"{title}: {tagline}" if tagline else title
        if batch:
            text = f"{text} [YC {batch}]"
        out.append(ContentItem(
            title=text[:150],
            url=url,
            src="YC",
            cat=CAT_PRODUCT,
            published=p,
        ))


async def _fetch_twitter(cfg: SourceConfig, since: dt.datetime, out: list[ContentItem]) -> None:
    """twitterapi.io 高级搜索：大佬时间线 + 关键词。需 TWITTERAPI_IO_KEY。"""
    key = os.environ.get("TWITTERAPI_IO_KEY")
    if not key:
        log.info("TWITTERAPI_IO_KEY not set; skipping X source")
        return
    since_ts = int(since.timestamp())
    queries: list[str] = []
    for h in cfg.twitter_handles:
        queries.append(f"from:{h} since_time:{since_ts}")
    for q in cfg.twitter_queries:
        queries.append(f'{q} since_time:{since_ts}')
    headers = {"x-api-key": key}
    # 走网关 egress 代理（trust_env=True）以自动注入 secret 明文；verify=False 适配代理的 CA
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0), headers=headers, verify=False, trust_env=True) as client:
        for q in queries:
            try:
                params = {"query": q, "queryType": "Top"}
                r = await client.get("https://api.twitterapi.io/twitter/tweet/advanced_search", params=params)
                if r.status_code == 401:
                    log.warning("twitterapi.io 401 (key invalid/expired); disabling X source")
                    return
                r.raise_for_status()
                data = r.json()
            except Exception as e:
                log.warning("twitterapi.io fail %s: %s", q, e)
                continue
            for t in data.get("tweets", [])[:10]:
                text = (t.get("text") or "").strip()
                if not text:
                    continue
                author = (t.get("author") or {}).get("userName", "x")
                out.append(ContentItem(
                    title=_clean_tweet_title(text),
                    url=t.get("url") or f"https://x.com/{author}/status/{t.get('id')}",
                    src=f"X/@{author}", cat=CAT_TREND,
                    published=dt.datetime.now(dt.timezone.utc),
                    extra={"full_text": text,
                           "likes": t.get("likeCount", 0), "retweets": t.get("retweetCount", 0)},
                ))
            await asyncio.sleep(2)
