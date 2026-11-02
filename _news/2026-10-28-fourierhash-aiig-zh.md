---
layout: post
date: 2026-10-28
inline: true
related_posts: false
lang: zh-CN
---

论文 [Seismic data interpolation using implicit neural representations with Fourier-hash features](https://doi.org/10.1016/j.aiig.2026.100287) 在 *Artificial Intelligence in Geosciences* 正式发表（开放获取），第一作者是 Linrong Wang。思路是把 Fourier 编码和多分辨率哈希编码混着用：训练前期以 Fourier 特征为主，先把连续的整体结构补出来；后期逐渐交给哈希特征去补局部细节。整个过程只用实际记录到的道做自监督。
