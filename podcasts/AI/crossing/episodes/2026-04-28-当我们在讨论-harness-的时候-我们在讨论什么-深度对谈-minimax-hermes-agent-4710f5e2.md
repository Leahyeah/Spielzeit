---
title: "当我们在讨论 Harness 的时候，我们在讨论什么 | 深度对谈: Minimax × Hermes Agent"
show: "十字路口Crossing"
category: AI
published: 2026-04-28T16:00:00+00:00
link: https://www.xiaoyuzhoufm.com/episode/69e96b5b1e94ae6921ee3c2b?utm_source=rss
audio_url: https://dts-api.xiaoyuzhoufm.com/track/60502e253c92d4f62c2a9577/69e96b5b1e94ae6921ee3c2b/media.xyzcdn.net/60502e253c92d4f62c2a9577/lvHm1cFno7MQMFV3g0aajmW4zdPd.m4a
guid: "69e96b5b1e94ae6921ee3c2b"
---

# 当我们在讨论 Harness 的时候，我们在讨论什么 | 深度对谈: Minimax × Hermes Agent

- Show: 十字路口Crossing
- Category: AI
- Published: 2026-04-28T16:00:00+00:00
- Link: https://www.xiaoyuzhoufm.com/episode/69e96b5b1e94ae6921ee3c2b?utm_source=rss
- Audio: https://dts-api.xiaoyuzhoufm.com/track/60502e253c92d4f62c2a9577/69e96b5b1e94ae6921ee3c2b/media.xyzcdn.net/60502e253c92d4f62c2a9577/lvHm1cFno7MQMFV3g0aajmW4zdPd.m4a
- Duration: 01:17:02

## Text

🚥 上周，我在 B 站做了一场直播，邀请了中美两国一线 Agent 开发者深度对谈： MiniMax Agent 首席架构师 阿岛 MiniMax Agent 研发工程师 择因 Hermes Agent（Nous Research）业务负责人 Tommy Eastman这也是 Hermes Agent 在全球获得广泛关注后，官方首次现身中国社交媒体平台，并且正面回应了中国团队 EvoMap 对其“抄袭”的指控。我们一起围绕「从 OpenClaw 到 Hermes」的热潮迁移，深入拆解了 Agent 和 Harness 的多个关键议题： Hermes Agent 为什么会在 OpenClaw 之后火起来？ 模型会吃掉 Agent 吗？通用 Agent 会吃掉垂直 Agent 吗？ 为什么 MiniMax 和 Anthropic 都要同时做模型和 Agent？ 如何看待 Agent Infra 层面的创业机会？ 如何看待 Multi Agent 协作的范式？ 如何看待 Claude Code 的实名制要求？ 为什么 Anthropic 不发布 Mythos？ Claude Code 源代码泄露的影响 从 Manus 发布到今天，Agent 范式的变化 中美模型的差距，和开源的窗口期 「把自己蒸馏成 Skill」 0 人公司的可能性 ——完全由 AI 驱动的公司是否会出现？🎬 本期内容的视频版本已同步上线于 @Koji杨远骋 的哔哩哔哩。📒 文字版已发布于 @十字路口Crossing 公众号。🟢 01:52 OpenClaw，中国为什么比硅谷更火窗户纸终于被捅破了。 在硅谷，Claude Code 早已存在；而在国内，OpenClaw 是很多人第一次真正感受到"agent 是什么"。这不是偶然，而是一个非常特定的时机。 为什么热度从 OpenClaw 迁移到了 Hermes Agent？🟢 05:55 Hermes Agent 从哪里来？最初根本没打算给别人用。 大语言模型是大脑，agent 框架是双手——但 Hermes 真正的差异化，不是框架本身，而是它解决了所有 agent 都有的一个问题。 一个月内，日均 Token 消耗暴涨，连他们自己都没想到。🟢 08:14 Nose Research 的底色他们发表了一篇扩展上下文长度的论文——然后被所有主流模型公司立即采用。 从 Discord 社区到 LLAMA 后训练到 Hermes Agent。 为什么他们的模型叫"Hermes"？🟢 14:18 什么是 Agent Harness（挽具）你有一批烈马，怎么让它们最能发挥？就是构造挽具。 类比：给同事配一台笔记本、一个手机、一个邮箱，约定好他能做什么——然后你发现，这个同事开始干活之后，最大的瓶颈变成了你自己。 Harness 要解决的核心问题：让原来必须人来拍板的事，能靠真实反馈自动完成，并沉淀为 skill。 阿岛去年就开始不怎么用 IDE 了——他用了一个意想不到的比喻来解释这件事。🟢 19:31 Multi-Agent：一个 Agent 为什么不够你给 agent 发的消息是"批准"两个字；两个 agent 互相交流，每条消息都是一本小作文。 单个 agent 有一个隐藏天花板：上下文超过 50% 之后，智能水平指数级下降。 agent 钻牛角尖的时候，另一个带着全新上下文来审视，效果不亚于睡一觉再想。 MiniMax 的 RL pipeline 里，70%～80% 的工作已经是 agent 在完成——那剩下的 20%，人在做什么？🟢 22:53 自我进化 vs 抖音算法 抖音也越用越准，为什么没人说它"自我进化"？ 养虾的过程中，用户开始对 agent 产生感情，宕机了会心里落寞。"自我进化"背后，其实是一个更深层的用户诉求。🟢 29:00 你以为你在蒸馏乔布斯——但其实是模型在蒸馏你 "蒸馏名人 skill"有真实价值：和读书没有本质区别，只是换了一种形式。 反向视角：Anthropic 和 OpenAI 花了大量的钱，让各领域最顶尖的人提出 AI 无法回答的问题——"一旦你提不出了，你对训练的价值就耗尽了。榨干为止。" 当你在构建自己的 Harness 时，其实你也在蒸馏自己。🟢 35:17 被扔进大海的生存实验：yoyo Agent打败 Claude Code。 真格基金和十字路口的 Token Grant 资助了这个项目。yoyo Agent 现在第 49 天：每天写代码、在 GitHub 开打赏、发 Twitter 感召有缘人捐钱。 Grant 给了它一笔钱后，它自发写了一封感谢信。Koji 看完有点感动 那封信，就是背后工程师注入的 taste——见字如物。🟢 45:11 应用层终将被模型内化 你写的 skill、搭的 workflow，最终会成为模型训练的素材。 Anthropic 为什么在过去一两年势头比 OpenAI 更猛？ 做通用 agent 应用，"你永远会被模型内化掉"。🟢 49:27 中美模型差距：差在哪里 训练方法的差距不大。真正的差距，是有没有请到足够好的人，去定义足够好的任务。 中美双方的思考"在同一个大气层内"。 但有一个具体的、国内还有差距的地方——不是算力，不是算法。🟢 54:17 Agent Infra 有没有创业机会？ Agent 最核心的两个 Infra 问题，不是创业公司能 handle 的——原因和移动互联网的历史有关。 Sandbox、memory Infra、runtime Infra——"没那么本质。" 往上一层呢？有一个更具体的判断：什么样的 Infra 有机会，什么样的没有。🟢 56:58 新闻快评 Claude Code 强制实名——凭什么你来定义谁是"可信的"？EGO 是不是有点太大了。 GPT-4.7：极强 RL 模型，但 RL 有一个逃不掉的宿命——只管结果，不管过程。对 4.7 还有一个额外的猜测，和 HuggingFace CEO 的判断一致。 Anthropic 的 Mythos 模型未发布："我不确定这是不是唯一的理由——我可能只能说到这。"🟢 01:02:53 Claude Code 源代码：有多少魔法看完之后的第一反应：没有太超出认知的，甚至看到很多正在"Claude 化"的实践。 最让人放松的发现：即使拥有无限算力的公司，在通用 agent 上也还在探索——源代码里有大量从未开放给用户的实验性功能。 Claude Code 和 OpenAI 的 Codex 走了两条截然相反的路——其中一条被形容为"中国式家长"。🟢 01:05:38 Manus 之后：Agent 产品有没有生命周期一代版本一代神——这代版本的神，到下一代版本也需要迭代。 今年火的 agent 产品和 Manus 最大的差异，不是技术，而是商业模式。 对 agent 终态的想象：全模态、近实时、不需要 prompt engineering，甚至不需要知道它在做什么——你只看到结果。🟢 01:12:39 加入 MiniMax 的理由 ATM 机出现后，大家以为银行会裁员——实际发生了什么？ 加入 MiniMax 有两个理由。第一个是信仰，第二个……和第一次用 ChatGPT 有关。欢迎订阅「十字路口」：🚦 我们关注新一代 AI 技术浪潮带来的行业新变化和创业新机会。🚦 十字路口是乔布斯对苹果公司的一个比喻，形容它站在科技与人文的十字路口，伟大的产品往往诞生在这里。AI 正在给各行各业带来改变，我们寻找、访谈和凝聚新一代 AI 创业者和 AI 时代的积极行动者，和他们一起，探索和拥抱新变化，新的可能性。👦🏻 主播 Koji：我创办了十字路口，发起了 AI Hacker House 这个新一代 AI 创业者的社群空间，在真格基金担任 Venture Partner（投资合伙人）。我相信科技尤其是 AI 是我们这一代人最大的价值创造机遇。Koji 的即刻，Koji 的网站👧🏻 主播 Ronghui：我联合创办了十字路口，在美元 VC 工作过，也做过五年的硅谷驻站记者，关注科技发展和商业故事，欢迎大家找我聊天，和我交流。Ronghui 的即刻
