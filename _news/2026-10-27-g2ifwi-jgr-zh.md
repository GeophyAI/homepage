---
layout: post
date: 2026-10-27
inline: true
related_posts: false
lang: zh-CN
---

论文 [G²IFWI: Gradient-coupled diffusion priors for regularizing implicit full waveform inversion](https://doi.org/10.1029/2026JH001488) 在 *JGR: Machine Learning and Computation* 正式发表，第一作者是 Linrong Wang。思路是把扩散模型先验的 score 梯度和隐式 FWI 的物理梯度放在一起优化；有井的时候，还能通过 guidance 把测井数据加进来。
