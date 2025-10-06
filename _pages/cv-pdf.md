---
layout: cv-pdf
title: "CV"
permalink: /cv-pdf/
author_profile: false
---

{% assign cv = site.data.cv %}

<div class="cv-container">
  <!-- Basic Information -->
  <div class="cv-section cv-header">
    <h1>{{ cv.basics.name }}</h1>
    {% if cv.basics.label %}
    <h2>{{ cv.basics.label }}</h2>
    {% endif %}
    
    <div class="cv-contact">
      {% if cv.basics.email %}
      <div class="cv-contact-item">
        <i class="fas fa-envelope"></i> {{ cv.basics.email }}
      </div>
      {% endif %}
      
      {% if cv.basics.phone %}
      <div class="cv-contact-item">
        <i class="fas fa-phone"></i> {{ cv.basics.phone }}
      </div>
      {% endif %}
      
      {% if cv.basics.website %}
      <div class="cv-contact-item">
        <i class="fas fa-globe"></i> {{ cv.basics.website }}
      </div>
      {% endif %}
      
      {% if cv.basics.location.city %}
      <div class="cv-contact-item">
        <i class="fas fa-map-marker-alt"></i> {{ cv.basics.location.city }}{% if cv.basics.location.region %}, {{ cv.basics.location.region }}{% endif %}{% if cv.basics.location.countryCode %}, {{ cv.basics.location.countryCode }}{% endif %}
      </div>
      {% endif %}
    </div>
  </div>

  <!-- Summary -->
  {% if cv.basics.summary %}
  <div class="cv-section">
    <h2>Summary</h2>
    <p>{{ cv.basics.summary }}</p>
  </div>
  {% endif %}

  <!-- Education -->
  {% if cv.education and cv.education.size > 0 %}
  <div class="cv-section">
    <h2>Education</h2>
    {% for education in cv.education %}
    <div class="cv-entry">
      <div class="cv-entry-header">
        <div class="cv-entry-title">{{ education.area }}{% if education.studyType %}, {{ education.studyType }}{% endif %}</div>
        <div class="cv-entry-date">
          {% if education.startDate %}{{ education.startDate }} - {% endif %}{{ education.endDate }}
        </div>
      </div>
      <div class="cv-entry-organization">{{ education.institution }}</div>
      {% if education.gpa %}
      <div>GPA: {{ education.gpa }}</div>
      {% endif %}
      {% if education.courses and education.courses.size > 0 %}
      <div class="cv-entry-description">
        <strong>Relevant Coursework:</strong>
        <ul>
          {% for course in education.courses %}
          <li>{{ course }}</li>
          {% endfor %}
        </ul>
      </div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Work Experience -->
  {% if cv.work and cv.work.size > 0 %}
  <div class="cv-section">
    <h2>Work Experience</h2>
    {% for work in cv.work %}
    <div class="cv-entry">
      <div class="cv-entry-header">
        <div class="cv-entry-title">{{ work.position }}</div>
        <div class="cv-entry-date">
          {% if work.startDate %}{{ work.startDate }} - {% endif %}{% if work.endDate %}{{ work.endDate }}{% else %}Present{% endif %}
        </div>
      </div>
      <div class="cv-entry-organization">{{ work.company }}{% if work.location %}, {{ work.location }}{% endif %}</div>
      {% if work.summary %}
      <div class="cv-entry-description">{{ work.summary }}</div>
      {% endif %}
      {% if work.highlights and work.highlights.size > 0 %}
      <div class="cv-entry-description">
        <ul>
          {% for highlight in work.highlights %}
          <li>{{ highlight }}</li>
          {% endfor %}
        </ul>
      </div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Skills -->
  {% if cv.skills and cv.skills.size > 0 %}
  <div class="cv-section">
    <h2>Skills</h2>
    {% for skill in cv.skills %}
    <div class="cv-entry">
      <div class="cv-entry-title">{{ skill.name }}{% if skill.level %} ({{ skill.level }}){% endif %}</div>
      {% if skill.keywords and skill.keywords.size > 0 %}
      <div>{{ skill.keywords | join: ", " }}</div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Awards -->
  {% if cv.awards and cv.awards.size > 0 %}
  <div class="cv-section">
    <h2>Awards & Honors</h2>
    {% for award in cv.awards %}
    <div class="cv-entry">
      <div class="cv-entry-header">
        <div class="cv-entry-title">{{ award.title }}</div>
        <div class="cv-entry-date">{{ award.date }}</div>
      </div>
      {% if award.awarder %}
      <div class="cv-entry-organization">{{ award.awarder }}</div>
      {% endif %}
      {% if award.summary %}
      <div class="cv-entry-description">{{ award.summary }}</div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Publications -->
  {% if cv.publications and cv.publications.size > 0 %}
  <div class="cv-section">
    <h2>Publications</h2>
    {% for publication in cv.publications %}
    <div class="cv-entry">
      <div class="cv-entry-title">{{ publication.name }}</div>
      {% if publication.publisher %}
      <div class="cv-entry-organization">{{ publication.publisher }}{% if publication.releaseDate %}, {{ publication.releaseDate }}{% endif %}</div>
      {% endif %}
      {% if publication.summary %}
      <div class="cv-entry-description">{{ publication.summary }}</div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Projects -->
  {% if cv.projects and cv.projects.size > 0 %}
  <div class="cv-section">
    <h2>Projects</h2>
    {% for project in cv.projects %}
    <div class="cv-entry">
      <div class="cv-entry-header">
        <div class="cv-entry-title">{{ project.name }}</div>
        {% if project.startDate or project.endDate %}
        <div class="cv-entry-date">
          {% if project.startDate %}{{ project.startDate }} - {% endif %}{% if project.endDate %}{{ project.endDate }}{% else %}Ongoing{% endif %}
        </div>
        {% endif %}
      </div>
      {% if project.description %}
      <div class="cv-entry-description">{{ project.description }}</div>
      {% endif %}
      {% if project.highlights and project.highlights.size > 0 %}
      <div class="cv-entry-description">
        <ul>
          {% for highlight in project.highlights %}
          <li>{{ highlight }}</li>
          {% endfor %}
        </ul>
      </div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Languages -->
  {% if cv.languages and cv.languages.size > 0 %}
  <div class="cv-section">
    <h2>Languages</h2>
    {% for language in cv.languages %}
    <div class="cv-entry">
      <div class="cv-entry-title">{{ language.language }}{% if language.fluency %} ({{ language.fluency }}){% endif %}</div>
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Interests -->
  {% if cv.interests and cv.interests.size > 0 %}
  <div class="cv-section">
    <h2>Interests</h2>
    {% for interest in cv.interests %}
    <div class="cv-entry">
      <div class="cv-entry-title">{{ interest.name }}</div>
      {% if interest.keywords and interest.keywords.size > 0 %}
      <div>{{ interest.keywords | join: ", " }}</div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% endif %}

  <!-- Online Profiles -->
  {% if cv.basics.profiles and cv.basics.profiles.size > 0 %}
  <div class="cv-section">
    <h2>Online Profiles</h2>
    <div>
      {% for profile in cv.basics.profiles %}
      <div class="cv-profile-link">
        <strong>{{ profile.network }}:</strong> {{ profile.url }}
      </div>
      {% endfor %}
    </div>
  </div>
  {% endif %}
</div>

<script>
  // Add a print button and auto-focus for PDF generation
  window.addEventListener('load', function() {
    // Add print instructions
    const printInstructions = document.createElement('div');
    printInstructions.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: #333;
      color: white;
      padding: 10px;
      border-radius: 5px;
      font-size: 14px;
      z-index: 1000;
      box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    `;
    printInstructions.innerHTML = `
      <div>Press Ctrl+P (or Cmd+P) to save as PDF</div>
      <div style="margin-top: 5px; font-size: 12px;">
        In print dialog, select "Save as PDF" as destination
      </div>
    `;
    document.body.appendChild(printInstructions);
    
    // Hide instructions after 5 seconds
    setTimeout(() => {
      printInstructions.style.opacity = '0';
      printInstructions.style.transition = 'opacity 0.5s';
      setTimeout(() => printInstructions.remove(), 500);
    }, 5000);
  });
</script>