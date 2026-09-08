# 聚合台工程总结（Horizon @ whiteJadeSoup）

_2026-09-08 02:12 · The John Constantine 与小彬共同建设_

---

## 一、目标

**一句话**：每天早上醒来，一份自动生成的报告告诉我——过去 24-48 小时，科技圈/AI 圈/我的三个项目（小红书运营、抖音发掘、创业点子寻找）相关的信息场里，**真正值得看的东西**是什么，别人在聊什么。

拆开是三层：

1. **降噪**：信息源很多（HN/Reddit/X/RSS），垃圾占 90%。AI 打分（0-10），只留 ≥6 分的。
2. **补背景**：入选内容不只有标题——AI 补齐「它是什么 / 为什么重要 / 社区怎么吵」，不用点出去自己查。
3. **可回溯**：报告挂在自己网站上，任何一条带原文链接，随时翻历史。

**非目标（现阶段）**：不做实时推送、不做多用户、不做原创内容生成——它是「每天一期的信息筛子」，不是「新闻编辑部」。

---

## 二、架构

```
┌─────────────── 信息源层（5 通道）───────────────┐
│  Hacker News   Reddit(官方API/接)   X(接)        │
│  RSS(极客公园/爱范儿/自定义搜索源)  GitHub/其他   │
└──────────────────────┬───────────────────────────┘
                       ↓ 抓取（去重合并）
┌─────────────── AI 加工层（豆包/方舟）────────────┐
│  打分 0-10 → 阈值过滤(6.0) → 背景 enrichment    │
│  （每条配 web_search 查背景+社区讨论）           │
└──────────────────────┬───────────────────────────┘
                       ↓
┌─────────────── 产出层 ──────────────────────────┐
│  ① 日报 Markdown（data/summaries/）             │
│  ② GitHub Pages 站点（whitejadesoup.github.io） │
│  ③ 飞书推送（要点+网址，准时）                   │
└─────────────────────────────────────────────────┘
```

**运行形态**（关键工程决策）：

- 本体：开源项目 [Thysrael/Horizon](https://github.com/Thysrael/Horizon)（Python/uv），fork 到 [whiteJadeSoup/Horizon](https://github.com/whiteJadeSoup/Horizon) 自持。
- 部署：**Mac 本机跑**（`.venv` + uv），不用云服务器——AI 打分走方舟 API，Pages 托管在 GitHub。
- 调度：手动触发或 cron，跑的时候**双 fork 脱离会话树 + 剥代理变量**（血泪教训：网关重启会杀子进程，代理会挡所有源）。
- 身份：git 提交用 whiteJadeSoup，Pages 源=gh-pages 分支。

**踩过的坑（已固化成规则）**：

| 坑 | 修法 |
|---|---|
| gateway 重启连带杀掉跑一半的任务 | 双 fork（`(cmd &)`）脱离进程树 |
| 网关代理 CONNECT 403 挡所有聚合源 | `env -u` 剥 HTTP(S)_PROXY 再跑 |
| Reddit IP 级限流（45s/请求） | 用户拍板：官方 Data API（免费 OAuth）替换 RSS |
| Pages 源设 main 分支 → posts 404 | 切 gh-pages 分支 + 手动触发 build |
| .gitignore 挡日报入库 | `!docs/_posts/2026-*` 放行 |

---

## 三、产物

**每天一份数字日报**，含四个信息面：

| 板块 | 来源 | 状态 |
|---|---|---|
| 科技要闻（9 条 7 分+） | Hacker News + 极客公园 + 爱范儿 | ✅ 已上线（09-07 首期） |
| Reddit 版块精华 | 5 个 sub（SideProject/artificial/AIAgents/InternetIsBeautiful/socialmedia） | 🔧 等 Reddit API 凭证，就差第一步注册 |
| X 时间线（盯人） | Playwright + Cookie（免费） | 🔧 等导出 cookie |
| X 关键词搜索 | twitterapi.io（$0.15/千推，$1 够数月） | 🔧 方案已定，待注册拿 key |

**今日成果（09-07 期）**：34 条抓取 → 14 条入选 → https://whitejadesoup.github.io/Horizon/2026/09/07/summary-en.html

**成本**：LLM 调用走方舟套餐（已含）+ Pages/仓库免费 + Reddit API 免费 + X 搜索 $1/数月 ≈ **每天不到 1 块钱**。

**衍生资产**（顺带建成）：
- `docs/reddit-x-integration-research.md`：X/Reddit 全方案调研（含实测数据）
- 自持 fork + CI 部署链路：以后任何改动 push 即上线
- 飞书推送规范：要点+网址，已成 USER.md 长期规则

---

## 四、下一步（按优先级）

1. **明天**：日报常态跑 + 飞书准时推送（要点+链接）
2. **等凭证**：Reddit API 注册（你，10 分钟）→ 我改 scraper；X cookie 导出；twitterapi.io key（可选，$1）
3. **本周**：日报中文化（对选题更友好）；源清单按三项目调优
4. **衍生**：日报里筛出的「Reddit 真实痛点/用户需求」单独摘出来 → 喂给创业点子库

_这个文档跟着工程走，架构变了更新它。_
