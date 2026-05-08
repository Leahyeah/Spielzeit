---
title: "E13 和 Macaron 创始人陈锴杰聊：RL + Memory 让 Agent 成为用户专属的“哆啦 A 梦”"
show: "海外独角兽"
category: AI
published: 2025-09-11T10:52:13+00:00
link: https://www.xiaoyuzhoufm.com/episode/68c2a8f52c82c9dccadd7771?utm_source=rss
audio_url: https://dts-api.xiaoyuzhoufm.com/track/6410266f5384961ba7e08c7d/68c2a8f52c82c9dccadd7771/media.xyzcdn.net/6410266f5384961ba7e08c7d/lvisIylsO59CpbQwX0y36GWZyHTy.m4a
guid: "68c2a8f52c82c9dccadd7771"
---

# E13 和 Macaron 创始人陈锴杰聊：RL + Memory 让 Agent 成为用户专属的“哆啦 A 梦”

- Show: 海外独角兽
- Category: AI
- Published: 2025-09-11T10:52:13+00:00
- Link: https://www.xiaoyuzhoufm.com/episode/68c2a8f52c82c9dccadd7771?utm_source=rss
- Audio: https://dts-api.xiaoyuzhoufm.com/track/6410266f5384961ba7e08c7d/68c2a8f52c82c9dccadd7771/media.xyzcdn.net/6410266f5384961ba7e08c7d/lvisIylsO59CpbQwX0y36GWZyHTy.m4a
- Duration: 01:10:42

## Text

最近，我们观察到 AI 市场开始出现了一些新变化：随着 ChatGPT 加入记忆功能，AI 的角色正发生有趣的转变——它不仅是帮你写代码、做 PPT 的小工具，还有潜力成为一个真正懂你的生活伙伴。同时，Agent 开发进入了更成熟的阶段。过去大家主要依赖 prompt 技巧，如今通过强化学习和记忆系统，开发者可以训练出既有情商、又能生成小工具的智能体。这两个趋势的叠加，推动 AI Agent 可以更加个性化、专业化地完成用户任务。本期节目，我们邀请了 Macaron 创始人陈锴杰。他是 95 后连续创业者，曾打造 300 万用户的互动故事平台 MidReal。他将和我们聊聊如何把 Memory 当作一种智能能力进行训练，并分享强化学习在 Agent 开发中的重要性。锴杰坦言，Macaron 还有巨大的优化空间，100 分里只会给 7-8 分。但他相信，Personal Agent 将成为像社交软件一样的超级赛道。如果你对 AI Agent 如何与我们的生活交互感兴趣，请千万不要错过这期内容！00:05:24 把 Memory 当成智能能力训练：Memory 不是目的，而是方法00:11:01 如何进行冷启动——让用户第一天就感到“被理解”？00:15:51 如何用 Multi-Agent 技术平衡“高情商的朋友”和“高智商的助理”00:18:59 Macaron 的愿景是做一个生活方式的分享平台00:22:36 AI Sub Agent 的“进化论”和记忆传递方式00:35:55 为什么强化学习（RL）是 Agent 智能提升下半场的核心？00:39:42 All-sync RL 技术：把 RL 训练速度从周压缩到天，实现产品快速迭代00:43:15 RL infra 很难像云服务一样标准化00:55:03 三个真实用例带来的 Aha Moments00:58:36 社交软件领域给 AI Agent 开发带来的思考01:06:21 如何思考 OpenAI 等巨头在个人 Agent 领域带来的竞争？Character.AI：个性化的 ChatGPT，AI 大模型时代的 UGC 平台Agent 最全 Playbook：场景、记忆和交互创新RL 是 LLM 的新范式对 DeepSeek 和智能下半场的几条判断Claude 4 核心成员：Agent RL，RLVR 新范式，Inference 算力瓶颈CoT（Chain-of-Thought，思维链）：指在训练大模型时，把推理过程逐步写出来，而不是只给最终答案。RAG（Retrieval-Augmented Generation，检索增强生成）：模型生成答案时，先从知识库/外部文档里检索相关内容，再用检索结果辅助生成。Context Engineering（上下文工程/上下文设计）：一种更系统的 prompt 设计方法，把相关的背景信息、任务指令、示例等整合到输入里。Multi-Agent 架构（多智能体架构）：指将不同功能的模型拆分为多个 Agent，每个 Agent 专注于某一类任务（如对话、代码生成），通过协作与协议完成整体目标。Sub Agent（子代理 / 小工具）：在 Personal Agent 中生成的专属小程序，用于解决具体生活或工作任务（如饮食规划、健身记录、日记管理）。它们由主 Agent 调用或生成。Router（任务路由）：在 Multi-Agent 系统中，负责把用户请求或上下文信息合理分配给不同的 Agent（如聊天 Agent、Coding Agent），确保任务由最合适的模块完成。on-policy（同策略训练）：强化学习中的一种训练方式，模型完全基于自己生成的数据来更新参数，而不是依赖外部静态数据集，能让训练目标更直接对齐实际环境。online training（在线训练）：指模型在上线运行过程中，根据用户实时反馈或交互数据不断更新和优化，相比批量离线训练更能快速适应用户需求。all-think RL / all-sync RL（全同步强化学习）：一种优化强化学习训练效率的方法。通过同时调度训练（trainer）和推理（inference），减少 GPU 资源空转，把训练时间从“按周”压缩到“按天”。GPU bubble（GPU 气泡）：在训练大模型时，由于训练和推理交替不均衡，导致 GPU 算力出现空闲、被浪费的现象。优化方法目标就是尽量“挤掉泡泡”。expert parallelism（专家并行）：大模型训练中的并行方式，把模型拆分为多个“专家模块”（Experts），不同 GPU 分别负责部分专家，提升效率。常见于 Mixture-of-Experts （MoE） 模型。pipeline parallelism（管线并行）：大模型训练中的并行方式，把神经网络的不同层分配到不同 GPU 上，像流水线一样依次传递数据，解决模型过大无法放入单卡的问题。
