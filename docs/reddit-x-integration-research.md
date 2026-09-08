# Horizon 接入 X(Twitter) / Reddit 调研报告

日期：2026-09-08 00:40 · 结论先行：**两源都能接，Reddit 免费零成本今天就通，X 有免费与付费两条路，推荐"Playwright+Cookie 自抓"起步、不花钱，量大再升级第三方 API。**

---

## 一、Horizon 自带能力盘点（不用自己写代码）

Horizon 内置 12 个采集器，其中就包括 reddit 和 twitter 两套：

| 源 | 内置实现 | 依赖 | 现状（本机实测） |
|---|---|---|---|
| **Reddit** | `src/scrapers/reddit.py`：三级降级（old.reddit HTML → .json API → .rss） | 无需登录 | ⚠️ 网关代理挡 reddit.com（CONNECT 403）；剥代理后实测：`.json`/old HTML 已被 reddit 风控（403/强制登录），**.rss 用浏览器 UA 可用（200，真内容）** |
| **X/Twitter** | 双模式：`apify`（第三方云抓取，需 APIFY_TOKEN）/ `playwright`（本机无头浏览器+Cookie，免费） | playwright + stealth + Chromium + 导出的 x_cookies_*.json | 本机未装 twitter extra（playwright 缺失），需 `uv sync --extra twitter && uv run playwright install chromium` |

配置入口：`data/config.json` → `sources.reddit` / `sources.twitter`（官方示例里都有现成模板，twitter 默认 `mode: apify`，可改 `playwright`）。

---

## 二、Reddit：免费方案，今天就通

**结论：可以，且零成本。**

1. **首选：走 RSS 路径（实测通）**。`.json` 和 old.reddit 都被风控了，但 `https://www.reddit.com/r/<sub>/new/.rss` 带浏览器 UA 返回 200、内容真实（实测 r/LocalLLaMA 返回完整帖子流）。注意两个坑：
   - Horizon 内置 Reddit scraper 的 UA 是浏览器串，理论上可用，但**当前被网关代理挡住**——Horizon 必须继续以"剥代理变量"方式跑，与已落地的修复一致。
   - Reddit 对 IP 有速率限制（实测连续两次请求触发 429，窗口约 23s），scraper 内置了多级降级，能扛；不要把 subreddits 配太多。
2. **次选：RSS 通用源**。`sources.rss` 里直接加 `https://www.reddit.com/r/<sub>/.rss`，把它当普通 RSS——这条路连 reddit scraper 都不用动，最稳。
3. **付费/官方路径**：Reddit Data API（OAuth）官方支持，但需要注册开发者应用+token 管理，对"每日聚合"场景属于杀鸡用牛刀。

**建议动作**：config 里启用 reddit，订阅 3-5 个与项目相关的 sub（候选：`r/artificial`、`r/LocalLLaMA`、`r/SideProject`、`r/socialmedia`），min_score 放宽到 20（reddit 不像 HN 全是高分帖）。

---

## 三、X(Twitter)：能接，但分免费/付费两条路

X 的公共 API 已死，2026 年所有"免费抓推"本质都是逆向或残次通道。按成本从零到高：

### 路线 A：Playwright + Cookie（免费，Horizon 原生支持，推荐起步）
- 原理：无头 Chromium 加载 x.com，用你登录导出的 Cookie 模拟浏览，抓指定用户时间线。
- 前置：① `uv sync --extra twitter` + `playwright install chromium`；② 你在浏览器登录 x.com，用 "Get cookies.txt" 类扩展导出 JSON 存到 `data/x_cookies_1.json`（.gitignore 已排除，不会泄露）；③ config 改 `twitter.mode = "playwright"`。
- 优点：零成本、Horizon 原生、抓的是完整时间线。
- 风险：**用你自己的账号 cookie 有被 X 风控标记的理论风险**（读操作、低频、单账号，实际风险低）；cookie 有时效，隔段时间需重导。
- 可靠性：中等偏上（Horizon 作者从 Apify 迁移到这条路线，说明 Apify scweet 已经先废了）。

### 路线 B：Apify 第三方 Actor（付费，量大才考虑）
- Horizon 的 `apify` 模式对接的 `altimis/scweet` actor 已基本失效（作者都弃了）。
- 现役替代：Apify 市场 `scrapesage/twitter-scraper`（$1.1/千推，免登录免 cookie，有 monitor 模式），或 `twitterapi.io`（$0.15/千推，PAYG）。
- 适合：账号列表 >20 个、或需要搜索/评论抓取的规模化场景。对接 Horizon 需要小改 scraper（换 actor id 与入参映射，工作量 1-2 小时）。

### 路线 C：免费单推通道 FxTwitter（零成本但只解决"单条"）
- 实测：`api.fxtwitter.com/<user>` 只返回用户资料不含推文列表；`api.fxtwitter.com/<user>/status/<id>` 抓单条推文稳定可用。
- 用途：配合"从别处拿到推文 URL 再补正文"的场景（如 RSS 里只有链接时补全内容），不能独立做时间线监控。

### 路线 D：X 官方 API（不推荐）
- 2026 年改为按量计费（约 $0.005/条读，免费层仅够测试），且基础套餐价格砍掉了多数小团队。读场景性价比最低，直接排除。

### 已排除
- **Nitter**：官方项目归档，公共实例全灭（实测 nitter.net RSS 返回 410，其余实例连接失败），社区 fork 也未恢复。别投入。

---

## 四、推荐方案（组合拳）

| 优先级 | 方案 | 成本 | 建议时机 |
|---|---|---|---|
| **P0 今天就做** | Reddit：RSS 通用源方式接入 3-5 个 sub | ¥0 | 下次跑 Horizon 前改 config 即可 |
| **P0 今天就做** | X：装 twitter extra + 导 cookie + playwright 模式，先订 5-10 个关键账号 | ¥0 | 同上，多花 15 分钟导 cookie |
| P1 观察 | playwright 被风控/cookie 频繁过期时 → 迁移 twitterapi.io（$0.15/千推） | ~¥0.1/天 | 出现问题再动 |
| P2 不动 | 官方 API / Nitter | — | 排除 |

## 五、风险与边界

### 补充实测（00:59–01:59）：Reddit 限流比预想更凶，纯 RSS 多源方案有缺陷

- **IP 级限流确认**：串行拉 5 个 sub（2s 间隔），第 1 个 200，后 4 个全部 429；换 UA 无效（排除 UA 封锁）；45s 后同 UA 重试 200 恢复。→ 限流窗口约 30-45s/请求，与 UA 无关，纯 IP 维度。
- **推论**：直接往 Horizon `sources.rss` 塞多条 sub 的 RSS 会大面积 429 失败（scraper 抓取间隔远小于 45s）。
- **修正后的方案**：
  - A（推荐，零账号）：给 fork 的 rss scraper 打补丁——Reddit 源串行 + 45s 间隔 + 429 等待重试；5 sub 约多花 4 分钟。
  - B（最正统，需 Reddit 账号）：注册官方 Data API script app（免费 OAuth，100 QPM），JSON 富数据，逛版块+搜索一并解决。
  - C（不推荐）：第三方付费 Reddit API，这个量级用不上。

1. **合规**：个人聚合分析用途，低频读取公开内容，属灰色但普遍做法；不要用于 resale 或高频爬取。
2. **账号安全**：cookie 方式只读不写，且 X 风控主要打击批量注册号；用主号有小概率触发验证，介意可注册小号专门用于导 cookie。
3. **稳定性**：X 前端结构随时会变，playwright 路径需要 Horizon 作者跟进更新；这正是 P1 备胎存在的意义。

---
附：实测数据快照（2026-09-08 00:33，本机直连）
- reddit .rss（浏览器UA）：200，内容真实 ✓
- reddit .json / old.reddit：403 / 强制登录 ✗
- nitter.net：410 Gone ✗
- x.com：200（可达，但解析需浏览器）
- api.fxtwitter.com：用户资料 200 / 单推 200 / 时间线 ✗
- 网关代理：reddit 与 x.com 全部 CONNECT 403，Horizon 必须剥代理跑
