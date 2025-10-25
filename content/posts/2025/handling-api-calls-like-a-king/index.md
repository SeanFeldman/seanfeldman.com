---
author: Sean Feldman
title: Handling API Calls like a King 👑
slug: handling-api-calls-like-a-king
date: '2025-10-25'
summary: "Turn sync HTTP calls into resilient async flows with Azure API Management and queues—embracing backpressure, retries, and idempotency to keep APIs fast and reliable."
tags: 
  - APIM
  - AzureServiceBus
comments: true
featuredImage: 'posts/handling-api-calls-like-a-king/handling-api-calls-like-a-king.webp'
enableWordCount: false
enableReadingTime: true
toc:
  enable: true
draft: false  
---

## Open Sesame!

Recently, was looking at adding an external facing API to an internal system. The requirement was to add two endpoints. One endpoint to submit requests from a 3rd party. And the second endpoint to query for requests status.

The developer in my was drewling just by thinking about all the interesting things I could do: ASP.NET Minimal API, token management, response caching, throttling with the new .NET APIs, etc. So many things to try out to build out a public facing API that would down the road serve other rest parties that would be onboarded via API route.

But then I looked at the cost effectiveness, maintenance, and the complexities that would be added to the system that's 99% of the time is an internal system. After some considerations, the sober realization was that building is not worth it. And since the client's system is in Azure, there's that handy "little" service called Azure API Management (APIM) that can do most of it, if not all, for a fraction of the cost that would normally be associated with custom development. Speaking of a comoditization of code development!

### Submitting a Request

```mermaid
graph LR
    3rd[3rd Party] -- HTTP call --> apim[APIM]
    apim -- ASB message -->func[Functions App]
    apim -. 201 -.-> 3rd
```

### Quering

```mermaid
graph LR
    3rd[3rd Party] -- HTTP call --> apim[APIM]
    apim -- HTTP call -->func[Functions App]
    func -. Response -.-> apim
    apim -. response -.-> 3rd
```

## Pros and Cons


HTTP request --> APIM --> ASB