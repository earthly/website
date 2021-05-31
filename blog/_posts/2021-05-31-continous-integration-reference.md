---
title: "Continous Integration and Continous Deployment Glossary"
categories:
  - Reference
author: Adam
deployment:
 - title: Blue-Green Deployment
   description:
    A software development practice where you deploy two identical production environments. The "blue" environment is the production environment that receives all traffic. The "green" is a duplicate of the "blue". Changes are deployed to the "green" first. Once they have been verified, the "blue" environment is also updated.
 - title: Canary Deployment
   description: 
    A technique where a new version of the software is released to a subset of users, usually a small percentage. This allows the team to monitor the new version for adverse effects. It is named after the canary in the coal mine which allowed miners to tell if it was safe to continue deeper into the mine.
 - title: Red-Black Deployment
   description: A deployment strategy in which you deploy to a new environment, verify that it works, and then switch all traffic to the new environment. This is a synonym for Blue-Green Deployment that had its origins at Netflix.  
 - title: Rolling Update Deployment Strategy
   description: A term commonly used in Kubernetes where instances of a new version of the service are added gradually, and instances of the old services are gradually and gracefully terminated.  
 - title: Shadow Deployment
   description: In a Shadow Deployment the new version of a service is deployed side by side with the existing production version. All requests to the production version are duplicated and sent to the shadow version as well. This is useful for testing performance and stability but care must be taken to ensure non-idempotent actions are mocked or stubbed out.
 - title: Dark Deployment
   description: A new feature or service is deployed to production but not available for use to users.  Often feature flags are used to enable dark features for select users.
 - title: A / B Testing
   description: A software development practice where a new version of software is released to a subset of users and compared to the existing version. The results of the two versions are compared and the version with the best performance is kept.
devops:
 - title: Feature Flag
   description: A mechanism to enable or disable specific features based on certain criteria. The visibility of features to specific users or groups can be controlled by simply flipping a flag. This allows you to release a new feature to a subset of users, monitor their behavior, and if it doesn't work as expected, turn it off and try something else.
 - title: Continous Integration
   description: 
    A software development practice where members of a team integrate their work frequently. An automated build verfies the integration by running a test suite. This helps to detect errors as quickly as possible.
   link: "[see more](/blog//blog/continuous-integration/)"
 - title: Continuous Deployment
   description:
    A software development practice where teams release software to a production environment with the intent of updating it frequently. The actual act of deployment is automated and can be done as frequently as desired.
 
    
  
   
  
 
    
---

Continuous Integration terminology can seem foreign or confusing at first glance. Here we are collecting commonly used build terminology to help demystify the field.

## DevOps Terms

{% assign terms = page.devops | to_title_order %}
{% for term in terms %}
  <h3>{{ term.title }}</h3>
  <p>{{ term.description }}</p>
  {% if term.link  %}
  <p>{{ term.link }}</p> 
  {% endif %}
{% endfor %}

## Deployment Terms
{% assign terms = page.deployment | to_title_order %}
{% for term in terms %}
  <h3>{{ term.title }}</h3>
  <p>{{ term.description }}</p>
  {% if term.link  %}
  <p>{{ term.link }}</p> 
  {% endif %}
{% endfor %}

## Suggestions

If you'd like to see additional terms added please reach out to us on twitter or via email.