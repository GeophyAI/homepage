---
layout: page
permalink: /research/
title: research
description: Two directions I am working on right now.
nav: true
nav_order: 2
---

### Implicit full-waveform inversion imaging

<div class="research-fig">
{% include figure.liquid loading="eager" path="assets/img/research/ifwim_field.png" class="img-fluid rounded z-depth-1" zoomable=true alt="IFWIM field-data results: velocity and reflectivity" caption="Field-data example: inverted velocity (top) and the reflectivity components R<sub>z</sub> and R<sub>x</sub> (middle, bottom). Click to enlarge." %}
</div>

Subsurface images are usually obtained in two steps: full-waveform inversion (FWI) for the velocity, then least-squares reverse time migration for the reflectivity. Implicit FWI imaging (IFWIM) represents the velocity and impedance models with the weights of a neural network and inverts them jointly with the vector-reflectivity acoustic wave equation; the reflectivity components then follow from the inverted impedance. Because the models are continuous functions, they can be resampled at any resolution, even on irregular grids.

[Paper (GJI 2026)](https://doi.org/10.1093/gji/ggag277) · [Code](https://github.com/DeepWave-KAUST/ifwi-pub)

### SWEEP: differentiable wave physics

{% include sweepx_map.liquid %}

<p class="caption">Components marked <i class="fa-solid fa-arrow-up-right-from-square"></i> open their repositories.</p>

SWEEP (Seismic Wave Equation Exploration Platform) is a unified solver framework for differentiable wave physics. Its engine, sweep-solver, covers more than 20 wave equations in 2-D and 3-D with PyTorch, JAX and CUDA backends. Around it, the SWEEPX ecosystem adds packages for multi-GPU job running, seismic I/O, optimization, misfit functions, tomography starting models and neural reparameterization, plus an agent you can ask in plain language.

[Documentation](https://sweepx.deepwave.group/) · [Preprint](https://arxiv.org/abs/2604.14189) · `pip install sweepx`

<style>
  .research-fig { max-width: 520px; margin: 0 auto; }
</style>
