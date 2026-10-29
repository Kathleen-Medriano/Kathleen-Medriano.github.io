---
permalink: /
title: "About"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% include base_path %}

I'm a PhD student in Cognitive Sciences at the University of California, Irvine, where I have studied since September 2022. I completed an MS in Statistics at UC Irvine from September 2022 to December 2024. My dissertation is on methods for time series data in the cognitive sciences, advised by Joachim Vandekerckhove. My research sits at the intersection of cognitive science, statistics, and computational modeling.

## Research Interests

My work centers on understanding complex cognitive processes through statistical and mathematical modeling. I specialize in:

- **Time Series Analysis**: Developing and applying temporal models to understand cognitive dynamics
- **Bayesian and Statistical Modeling**: Building statistical frameworks for cognitive science research, with a proper accounting of uncertainty
- **Model Discovery**: Developing data-driven algorithms to identify plausible generative models for cognitive data

## Current Research

<!-- - **Diffusion process sufficiency**: A reconstruct-then-bootstrap test of whether a diffusion process is sufficient for an observed time series, published in *Computational Brain & Behavior* (2026) -->
- **Model discovery for hierarchical datasets**: Data-driven discovery of parsimonious models for hierarchical datasets in the cognitive and behavioral sciences

## Academic Background

I began with a BS in Psychology at the University of Santo Tomas (June 2012–June 2016), which gave me a foundation in human cognition and behavior. I then completed a Graduate Diploma in Mathematics at the University of the Philippines Diliman (August 2017–July 2019). At UC Irvine I earned an MS in Statistics (September 2022–December 2024) and am pursuing a PhD in Cognitive Sciences (September 2022–present). That sequence lets me connect questions about human cognition with statistical inference, Bayesian modeling, and computational methods.

## Recent News & Highlights

<style>
  .home-news-list {
    list-style: none;
    padding-left: 0;
  }
  
  .home-news-list li {
    margin-bottom: 0.8em;
  }
  
  .view-all-news {
    margin-top: 1em;
  }
  
  .view-all-news a {
    color: #3498db;
    text-decoration: none;
    font-weight: 500;
  }
  
  .view-all-news a:hover {
    text-decoration: underline;
  }
</style>

<ul class="home-news-list">
{% assign recent_news = site.news | sort: "date" | reverse | limit: 3 %}
{% for item in recent_news %}
  <li>{{ item.title }}, {{ item.date | date: "%B %Y" }}</li>
{% endfor %}
</ul>

<div class="view-all-news">
  <a href="{{ base_path }}/news/">View all news →</a>
</div>
