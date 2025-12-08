---
layout: archive
title: "News"
permalink: /news/
author_profile: true
---

{% include base_path %}

<style>
  .news-item {
    margin-bottom: 2em;
    padding: 1.5em;
    border-left: 4px solid #2c3e50;
    background-color: #f8f9fa;
  }
  
  .news-date {
    color: #7f8c8d;
    font-size: 0.9em;
    margin-bottom: 0.5em;
  }
  
  .news-title {
    font-size: 1.2em;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 0.5em;
  }
  
  .news-excerpt {
    color: #555;
    line-height: 1.6;
  }
  
  .news-link {
    display: inline-block;
    margin-top: 0.5em;
    color: #3498db;
    text-decoration: none;
  }
  
  .news-link:hover {
    text-decoration: underline;
  }
  
  .year-divider {
    margin: 2em 0 1em 0;
    border-bottom: 2px solid #2c3e50;
    padding-bottom: 0.5em;
  }
</style>

# Recent News & Highlights

{% assign news_by_year = site.news | group_by_exp: "item", "item.date | date: '%Y'" | sort: "name" | reverse %}

{% for year in news_by_year %}
  <h2 class="year-divider">{{ year.name }}</h2>
  {% assign sorted_news = year.items | sort: "date" | reverse %}
  {% for item in sorted_news %}
    <div class="news-item">
      <div class="news-date">
        {{ item.date | date: "%B %Y" }}
      </div>
      <div class="news-title">{{ item.title }}</div>
      <div class="news-excerpt">{{ item.excerpt }}</div>
      <a href="{{ base_path }}{{ item.url }}" class="news-link">Read more →</a>
    </div>
  {% endfor %}
{% endfor %}
