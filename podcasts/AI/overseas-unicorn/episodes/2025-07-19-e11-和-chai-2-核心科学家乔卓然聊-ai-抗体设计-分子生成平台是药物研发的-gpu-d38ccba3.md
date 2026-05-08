---
title: "E11 和 Chai-2 核心科学家乔卓然聊「AI 抗体设计」：分子生成平台是药物研发的 GPU"
show: "海外独角兽"
category: AI
published: 2025-07-19T03:51:36+00:00
link: https://www.xiaoyuzhoufm.com/episode/687b15cba9dec925000a83fe?utm_source=rss
audio_url: https://dts-api.xiaoyuzhoufm.com/track/6410266f5384961ba7e08c7d/687b15cba9dec925000a83fe/media.xyzcdn.net/6410266f5384961ba7e08c7d/lgRlKGY1JVztVZ0mooNrhVmRdFAM.m4a
guid: "687b15cba9dec925000a83fe"
---

# E11 和 Chai-2 核心科学家乔卓然聊「AI 抗体设计」：分子生成平台是药物研发的 GPU

- Show: 海外独角兽
- Category: AI
- Published: 2025-07-19T03:51:36+00:00
- Link: https://www.xiaoyuzhoufm.com/episode/687b15cba9dec925000a83fe?utm_source=rss
- Audio: https://dts-api.xiaoyuzhoufm.com/track/6410266f5384961ba7e08c7d/687b15cba9dec925000a83fe/media.xyzcdn.net/6410266f5384961ba7e08c7d/lgRlKGY1JVztVZ0mooNrhVmRdFAM.m4a
- Duration: 01:20:15

## Text

AlphaFold 3 获得诺贝尔奖是 AI 在生物领域的重要里程碑，是生命科学领域中“foundation model 时刻”的典型代表，但蛋白质结构预测只是科研闭环的起点，只有当模型的能力从“预测结构”迈向“直接生成分子”，新药开发效率才能实现真正的指数级提升。Chai Discovery 这家公司正是在 AlphaFold 方向上复现开源最快的公司。去年 9 月获得了 Thrive 和 OpenAI 3000 万美金的种子轮投资，估值达到 1.5 亿美金。他们的模型 Chai-1 选择的技术路线是用 Diffusion 模型做结构预测，和 AlphaFold 路线接近。今年 6 月 30 日，他们又发布了新模型 Chai-2，它在零样本的前提下能自动生成有效的抗体结构，命中率高达 16%，是传统噬菌体筛选技术命中率的百倍，还具备极强的可扩展性，也就说，可以在几个小时内，为任何一个靶点设计出可实验验证的候选分子。可见 Chai 的目标并不是 AI 辅助制药，而是构建“AI-native 制药”平台，把科学问题转化成工程问题。本期内容我们邀请到了 Chai Discovery 的创始科学家乔卓然，卓然曾在 Iambic Therapeutics 担任 Senior Research Scientist，2025 年起，他作为创始团队成员和 AI 科学家加入了 Chai Discovery，是 Chai-2 模型的核心贡献者。他将结合自己科研经历，和我们分享了 Chai-2 的模型架构、实验成果，以及 AI 在药物发现领域真正的突破口。One More Thing：本期文字稿可见 👉 对谈 Chai-2 核心科学家乔卓然：抗体生成成功率提升百倍，分子生成平台是药物研发的 GPU｜Best Minds00:06:00 Diffusion Model 带来了建模范式的根本改变00:08:10 AlphaFold 2 给模型的架构扫平了很多障碍00:16:28 Chai 团队的最大特点是具备第一性原理00:18:00 Chai-2 和 AlphaFold 有什么不同？00:21:42 蛋白质结构设计是结构预测的逆问题00:29:56 Chai-2 相较于 Chai-1 最大的进步是从预测过渡到了生成00:34:21 Chai-2 将药物开发周期从数月缩短到两周00:37:56 在零样本前提下，Chai-2 能设计出具备 binding 活性的抗体，成功率高达 16%00:45:37 模型的结构预测能力决定了模型上限00:51:59 在所有 de novo 抗体设计或 binder 设计中，模型早已超越了人类的能力01:00:04 分子生成平台对药物研发的作用将像 GPU 对 AI 的作用一样01:04:15 Zero-shot 更接近药物设计的本质01:05:14 合成数据是连接实验数据和生物学理论的“第三模态”01:12:43 未来 AI for Science 公司的商业模式是“平台即 IP”>> 对谈 Chai-2 核心科学家乔卓然：抗体生成成功率提升百倍，分子生成平台是药物研发的 GPU｜Best Minds>> 对谈斯坦福 Biomni 作者黄柯鑫：AI Scientist 领域将出现 Cursor 级别的机会｜Best Minds>> Chai Discovery：OpenAI 投资的 AI4Sci 公司，AlphaFold 最快追赶者>> Isomorphic Labs：DeepMind 创始人再创业，打造制药界的 TSMC>> FutureHouse 联合创始人：AI Scientist 不是“全自动化科研”>> AI4Science 图谱，如何颠覆 10 年 x 20 亿美金成本的药物研发模式>> OpenEvidence，医疗领域诞生了第一个广告模式 Chatbot>> Flagship 创始人：AI for Science 的下一步是 Multi-agent>> Anthropic 创始人最看好的领域，AI for Science 深度解读Chai Discovery：这是一家成立于 2024 年的 AI 初创公司，专注于通过 AI 预测和再编程生化分子结构，加速新药研发进程。去年 9 月获得了 Thrive 和 OpenAI 3000 万美金的种子轮投资，估值达到 1.5 亿美金。他们的模型 Chai-1 选择的技术路线是用 Diffusion 模型做结构预测，和 AlphaFold 路线接近，今年 6 月又发布了最新模型 Chai-2。Score-based generative modeling：这是一种生成模型方法，核心思想是学习数据分布的“score function”，即对数密度函数的梯度。与传统的生成对抗网络或变分自编码器不同，这种方法不直接生成样本，而是通过一个随机微分方程从噪声出发，逐步将样本转化为数据分布中的真实样本。Entos AI（现称 Iambic Therapeutics）：是一家 AI 驱动小分子药物发现初创公司，依托自身专有的 OrbNet 平台，将量子力学融入机器学习，加速预筛选化合物、提高准确性。卓然的 PhD 导师 Tom Miller 是创始人兼 CEO。NeuralPLexer2 和 NeuralPLexer3：这是由 Caltech 的 Thomas F. Miller III 等人在内的研究团队开发的一系列用于大规模分子结构预测和生成的深度学习模型，主要面向量子化学和计算分子科学等领域。这些模型在保留物理精度的同时，大幅提升了计算效率。酵母展示和噬菌体展示：这是两种常见的体外蛋白筛选技术，用于发现与特定靶标具有高亲和力的抗体或蛋白分子。它们通过将蛋白质或抗体片段表达在微生物（如酵母或噬菌体病毒）表面，然后利用筛选和富集过程找到目标结合物。Lab-in-the-loop optimization：是一种将实验反馈与机器学习模型相结合的优化方法，常用于蛋白质或药物分子设计流程中。该方法通过迭代过程进行优化，模型首先生成候选序列，随后通过实验验证性能，再将实验数据反馈给模型，来指导下一轮设计。通过这种方式，能够持续提升设计的效率和准确性。这种方法代表了一种“模型+实验”协同进化的设计理念，与完全依赖模型的“零样本生成”策略不同。DockQ：用于评估蛋白质复合物对接质量的综合评分指标，介于 0 和 1 之间，数值越高表示预测结构越接近真实结构。通常，DockQ > 0.23 被视为是正确对接的阈值，用以判定一个复合结构是否可信。Humira：这是全球首个由噬菌体展示技术筛选获得并成功商业化的全人源单克隆抗体药物，最初由 Cambridge Antibody Technology（后并入阿斯利康）开发，并由 Abbott（现为 AbbVie）推广上市。
