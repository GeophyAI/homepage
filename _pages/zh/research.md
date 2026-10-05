---
layout: page
lang: zh-CN
permalink: /zh/research/
title: 研究
description: 目前在做的两个方向。
nav: false
---

### 隐式全波形反演成像

<div class="research-fig">
{% include figure.liquid loading="eager" path="assets/img/research/ifwim_field.png" class="img-fluid rounded z-depth-1" zoomable=true alt="IFWIM 实际数据结果：速度与反射系数" caption="实际数据结果：反演得到的速度（上），以及反射系数分量 R<sub>z</sub>、R<sub>x</sub>（中、下）。点击图片可以放大。" %}
</div>

常规做法分两步：先用全波形反演（FWI）求速度，再用最小二乘逆时偏移求反射系数。隐式 FWI 成像（IFWIM）把速度和阻抗模型都用神经网络的权重来表示，结合矢量反射系数声波方程一起反演，反射系数再由反演出来的阻抗算出来。因为模型是连续函数，所以可以按任意分辨率重采样，不规则网格也能用。

[论文（GJI 2026）](https://doi.org/10.1093/gji/ggag277) · [代码](https://github.com/DeepWave-KAUST/ifwi-pub)

### SWEEP：可微分的波动物理

{% include sweepx_map.liquid alt="SWEEPX 生态：核心引擎 sweep-solver 及其周边的各个包" %}

<p class="caption">带 <i class="fa-solid fa-arrow-up-right-from-square"></i> 的组件可以点击，跳到对应的代码仓库。</p>

SWEEP（Seismic Wave Equation Exploration Platform）是一个统一的可微分波动方程求解框架。核心引擎 sweep-solver 支持 20 多种波动方程，2D、3D 都能算，后端有 PyTorch、JAX 和 CUDA。围绕它的 SWEEPX 生态还有多卡任务调度、地震数据读写、优化器、目标函数、层析初始模型、神经网络重参数化这些包，另外还有一个能用大白话提问的助手。

[文档](https://sweepx.deepwave.group/) · [预印本](https://arxiv.org/abs/2604.14189) · `pip install sweepx`

<style>
  .research-fig { max-width: 520px; margin: 0 auto; }
</style>
