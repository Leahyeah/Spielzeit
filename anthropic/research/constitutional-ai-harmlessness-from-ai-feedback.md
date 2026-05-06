---
title: "Constitutional AI: Harmlessness from AI Feedback"
url: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
date: "Dec 15, 2022"
category: "Alignment Research"
description: "Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems."
source: Anthropic Research
---

# Constitutional AI: Harmlessness from AI Feedback

Alignment Research | Dec 15, 2022

> Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems.

## External Links

- https://arxiv.org/abs/2212.08073

## Archived Content

Alignment Research

# Constitutional AI: Harmlessness from AI Feedback

Dec 15, 2022 [Read Paper](https://arxiv.org/abs/2212.08073)

## Abstract

As AI systems become more capable, we would like to enlist their help to supervise other AIs. We experiment with methods for training a harmless AI assistant through self-improvement, without any human labels identifying harmful outputs. The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'. The process involves both a supervised learning and a reinforcement learning phase. In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses. In the RL phase, we sample from the finetuned model, use a model to evaluate which of the two samples is better, and then train a preference model from this dataset of AI preferences. We then train with RL using the preference model as the reward signal, i.e. we use 'RL from AI Feedback' (RLAIF). As a result we are able to train a harmless but non-evasive AI assistant that engages with harmful queries by explaining its objections to them. Both the SL and RL methods can leverage chain-of-thought style reasoning to improve the human-judged performance and transparency of AI decision making. These methods make it possible to control AI behavior more precisely and with far fewer human labels.

## Policy Memo

[Constitutional AI Policy Memo](https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf)

[](https://twitter.com/intent/tweet?text=https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) [](https://www.linkedin.com/shareArticle?mini=true&url=https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)

## Related content

### How people ask Claude for personal guidance

[Read more](https://www.anthropic.com/research/claude-personal-guidance)

### Evaluating Claude’s bioinformatics research capabilities with BioMysteryBench

[Read more](https://www.anthropic.com/research/Evaluating-Claude-For-Bioinformatics-With-BioMysteryBench)

### Announcing the Anthropic Economic Index Survey

We're launching the Anthropic Economic Index Survey, a monthly survey conducted through Anthropic Interviewer.

[Read more](https://www.anthropic.com/research/economic-index-survey-announcement)
