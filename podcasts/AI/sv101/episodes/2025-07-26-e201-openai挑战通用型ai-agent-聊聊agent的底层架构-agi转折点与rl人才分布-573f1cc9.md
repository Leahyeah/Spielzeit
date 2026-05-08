---
title: "E201｜OpenAI挑战通用型AI Agent，聊聊Agent的底层架构、AGI转折点与RL人才分布"
show: "硅谷101"
category: AI
published: 2025-07-26T00:00:00+00:00
link: https://sv101.fireside.fm/211
audio_url: https://aphid.fireside.fm/d/1437767933/f0f20376-8faf-4940-b920-84af6c734e2d/aa07ca42-2e0c-4009-8e2f-9fca346bfaad.mp3
guid: "aa07ca42-2e0c-4009-8e2f-9fca346bfaad"
---

# E201｜OpenAI挑战通用型AI Agent，聊聊Agent的底层架构、AGI转折点与RL人才分布

- Show: 硅谷101
- Category: AI
- Published: 2025-07-26T00:00:00+00:00
- Link: https://sv101.fireside.fm/211
- Audio: https://aphid.fireside.fm/d/1437767933/f0f20376-8faf-4940-b920-84af6c734e2d/aa07ca42-2e0c-4009-8e2f-9fca346bfaad.mp3
- Duration: 1:19:34

## Text

美国时间7月17日，OpenAI终于迎来了它的“Agent时刻”——通用型ChatGPT Agent正式发布。它整合了深度研究工具Deep Research与执行工具Operator，可一站式完成复杂任务，但仍存在速度慢、个性化不足等短板。 ChatGPT Agent的技术本质是“浏览器+沙盒”的混合架构，与Manus、Genspark形成技术路线差异。在底层架构层面，浏览器（Browser-based）代理虽堪称“万能”，但运行速度较慢；沙盒（Sandbox）代理高效，但无法联网操作、工具库受限；而工作流集成（Workflow API）速度快、结果精准。在训练方法层面，强化学习（RL）被视为AGI从“执行者”向“创新者”跨越的重要路径，但当前面临的验证泛化与训练不稳定难题，如同两道枷锁锁住了这扇进阶之门。 强化学习能否成为通用AI爆发的关键引擎？AGI实现技术跃迁的分水岭究竟在哪？在把Agent产品化和商业化的道路上，又如何平衡模型能力与用户体验？本期《硅谷101》，主播泓君对话Pokee.ai创始人朱哲清，多维度测评ChatGPT Agent使用体验，并深入拆解Agent的四大底层设计逻辑、探讨强化学习的训练路径，以及我们迎接“超级智能时刻”所面临的技术挑战。 【主播】 泓君Jane，硅谷101创始人，播客主理人 【嘉宾】 朱哲清，Pokee.ai创始人，前MetaAI应用强化学习团队负责人，斯坦福强化学习博士（X：@ZheqingZhu） 【101 Weekly新节目预告】 硅谷101上线了一版更加轻量级的音视频节目「101Weekly」，每周由我们的三位主播复盘三个商业热点事件，每期10分钟左右，并请来行业专家来一手分析解读，希望这每周的30分钟，帮助大家轻松了解一周新闻大事件，点击收听。 音频版：Fireside｜小宇宙｜苹果播客｜Spotify 视频版：BiliBIli｜Youtube｜视频号｜抖音 【你将听到】 ChatGPT Agent首发体验与技术拆解 00:21 拆解AI Agent技术路径：什么是“聪明机器的大脑”？ 02:12 ChatGPT Agent一手实测：浏览器操作如超人 VS 速度慢如蜗牛 04:26 视觉能力加持：Action体验有提升，但仍需等待 05:45 旅行规划场景：支付环节仍需人类介入，信任门槛尚未跨越 08:11 “全部推翻重来”：缺乏个性化机制、记不住反馈细节 10:07 ChatGPT Agent“打通搜索与执行”的本质：Deep Research + Operator的“拼贴工程” 通用型Agent技术路径对比 12:31 通用Agent技术类比：Operator最早专注Browser操作，如今叠加Sandbox后，在通用Agent里表现最强 14:52 四大技术方向优劣势对比： 15:40 浏览器为主：通用性强，但速度慢、体验差、成本高 17:21 开放虚拟机：本地运行快，但访问互联网等外部服务不易 17:37 大模型+虚拟机：GensPark模式，相对环节更封闭 18:46 Workflow+工具集成：Pokee模式，交付好但不是所有任务都能做 20:23 Manus模式：Browser-based，Sandbox强，全能但慢 22:28 Genspark模式：标化工作流，牺牲通用性换取速度与稳定性 23:41 Pokee模式：速度快成本低，但范围受限 26:52 B端客户还是C端客户，适用场景与底层技术逻辑完全不同 29:36 Agent将重塑互联网入口，传统门户流量将大幅下滑 32:03 MCP无人维护：2万个协议中，真正可用的不到200个 33:47 Agent时代的广告逻辑大变：反而更有利于创作者？ 强化学习与AGI的五个层次 38:52 强化学习适用场景：目标明确、机制清晰但数据稀缺 41:50 新兴路径：强化学习预训练（RL Pretraining） 44:40 一个非共识：验证（Verification）方向的泛化性，可能产出人类所不拥有的知识 46:51 AGI五级路径中，“执行者”(L3) 与“创新者”(L4) 间存在巨大技术鸿沟，核心在于验证能力 50:37 强化学习预训练的致命弱点：给出的解决方案可能“人类都看不懂” 52:43 强化学习（RLHF） Vs 监督学习微调（SFT）：效果×2，但成本×10 Meta收购ScaleAI背后的逻辑 54:08 Meta收购Scale：多模态数据仍然是瓶颈 56:46 多模态数据的最大挑战：数据复杂 + 维度多 → 主观标准难统一 57:59 AI的核心问题：短期算力，中期数据，长期人才 59:10 如何让Agent调用更好用？自研模型 01:03:33 平衡模型能力与用户体验：模型能力决定下限，产品细节决定上限 强化学习的人才大本营 01:05:42 RL奠基人、2024年图灵奖得主Richard Sutton：想法极具前瞻性，且坚持原则 01:07:47 模型可塑性挑战：AI的“灾难性遗忘”亟待解决 01:09:56 奖励函数设计难：强化学习中如何设定“道德且有效”的多目标激励 01:11:47 RL核心研究圈：学术界与业界均高度集中 学术界：OpenAI早期团队，Peter Abbeel, Sergey Levine , Richard Sutton 业界：以David Silver为代表的DeepMind员工、以John Langford为代表的微软员工等 01:12:50 从AlphaGo开始，伦敦成为强化学习研究的重要中心 01:15:28 如何像投资人销售过于超前的想法：只说一个非共识 01:16:58 市场正在分化，技术路径选择是创业公司活下来的核心 【节目中提到的AI Agent】 OpenAI相关： ChatGPT Agent｜Operator｜Deep Research 其他： Manus｜Genspark｜Perplexity｜Claude Agent｜Fellou｜Flowise｜Zapier｜UIPath｜Replicate 【节目提到的相关术语】 MCP / Model Context Protocol（模型上下文协议） A2A（Agent-to-Agent Protocol） SDK（软件开发工具包） API（应用程序接口） Vision Model Browser-based Agent Sandbox（沙盒环境） Virtual Machine (VM) Token Consumption（Token消耗） Tool Calling：调用第三方工具或API完成任务 Workflow-based Agent Reinforcement Learning / RL（强化学习） RL Fine-tuning / RLFT（强化学习微调） RL Pre-training（强化学习预训练） Verification（验证机制） Ground Truth（基准真值） Hallucination（幻觉） Human Feedback（人类反馈） Supervised Fine-tuning / SFT (监督式微调) Human Readability（可读性） Catastrophic Forgetting（灾难性遗忘） Benchmark Score（基准分数） ICML（International Conference on Machine Learning）：机器学习顶级学术会议 【相关节目】 E200｜投资人视角深聊：AI Agent的核心壁垒与投资逻辑 E195｜从工具到伙伴：七位AI Agent深度使用者的思考 E191｜小而美的机会来了，聊聊这轮AI Agent进化新范式 【监制】 泓君 【后期】 AMEI 【Shownotes】 陈思扬 【运营】 王梓沁 【BGM】 Simple Pleasantries - Arthur Benson Anticipating a New Day - Stationary Sign 【在这里找到我们】 公众号：硅谷101 收听渠道：Apple Podcast｜Spotify｜小宇宙｜喜马拉雅｜蜻蜓FM｜荔枝FM｜网易云音乐｜QQ音乐 其他平台：YouTube｜Bilibili 搜索「硅谷101播客」 联系我们：podcast@sv101.netSpecial Guest: 朱哲清.
