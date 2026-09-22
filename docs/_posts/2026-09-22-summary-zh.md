---
layout: post
title: "Horizon 创业日报 · 2026-09-22"
date: 2026-09-22
categories: daily
---

## TLDR

### 核心看点

- 亚马逊封禁Meta的Muse AI代理在其平台购物，平台与AI代理的'客户归属权'之争正式开打：当代理替用户下单，平台失去的是流量入口与用户关系，Agent创业者需尽早评估对大平台的依赖风险。
- 华为因国内算力需求远超产能而暂缓昇腾芯片出海，叠加三星HBM4扩产，AI算力与存储的供需缺口仍在扩大，国产算力'自用优先'正在重塑全球供应链格局。
- 今日多条变现案例（短剧30天12万美元、19岁卖AI服务月收15万、微SaaS17天百万流水）共同指向一个结论：AI时代赚钱的核心是销售与分发能力而非技术本身，且流水不等于收入，交付与留存才是真门槛。
- 融资4.16亿美元、4.65亿卖身、创始人分文未得的极端案例引发热议，配合'多数创业公司其实不需要VC'的讨论，清算优先权与融资结构正在被创业者重新审视。

### 趋势分析

- Agent正从'能聊'走向'能做'：谷歌开源AX编排框架、Grok快速迭代、推理工程师成最抢手岗位、大模型被注入机器人本体，基建全面加速；但亚马逊封杀Meta代理说明商业化落地必撞平台墙——创业者的机会在垂直场景与自有渠道，而非寄生于他人流量。
- 小模型+开源正以垂直与端侧取胜：1亿参数文生图宣称SOTA、27B写作模型、8GB显存可训的持续学习模型、俄系与国产开源模型密集入场——前沿能力不再是巨头专属，创业者可用低成本小模型做垂直差异化，本地化部署成为新战场。
- 创业叙事正从'融资驱动'转向'盈利与分发驱动'：独立开发者变现案例井喷、MVP被重新定义为'最快验证核心假设的实验'、爆款帖直言分发是生死线——对创业者的含义是：先验证谁付钱再谈规模化，把销售能力当作第一优先级来建设。


## 一、技术前沿发展

### [Grok 4.7](https://x.ai/news/grok-4-7) ⭐️ 7.0/10 · Hacker News

- **概述**：xAI推出Grok 4.7版本，延续其数周级的高频迭代节奏。新版本在推理、编程与实时信息处理能力上进一步提升，并深度绑定X平台的数据与分发生态。
- **分析**：xAI以极快速度追赶OpenAI和Google，说明前沿模型竞争已进入小步快跑、持续压强的阶段。Grok背靠X的实时数据流与Colossus超算集群，在时效性场景具备独特优势。头部模型密集发布将持续压低API价格，加速基础能力的商品化。
- **思考**：创业者应把模型能力视为持续贬值的资源，避免在易被下一代模型覆盖的单点能力上重投入。可关注Grok实时数据优势衍生的新场景，如舆情监测、金融信息类产品。

### [AX – Google’s Open Agentic Orchestrator](https://agentexecutor.io) ⭐️ 7.0/10 · Hacker News

- **概述**：谷歌开源了名为AX的智能体编排器，用于协调和管理多个AI Agent的协作与执行。开发者可基于它快速搭建生产级的多智能体工作流。
- **分析**：谷歌亲自下场做Agent编排层，说明多智能体系统正从概念验证走向生产级基础设施。其开源策略意在抢占开发者心智，复制Android、Kubernetes式的生态打法。编排层是Agent技术栈中粘性较高的环节，巨头入场将挤压纯框架类创业公司的空间。
- **思考**：创业者不必自研编排框架，可直接基于AX等开源基建快速构建应用。真正的护城河应放在垂直场景的数据积累、工作流理解和行业交付能力上。

### [Show HN: Mini-AGI – Dynamic continual learning model trained on 8GB VRAM](https://github.com/volotat/mini-AGI/) ⭐️ 6.0/10 · Show HN

- **概述**：有开发者在Hacker News展示Mini-AGI项目，这是一个支持动态持续学习的模型，可在8GB显存的消费级显卡上完成训练。项目展示了低成本实现模型持续进化的可行路径。
- **分析**：持续学习是大模型的长期痛点，主流模型的知识更新目前依赖昂贵的重训练。若8GB显存即可实现动态学习，意味着个人开发者和小团队能构建越用越聪明的私有模型。该方向若成熟，将催生个性化AI与边缘AI的新创业机会。
- **思考**：创业者可关注小模型加持续学习的路线，在私有数据、个人助理等场景做出差异化。同时需冷静验证其实际效果与主流模型的差距，避免被demo效果迷惑。

### [GPT-6 Astra开进机器人身体！清华联手无问芯穹等开源RPent](https://www.qbitai.com/2026/09/493218.html) ⭐️ 6.0/10 · 量子位

- **概述**：清华大学联合无问芯穹等机构开源RPent项目，将GPT-6 Astra大模型接入机器人身体，实现大模型驱动的具身智能。这标志着国产大脑加本体结合的具身智能开源方案落地。
- **分析**：具身智能是当前最热赛道之一，开源VLA类模型正在快速降低机器人智能化的门槛。清华的学术力量与无问芯穹的算力基础设施结合，体现了高校加AI基建公司协同的产业模式。开源将加速国内机器人创业公司迭代，缩小与海外头部具身智能团队的差距。
- **思考**：具身智能创业可站在开源肩膀上，把资源集中在场景选择、数据回收和本体工程上。机器人加垂直场景如物流、巡检、服务，是更务实的切入点。

### [开源Top2！实测阶跃Step 5 Preview，真有点猛啊…](https://www.qbitai.com/2026/09/493179.html) ⭐️ 6.0/10 · 量子位

- **概述**：阶跃星辰发布Step 5 Preview，实测表现冲进开源模型Top2，媒体评价其能力相当强劲。这延续了国产开源模型在榜单成绩与实际体验上双双突破的势头。
- **分析**：阶跃星辰以多模态起家，Step 5的突破说明其通用能力已跻身开源第一梯队，与DeepSeek、Qwen形成国产开源多强格局。开源头部位置意味着开发者迁移成本低、生态吸引力强，将直接争夺应用开发者的默认选择。国产模型能力逼近的同时保持价格优势，利好国内应用层创业。
- **思考**：创业者选型时可扩大国产开源模型的备选池，通过多模型AB测试压低成本、避免单一依赖。模型竞争越激烈，应用层的议价能力和窗口期越好。

### [yandex/AliceAI-Foundation-80B-A3B-Base: Russian-developed competitor to Qwen 35B and DeepSeek V4 Flash](https://www.reddit.com/r/LocalLLaMA/comments/1wmmnrt/yandexaliceaifoundation80ba3bbase/) ⭐️ 6.0/10 · r/LocalLLaMA

- **概述**：Yandex发布开源基础模型AliceAI-Foundation-80B-A3B-Base，采用总参数80B、激活约3B的MoE架构，直接对标Qwen同级与DeepSeek V4 Flash。这是俄罗斯科技公司在开源大模型赛道的重要落子。
- **分析**：继DeepSeek、Qwen之后，俄罗斯也加入高性价比开源模型竞争，全球开源格局进一步多极化。小激活的MoE设计延续了低成本高吞吐的推理路线，说明该架构范式已成国际共识。地缘因素影响下，俄语区市场可能形成相对独立的模型生态。
- **思考**：开源模型供给越充分，推理成本越低，应用层创业窗口越大。做出海产品时可评估多语言、多区域的模型组合，降低对单一生态的依赖。

### [[MASSIVE RELEASE] Supra2-IMG - a tiny 100M text-to-image model - SOTA quality and open release!](https://www.reddit.com/r/LocalLLaMA/comments/1wmftr3/massive_release_supra2img_a_tiny_100m_texttoimage/) ⭐️ 6.0/10 · r/LocalLLaMA

- **概述**：社区发布Supra2-IMG，一个仅100M参数的文生图模型，宣称以极小体积达到SOTA级生成质量并完全开源。相比动辄数十亿参数的主流文生图模型，体积缩小了两个数量级。
- **分析**：若质量属实，这将大幅降低图像生成的部署成本，让手机和嵌入式设备本地生图成为可能。小模型路线挑战了大力出奇迹的规模逻辑，说明架构与数据创新仍有巨大红利。端侧生图在隐私、延迟、成本上优势明显，将打开新的应用空间。
- **思考**：创业者可优先探索端侧图像生成场景，如相机滤镜、电商素材、隐私敏感行业等。端侧AI应用天然规避API成本，商业模式上可考虑硬件授权或订阅制。

### [we put out a 27b writing model, open weights, eq-bench 4 at 1330](https://www.reddit.com/r/artificial/comments/1wlt16o/we_put_out_a_27b_writing_model_open_weights/) ⭐️ 6.0/10 · r/artificial

- **概述**：一个团队发布27B参数的开放权重写作模型，在创意写作基准EQ-Bench 4上取得1330分。该模型专注文学与长文本创作，用更小的体积在垂直任务上对标通用旗舰模型。
- **分析**：EQ-Bench是社区公认的创意写作评测，1330分说明专用模型在垂直领域能以小博大。写作类模型验证了通用底座加垂直微调路线的商业价值，创作需求付费意愿强、场景清晰。开源策略有助于快速建立开发者社区和产品口碑。
- **思考**：垂直小模型加开源是中小团队的可行打法，应选一个付费意愿强的场景做深。中文网文、剧本、营销文案等创作场景同样存在机会，关键在数据质量与风格控制。


## 二、创业产品

### [Google Flow for iOS & Android](https://www.producthunt.com/products/google) ⭐️ 6.0/10 · Product Hunt

- **概述**：谷歌将其AI电影制作工具Flow正式推出iOS和Android版本。Flow基于Veo视频模型，此前仅限网页端，移动化意味着用户可随时随地生成与剪辑AI视频。这延续了AI视频工具从专业桌面走向大众口袋的趋势。
- **分析**：谷歌把Flow推向移动端，说明AI视频的下一战场在手机：创作门槛越低，用户规模越大，数据飞轮越快。移动端也是订阅付费和社交分发的天然场景。国内可灵、即梦、海螺等已深耕移动端，谷歌入场将加剧全球竞争，也验证了该赛道的天花板足够高。
- **思考**：纯视频生成工具的窗口正在关闭，大厂模型加渠道的碾压下，机会转向垂直工作流如电商、短剧、广告与本地化运营。与其拼模型，不如拼场景和分发。

### [NiubiGEO](https://www.producthunt.com/products/niubigeo) ⭐️ 6.0/10 · Product Hunt

- **概述**：NiubiGEO在Product Hunt发布，是一款GEO（生成式引擎优化）工具，帮助品牌优化内容，让ChatGPT、Perplexity、AI Overviews等AI引擎在回答时引用并推荐自己。产品名Niubi直接使用中文网络梗，疑似华人团队出海作品。
- **分析**：当用户搜索习惯从Google转向AI对话，传统SEO逻辑失效，被AI引用成为新的流量入口，GEO正从概念变成真金预算。该赛道尚处早期，工具、方法论、计价标准都未定型，先发者有机会定义品类。名字用Niubi既是记忆点，也反映中国创业者出海时越来越自信的文化输出。
- **思考**：创业者应尽早关注GEO：一方面可将其作为低成本获客手段，优化产品在AI回答中的呈现；另一方面GEO工具本身是新兴市场，可观察其付费意愿与续费率再决定是否入局。

### [Capsule 26 - An AI agent that must pay for its own API calls or shut down. Public ledger, day 4, zero sales. How would you get it to earn?](https://www.reddit.com/r/SideProject/comments/1wm2h39/capsule_26_an_ai_agent_that_must_pay_for_its_own/) ⭐️ 6.0/10 · r/SideProject

- **概述**：一位开发者在Reddit发起实验：名为Capsule 26的AI代理必须靠自己的收入支付API调用费用，赚不到钱就自动关机，全程公开账本。截至第4天销售额为零，作者向社区征集让代理赚钱的方法。这本质是一场AI代理经济生存挑战。
- **分析**：这类实验直击AI代理落地的核心难题：代理能否自主完成真实商业闭环，而不只是演示。零收入说明当前代理在获客、信任、支付环节仍有硬伤，人类监督仍不可少。但公开账本本身就是内容营销，实验的叙事价值可能超过商业价值，作者已借此获得社区关注。
- **思考**：代理创业别只堆能力，先想清楚谁付钱、为什么付。同时公开过程是低成本获客利器，build in public的叙事往往比产品本身更早带来流量。

### [I built unfill.io — drop a meeting recording, get a real .pptx you can present](https://www.reddit.com/r/EntrepreneurRideAlong/comments/1wlqmjc/i_built_unfillio_drop_a_meeting_recording_get_a/) ⭐️ 6.0/10 · r/EntrepreneurRideAlong

- **概述**：开发者在Reddit分享其新产品unfill.io：用户上传会议录音，系统自动转录、提炼要点并生成一份真实可编辑、可演示的.pptx演示文稿。它瞄准开完会要做汇报材料这一高频痛点，输出的是真正的PowerPoint文件而非网页版幻灯片。
- **分析**：会议录音转PPT的巧思在于切入具体工作流：会后向领导或客户同步结论是刚需，且.pptx格式保证了与企业现有流程的兼容。AI幻灯片赛道已有Gamma、AiPPT等众多玩家，但多数从文本或文档生成，从录音切入的差异化明确。风险在于生成质量与模板美观度决定留存，且大厂办公套件随时可能内置同类功能。
- **思考**：在拥挤的AI生成赛道，换一个输入源如录音、邮件、代码库就能切出新场景。优先输出客户已有格式，降低迁移成本，比重新发明文档更容易被买单。

### [Show HN: Lossless-memory – a personal AI memory that never summarizes](https://github.com/aru-labs/lossless-memory) ⭐️ 6.0/10 · Show HN

- **概述**：一款名为Lossless-memory的个人AI记忆产品在Show HN发布，核心卖点是永不总结。与多数AI记忆方案通过摘要压缩历史不同，它完整保留原始对话与上下文细节。作者认为摘要必然丢失信息，无损存储才能让AI真正记住用户。
- **分析**：当前主流AI记忆功能普遍依赖摘要压缩，长期使用会丢失细节，这是真实存在的用户痛点。无损记忆的技术挑战在于检索与成本：数据无限增长时如何高效召回并控制token开销。若能解决，记忆层可能成为AI应用的护城河和个人数据资产。该方向已有Mem0、Letta等玩家，竞争正在加速。
- **思考**：AI记忆是基础设施级机会，但通用方案难敌大厂，创业者可考虑垂直场景如法律、医疗、销售的记忆产品。隐私保护与本地化存储是可行的差异化卖点。


## 三、创业动态

### [Huawei shelves global AI chip rollout as China's own demand outstrips supply — AMD and Nvidia no longer have to worry.](https://www.reddit.com/r/LocalLLaMA/comments/1wmm89l/huawei_shelves_global_ai_chip_rollout_as_chinas/) ⭐️ 8.0/10 · r/LocalLLaMA

- **概述**：华为原计划向海外市场推广其AI芯片，但由于中国国内对昇腾芯片的需求过于旺盛、产能无法同时满足本土客户，华为决定搁置全球推广计划。这意味着英伟达和AMD短期内不必担心华为在海外市场竞争。
- **分析**：这一决定折射出国产AI算力的真实供需状况：在出口管制背景下，国内大模型公司与云厂商对国产芯片需求井喷，华为产能优先保内需。国产替代已从政策驱动转向市场倒逼，算力自主可控的确定性大幅提升。同时海外暂缺竞争也说明，先进制程产能仍是国产芯片的最大瓶颈。
- **思考**：面向国内市场的AI创业公司应尽早测试和适配昇腾等国产芯片生态，提前锁定算力资源。围绕国产芯片的工具链、迁移服务和推理优化等卖铲子生意，窗口期正在打开。

### [Amazon blocks Meta’s new Muse AI agent from shopping on amazon.com](https://www.forbes.com/sites/jonmarkman/2026/09/21/amazon-blocks-metas-new-muse-ai-agent-from-shopping-on-amazoncom/) ⭐️ 8.0/10 · Hacker News

- **概述**：Meta推出可代用户浏览和下单的Muse AI购物智能体，但亚马逊随即封锁其访问amazon.com，禁止该代理代替用户完成购物。这是大型电商平台首次高调对第三方AI代理关门。
- **分析**：电商平台的商业模式建立在用户直接访问、广告变现和数据掌控之上，AI代理会绕过广告、自动比价，削弱平台对用户关系的控制。亚马逊此举预示代理经济与平台经济的冲突已进入正面交锋阶段，类似当年比价工具被屏蔽的历史重演。谁掌握入口谁就掌握定价权，代理层与平台层的博弈将定义下一代电商格局。
- **思考**：做AI代理类产品的创业者必须预判平台封锁风险，不要把命脉押在无授权的爬取与自动化操作上。更可行的路径是争取官方API合作，或切入平台愿意开放的场景，如企业采购、跨平台聚合等。

### [company raised $416M, sold for $465M, founders got $0](https://www.reddit.com/r/SaaS/comments/1wlzxqi/company_raised_416m_sold_for_465m_founders_got_0/) ⭐️ 7.0/10 · r/SaaS

- **概述**：一家累计融资4.16亿美元的创业公司以4.65亿美元被收购，看似小有回报，但因投资人持有清算优先权等条款，出售款项几乎全部归属投资方，创始人与普通股股东颗粒无收。该案例在海外创投圈引发对融资条款的激烈讨论。
- **分析**：这暴露了风险投资条款残酷的一面：清算优先权尤其是参与优先股，意味着退出价格不够高时普通股可能归零。巨额融资抬高了清算瀑布的门槛，公司必须以远超融资总额的价格退出，创始人才有实际回报。对创始人而言，估值高低不是唯一指标，条款结构往往比估值更致命。
- **思考**：创业者融资时要请专业律师审读清算优先权、参与分配、回购等条款，警惕高估值加重条款的组合。理性控制融资节奏与规模，避免为虚高估值埋下退出即清零的隐患。

### [How can I get my first 1,000 users in the US when I have no network there?](https://www.reddit.com/r/Startup_Ideas/comments/1wm9r91/how_can_i_get_my_first_1000_users_in_the_us_when/) ⭐️ 7.0/10 · r/Startup_Ideas

- **概述**：一位创业者在Reddit发帖求助：产品想进入美国市场，但当地毫无资源和人脉，如何获得前1000个用户。帖子引发关于出海冷启动方法的广泛讨论。
- **分析**：前1000个用户几乎无法靠广告买来，核心是找到高浓度场景：垂直社区如Reddit、Discord、行业论坛，KOC合作，SEO内容和冷邮件外联等。人脉缺失反而逼创业者回归产品与渠道基本功，用内容和口碑替代关系网。冷启动的本质是手动做不可规模化的事，而非寻找捷径。
- **思考**：出海创业者应把目标市场拆解为具体的社区和人群，先服务好一个细分圈层再扩散。与其焦虑人脉，不如系统化投入内容营销和社区运营，用三到六个月建立初始分发能力。

### [Spent 18 months on a parenting app, pivoted halfway when I realised I'd built the wrong thing, and it's now live on Google Play.](https://www.reddit.com/r/SideProject/comments/1wm8m0x/spent_18_months_on_a_parenting_app_pivoted/) ⭐️ 6.0/10 · r/SideProject

- **概述**：一位独立开发者分享：花18个月开发育儿应用，中途意识到做的东西并非用户真正所需，果断调整方向，产品现已登陆Google Play。帖子详细复盘了转型前后的心路历程。
- **分析**：这个案例的稀缺之处在于中途纠错：多数独立开发者因沉没成本太高，明知方向不对仍硬撑到底。18个月才意识到做错，说明前期用户验证严重不足，但及时转型仍好于一条路走到黑。独立开发最大的敌人不是技术，而是闭门造车式的自我感动。
- **思考**：创业者应把验证前置：先找到10到20个真实用户聊透痛点，再做MVP，避免用18个月去验证一个假设。发现方向错误时，转型越早，剩余弹药越多。

### [I accidentally made the #2 post of the year. Here is what +400k views taught me about the SaaS delusion](https://www.reddit.com/r/SaaS/comments/1wm8e0b/i_accidentally_made_the_2_post_of_the_year_here/) ⭐️ 6.0/10 · r/SaaS

- **概述**：一位创业者意外做出年度第二热帖，获得40万以上浏览量。他借此复盘了流行的SaaS幻觉，即以为做出产品就能自动获得订阅收入的迷思，指出大多数SaaS死于无人问津而非产品糟糕。
- **分析**：SaaS被动收入叙事在独立开发圈流行多年，但现实是获客成本、留存和分发才是决定性变量。40万浏览本身也证明了分发能力的价值：好内容带来的注意力远超好产品的自然增长。市场已从产品稀缺进入注意力稀缺时代，会写、会讲、会运营的创始人优势巨大。
- **思考**：创业者应把至少一半精力投入分发：内容、SEO、社区和合作渠道，而非全部押注产品打磨。在动手写代码之前，先验证自己是否具备触达目标用户的渠道。

### [Most startups don't actually need VC](https://www.reddit.com/r/Startup_Ideas/comments/1wm70ev/most_startups_dont_actually_need_vc/) ⭐️ 6.0/10 · r/Startup_Ideas

- **概述**：r/Startup_Ideas上有创业者发帖指出，绝大多数创业公司并不真正需要VC，靠自有资金和早期客户收入同样能跑通业务。帖子引发社区对融资必要性的讨论，不少人分享了不融资也能做大的案例。
- **分析**：这一观点在当前资本环境下尤其值得中国创业者关注。一级市场投资节奏放缓，'先赚钱再扩张'的路径重新流行。VC的钱伴随高增长对赌和股权稀释，只适合少数需要烧钱抢市场的赛道。对多数生意型创业而言，控制成本、快速验证、用客户收入滚动发展反而更稳健。
- **思考**：创业者应先问自己商业模式是否真的需要巨额资本投入，而非默认融资是成功的标志。能自我造血的项目议价能力更强，也更容易在资本寒冬中活下来。

### [Been looking at MVPs backwards](https://www.reddit.com/r/EntrepreneurRideAlong/comments/1wmi7p4/been_looking_at_mvps_backwards/) ⭐️ 6.0/10 · r/EntrepreneurRideAlong

- **概述**：一位创业者在r/EntrepreneurRideAlong发帖称自己一直把MVP（最小可行产品）理解反了。他认为MVP的重点不是做一个功能精简的产品，而是用最低成本验证最关键的商业假设，有时甚至不需要写代码。
- **分析**：这一反思切中许多技术型创始人的通病：花数月打磨产品，却从未验证用户是否愿意付费。MVP的本质是学习工具而非半成品，落地页、人工服务、社群运营都可以是MVP。先验证需求再投入开发，能大幅降低沉没成本。精益创业理念流行多年，实践中仍常被误读为'做个简陋版App'。
- **思考**：创业者在动手开发前，应先明确最想验证的假设是什么，再选择最便宜的验证方式。用'卖得出去'而非'做得出来'来检验需求，往往更接近市场真相。

### [He paid me a MacBook to build this in my spare time. Now it's turning into a real SaaS and he wants in. What do I actually owe him?](https://www.reddit.com/r/EntrepreneurRideAlong/comments/1wmaalj/he_paid_me_a_macbook_to_build_this_in_my_spare/) ⭐️ 6.0/10 · r/EntrepreneurRideAlong

- **概述**：一位开发者受人之托，用业余时间开发了一个工具，对方仅支付一台MacBook作为报酬。如今该项目成长为真正的SaaS产品，原客户希望入股参与，发帖者困惑自己到底欠对方什么。社区普遍认为一次性小额报酬不构成股权依据。
- **分析**：这类纠纷在早期创业中极为常见，根源是合作初期没有书面约定知识产权和收益归属。一台电脑的报酬在法律上更接近外包费用，买断的是当时的工作成果，而非未来收益的分成。但人情与法律是两回事，若对方提供了需求、资源或渠道，适当补偿也有合理性。此帖的核心提醒是：利益分配必须在项目升值之前谈清楚。
- **思考**：创业者在接受或提供任何形式的'帮忙'时，应尽早用书面协议明确权属，哪怕只是一封确认邮件。股权应留给真正的长期贡献者，模糊的好意日后往往演变成纠纷。

### [Payroll took days, now it's one click. What I learned building ops software for a fleet business](https://www.reddit.com/r/EntrepreneurRideAlong/comments/1wmkjgd/payroll_took_days_now_its_one_click_what_i/) ⭐️ 6.0/10 · r/EntrepreneurRideAlong

- **概述**：一位独立开发者在r/EntrepreneurRideAlong分享为车队（fleet）企业构建运营软件的经历，将原本耗时数天的工资核算流程压缩为一键完成。他总结了深入传统行业做效率工具的实战心得。
- **分析**：这是垂直SaaS的典型案例：传统行业的运营痛点往往不被通用软件覆盖，懂业务细节的开发者有机会切入。车队管理涉及薪酬、调度、合规等复杂流程，客户付费意愿强、粘性高。相比竞争激烈的通用工具赛道，'脏活累活'多的细分市场反而壁垒更深。中国创业者可类比物流车队、连锁门店、餐饮后厨等场景。
- **思考**：创业者不妨从自己熟悉或能深入调研的传统行业找痛点，用软件替代重复人工流程。垂直SaaS的关键是先泡在客户现场理解真实流程再动手开发，获客也更容易靠行业口碑裂变。


## 四、大家在靠什么赚钱

### [One short drama made our 5-person team $120k in 30 days](https://www.reddit.com/r/Entrepreneur/comments/1wlzfux/one_short_drama_made_our_5person_team_120k_in_30/) ⭐️ 8.0/10 · r/Entrepreneur

- **概述**：一个5人小团队制作的单部短剧在30天内获得约12万美元收入。帖子在r/Entrepreneur引发关注，再次展示短剧（尤其面向英语市场的出海短剧）的高ROI潜力。
- **分析**：短剧是典型的内容+投流生意：制作成本可控、剧情钩子密集，用户为追更持续付费。海外短剧市场（ReelShort、DramaBox等）已验证付费模型，单剧爆款即可覆盖多部亏损。5人小团队能跑通，说明编剧、拍摄、投流、素材等环节的产业链分工已成熟，可外包拼装。
- **思考**：短剧出海仍有窗口期，但核心能力在投流ROI与选题测试，而非拍摄本身。小团队宜从投流代理、发行分账或本地化改编切入，避免一开始就重资产自制。

  - **客户是谁**：以25-45岁女性为主的海外短剧用户，集中在北美、东南亚、拉美
  - **客户从哪儿来**：TikTok、Instagram、Facebook信息流广告引流至短剧App或小程序
  - **为什么会付钱**：剧情上头带来的即时情绪价值，单集解锁门槛低、追更复购频次高
  - **商业模式**：IAP单集解锁/会员订阅+广告变现（IAA），利润来自投流ROI差价
  - **核心护城河**：工业化内容生产能力、买量投放与素材迭代的数据能力、本地化剧本经验
  - **⚠️ 风险与合规**：内容需符合平台与目标市场审查，擦边、暴力剧情易被下架；投流成本波动大属正常商业风险，无明显违法

### [Made $2,250 last week with my 15-month-old side project, here's what worked (and what didn't)](https://www.reddit.com/r/Startup_Ideas/comments/1wmfei8/made_2250_last_week_with_my_15monthold_side/) ⭐️ 8.0/10 · r/Startup_Ideas

- **概述**：一位独立开发者分享其运营15个月的副业项目上周收入2250美元，并复盘了有效与无效的增长手段。属于典型的微型SaaS/工具类慢增长案例。
- **分析**：15个月才做到周入2250美元（年化约11-12万美元），说明独立产品增长靠长期积累而非爆发。此类复盘的价值在渠道验证：通常SEO内容与社区口碑有效，付费投放和过早扩张产品线无效。对单人团队，慢增长但高利润率是更可持续的路径。
- **思考**：副业创业要按18-24个月增长曲线做预期管理，前期靠主业现金流养产品。别人复盘的'什么没用'往往比'什么有用'更值钱，能少踩坑。

  - **客户是谁**：该项目所属细分领域的职业人群或中小商家，以及关注独立开发的创业者群体
  - **客户从哪儿来**：SEO/博客内容、Reddit与Hacker News等社区、老用户口碑推荐
  - **为什么会付钱**：解决一个具体高频痛点，省时省钱，订阅制决策门槛低
  - **商业模式**：订阅制SaaS或一次性买断工具，边际成本低、利润率高
  - **核心护城河**：细分定位+长期积累的SEO内容与用户反馈迭代，大厂看不上小市场
  - **⚠️ 风险与合规**：常规SaaS合规风险低；需注意此类收入分享存在幸存者偏差，勿直接照搬

### [I collected $150k in one month selling AI services at 19. The real skill wasn’t AI.](https://www.reddit.com/r/EntrepreneurRideAlong/comments/1wltcg2/i_collected_150k_in_one_month_selling_ai_services/) ⭐️ 8.0/10 · r/EntrepreneurRideAlong

- **概述**：一位19岁创业者称通过销售AI服务（大概率为AI自动化代理/Agency模式）单月收款15万美元，并强调真正的关键技能是获客与销售而非AI本身。
- **分析**：这是近年'AI自动化代理'模式的典型样本：用现成工具（n8n、Make、GPT等）为中小企业搭建客服、线索筛选等自动化流程，赚服务费与月度retainer。技术门槛不高，壁垒在冷邮件、LinkedIn获客和成交能力。需注意'收款15万'可能含合同总额而非利润，单人案例有幸存者偏差。
- **思考**：AI服务创业的短板通常不是技术而是信任与获客，先跑通3-5个可复制的交付案例比堆砌技术重要。服务生意成熟后可产品化交付，提升毛利与规模性。

  - **客户是谁**：想用AI但无技术团队的中小企业：本地服务商、电商、律所、诊所、地产中介等
  - **客户从哪儿来**：冷邮件/LinkedIn/社媒私信陌生开发、本地商会人脉、客户转介绍
  - **为什么会付钱**：担心落后于AI浪潮+可量化的人力成本节省（替代客服、行政重复工作）
  - **商业模式**：项目制搭建费+月度维护retainer，或按效果、按坐席收费的服务模式
  - **核心护城河**：销售与成交能力、行业Know-how与交付SOP、可展示的案例背书
  - **⚠️ 风险与合规**：过度承诺AI效果、交付烂尾是主要风险；'收款'口径可能夸大属营销话术，无明显违法但需甄别

### [My micro-SaaS crossed $1,000,000 in volume after 17 days.](https://www.reddit.com/r/micro_saas/comments/1wldeaf/my_microsaas_crossed_1000000_in_volume_after_17/) ⭐️ 7.0/10 · r/SaaS

- **概述**：开发者在r/SaaS称其微型SaaS上线17天累计交易额（volume）突破100万美元。需注意volume通常指经其处理的流水/GMV，而非自身营收。
- **分析**：若volume为流水，产品可能是支付分账、结算或交易撮合类工具，按take rate抽成，实际收入可能仅为流水的小个位数百分比。17天做到百万流水，通常来自既有私域流量、病毒传播或高客单交易场景。此类数据也需警惕刷量或为融资、卖课造势的可能。
- **思考**：看数据先问口径：GMV、收款、MRR、利润是四回事，帖子与媒体常混用。交易类产品早期就要设计风控与合规，流水越大平台责任越大。

  - **客户是谁**：推测为需要收付款、分账、结算的中小卖家或创作者
  - **客户从哪儿来**：开发者社区、Twitter/X、Product Hunt或既有用户群冷启动
  - **为什么会付钱**：解决收款、分账、结算等交易基础设施痛点，按交易抽成定价合理
  - **商业模式**：按交易额抽成（take rate）的平台型模式，收入=流水×费率
  - **核心护城河**：交易网络效应、支付与风控基础设施、上下游集成生态
  - **⚠️ 风险与合规**：涉资金流转需关注KYC/AML、拒付与账户冻结风险；若为他人处理大额流水而合规缺位则灰色程度较高，此处仅报现象不展开

### [Working with my first wigs client for live AI wig try-on with few hairstyles and an original-camera comparison](https://www.reddit.com/r/SideProject/comments/1wm75q1/working_with_my_first_wigs_client_for_live_ai_wig/) ⭐️ 6.0/10 · r/SideProject

- **概述**：一位独立开发者与首个假发行业客户合作，开发实时AI假发试戴功能，支持少量发型样式及与原始摄像头画面的对比展示。属于AI视觉试穿在垂直品类的落地。
- **分析**：假发是跨境电商高毛利品类（以美国非裔消费者市场为主），客单高、退货率高、购买决策极依赖效果展示，试戴功能能直接提升转化、降低退货，卖家付费意愿明确。技术上可基于现成人脸关键点与发丝分割实现，单人即可交付MVP。该案例展示了'老品类+AI体验升级'的服务切入路径。
- **思考**：垂直行业AI试穿/试戴适合走'首个标杆客户→行业模板化复制'路径，先深耕一个品类做透再横向扩展。人脸数据属生物识别信息，合规成本要提前计入报价。

  - **客户是谁**：假发品牌与卖家（独立站、Amazon、AliExpress商家），尤其面向欧美非裔消费者的店铺
  - **客户从哪儿来**：跨境电商卖家社群、Shopify服务商生态、主动陌拜与行业展会
  - **为什么会付钱**：提升转化率、降低退货率，试戴体验成为店铺差异化卖点
  - **商业模式**：按项目定制开发费，或SaaS插件按月订阅/按SKU数量计费
  - **核心护城河**：垂直品类试戴效果的调优经验、与头部卖家深度绑定的标杆案例
  - **⚠️ 风险与合规**：人脸属生物识别敏感数据，需注意采集授权与各地隐私法（如美国伊利诺伊州BIPA）；整体合规风险中等偏低

### [Using Polar.sh as Merchant of Record from outside the US/EU: how are reviews and payouts going? (I will not promote)](https://www.reddit.com/r/startups/comments/1wmc5bg/using_polarsh_as_merchant_of_record_from_outside/) ⭐️ 6.0/10 · r/startups

- **概述**：有创业者发帖询问在美国/欧盟之外使用Polar.sh作为Merchant of Record（记录商户）的真实评价与打款情况。Polar是面向独立开发者的开源变现平台，代收款项并处理全球税务合规。
- **分析**：非美欧独立开发者长期面临收款难题：Stripe覆盖有限，Paddle、Lemon Squeezy审核趋严。MoR模式下平台作为商户主体代收款项、代缴VAT/销售税，开发者无需注册海外公司，这对中国等地区开发者价值极大。帖子同时反映社区对新兴MoR的打款稳定性与封号风险仍有疑虑。
- **思考**：出海收款基础设施是独立开发的隐形瓶颈，选MoR要看打款记录、费率与封号申诉机制，最好多平台备份。中国团队也可评估香港主体+正规通道等组合方案。

  - **客户是谁**：美国/欧盟之外的独立开发者、微型SaaS与数字产品卖家，含中国出海个人开发者
  - **客户从哪儿来**：GitHub开源社区、开发者Twitter/X、独立开发社区口碑传播
  - **为什么会付钱**：一站式解决全球收款、税务合规与发票开具，免去注册维护海外公司的高成本
  - **商业模式**：MoR交易抽成模式（约4%+固定费），平台承担税务合规主体责任
  - **核心护城河**：开源带来的开发者信任、MoR税务合规牌照与基础设施、开发者体验
  - **⚠️ 风险与合规**：依赖单一MoR存在账户冻结、打款延迟与政策变动风险；个人借MoR规避税务申报属灰色地带，应依法合规申报，此处仅报现象


## 五、AI工作流、方法、效率

### [Python Workers are now generally available](https://blog.cloudflare.com/python-workers-ga/) ⭐️ 6.0/10 · Hacker News

- **概述**：Cloudflare宣布Python Workers正式商用（GA），结束长期Beta阶段。开发者可用Python编写边缘函数并部署到其全球网络，底层基于Pyodide（WebAssembly版CPython），支持FastAPI等主流生态。这意味着Python开发者无需切换技术栈也能享受Serverless边缘计算。
- **分析**：Python是AI与数据领域的主导语言，此前边缘计算几乎被JS/TS垄断，此举打通了从AI模型到边缘部署的完整链路。对创业者而言，部署成本与运维复杂度进一步降低，个人开发者也能以极低费用获得全球分布式能力。这也是Cloudflare与AWS Lambda、Vercel争夺开发者生态的关键落子。Python生态在Workers中的兼容深度，将决定其真实生产力上限。
- **思考**：对创业者来说，AI应用加边缘Python是低成本验证MVP的新路径，尤其适合AI Agent的API网关与数据处理中间层。以Python为主栈的团队可省去学习TS的成本，小团队也能拥有大厂级的全球分发能力。

  - **核心流程**：① 用Python编写Worker（可复用FastAPI等框架）→ ② Wrangler CLI本地调试 → ③ 一条命令部署至全球边缘节点 → ④ 绑定KV/R2/D1存储与Workers AI能力 → ⑤ 按请求计费、自动弹性扩缩容
  - **关键点**：最值得抄的是零服务器全球部署：用Python写一个API，几分钟获得全球低延迟分发，月成本近乎为零，非常适合作为AI产品的MVP底座。

### [M5 Ultra Mac Studio Review: The Dream Mac for Local AI Agents](https://www.reddit.com/r/LocalLLaMA/comments/1wmg1zj/m5_ultra_mac_studio_review_the_dream_mac_for/) ⭐️ 6.0/10 · r/LocalLLaMA

- **概述**：海外社区评测认为，搭载M5 Ultra芯片的新款Mac Studio是运行本地AI Agent的梦想之机。其超大统一内存可在本地流畅运行DeepSeek、Llama等大参数开源模型，功耗与噪音远低于多卡GPU方案。评测特别强调其在多Agent并发与长上下文场景下的稳定性。
- **分析**：Apple Silicon的统一内存架构让单机跑大模型成为可能，相比租用H100集群，一次性投入后无按token计费，长期成本优势明显。本地化部署意味着数据不出内网，对金融、医疗、法律等隐私敏感行业是刚需卖点。开源模型能力持续逼近闭源，让本地硬件的投资回报率不断上升。混合架构（本地推理为主、云端兜底）正在成为创业公司的主流选择。
- **思考**：创业者可考虑用买断制本地算力替代云API：若产品日均调用量大，一台Mac Studio一两年即可回本，数据合规还能成为To B差异化卖点。轻量团队可先从Mac mini起步验证工作流，再决定是否加码高端机型。

  - **核心流程**：① 购置M5 Ultra Mac Studio并按内存档位选配 → ② 部署Ollama/MLX/LM Studio等推理框架 → ③ 加载DeepSeek、Qwen、Llama等开源模型 → ④ 通过本地API接入LangChain等Agent框架 → ⑤ 敏感数据全程不出内网，云端仅作溢出兜底
  - **关键点**：最值得抄的是统一内存即显存的思路：用一台Mac Studio替代GPU服务器跑开源模型，把AI推理成本从按token计费变成一次性固定资产。

### [Vibe Coding Report - 2026: start your dream business today](https://www.reddit.com/r/Startup_Ideas/comments/1wmfkgw/vibe_coding_report_2026_start_your_dream_business/) ⭐️ 6.0/10 · r/Startup_Ideas

- **概述**：一份2026年Vibe Coding趋势报告指出，借助Cursor、Claude Code、v0等AI编程工具，非技术背景者用自然语言描述需求即可构建产品，今天就开始梦想生意正在成为现实。报告预计覆盖工具链选型、独立开发者案例与收入数据。
- **分析**：Vibe Coding自2025年被Karpathy提出后从梗演变为方法论，2026年报告的出现标志着它已进入主流创业流程。开发门槛坍塌意味着技术壁垒不再是护城河，分发能力、审美与需求洞察成为新的竞争维度。验证一个想法的成本从数月数万美元压缩到数天数百美元，试错次数成为新优势。但AI生成代码的安全隐患与维护债务，也会让快变成双刃剑。
- **思考**：创业者应把问题从会不会写代码换成会不会定义问题：用Vibe Coding快速做十个MVP，用数据筛出一个值得深耕的方向。但核心业务逻辑与用户资产必须自己掌控，避免被单一AI工具链锁死。

  - **核心流程**：① 用AI对话梳理需求并生成PRD → ② 用Cursor/Claude Code/v0生成前后端代码 → ③ 接入现成的支付、登录、数据库服务 → ④ 尽快上线投放，收集真实用户反馈 → ⑤ 数据验证通过后再投入工程资源正式重构
  - **关键点**：最值得抄的是先卖再做：用Vibe Coding几天做出可收费的MVP，用真实付费验证需求，而不是花半年打磨一个没人要的完美产品。
