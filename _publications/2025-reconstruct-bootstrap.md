---
title: "A Reconstruct-then-Bootstrap Test for the Sufficiency of Diffusion Processes"
collection: publications
category: manuscripts_in_prep
permalink: /publication/2025-reconstruct-bootstrap
excerpt: 'A novel statistical test to assess whether a diffusion process model is sufficient for observed time series data, using Kramers-Moyal expansion and bootstrap methods.'
date: 2025-01-01
venue: 'Submitted'
paperurl: 'http://psyarxiv.com/h2dqu_v1'
authors: 'Kathleen Medriano, Joachim Vandekerckhove'
---

Diffusion processes are commonly used in the modeling of time series that exhibit stationarity and Markovianity. However, those two properties do not guarantee that a diffusive process is sufficient for the time series. In this paper, we develop a test for the sufficiency of a diffusion process for an observed time series. 

To develop the test we capitalize on the Kramers-Moyal (KM) expansion: a Taylor expansion of the integral form of the master equation that describes Markov continuous-time processes. In the idealized case, if the observed data indeed arise from a true diffusion process, then the KM expansion should truncate naturally after the second term, meaning any higher-order (≥ 3) KM coefficients should be zero. 

However, in practice, the discrete nature of measurement introduces artificial higher-order KM coefficients, even when the underlying process is truly diffusive. Nonetheless, for genuinely diffusive systems, the sampling distribution of a statistic associated with higher-order coefficients will be different than non-diffusive ones. This is a viable avenue for testing the appropriateness of a diffusion model given an observed time series. 

We propose a meaningful statistic that could inform whether or not a diffusion model is sufficient for a given time series. We then build a test that involves reconstructing the diffusion equation to generate surrogate paths, yielding a bootstrap distribution against which the observed statistic could be compared. We evaluate the sensitivity and selectivity of the proposed test in Monte Carlo studies.

