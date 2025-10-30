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
featuredImage: '/posts/handling-api-calls-like-a-king/handling-api-calls-like-a-king.webp'
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

The internal backend implementation is already capable of processing requests that arrive as messages on Azure Service Bus. With a little bit of configuration, and I mean Bicep, it's possible to expose an HTTP endpoint to accept requests, "massage" those, turn into ASB messages, and post to the necessary queue or topic. This can be done with fire and forget approach using the new APIM policy `send-service-bus-message` (in public preview as of writting of this post), or send a message off to ASB, ensuring it has been ingested successfully, and return success or the error code after that, using `send-request` policy. Personally, I prefer the later for now as it's not returning blindly 201, but indicates if there's a failure. And the error can be controlled to ensure you're not leaking anything sensitive.

```mermaid
graph LR
    3rd[3rd Party] -- HTTP call --> apim[APIM]
    apim -- ASB message -->func[Functions App]
    apim -. 201 -.-> 3rd
```

### Quering

This is the easy part. Validate the HTTP call, rate limit with `rate-limit` policy to stop abusing callers, 

```mermaid
graph LR
    3rd[3rd Party] -- HTTP call --> apim[APIM]
    apim -- HTTP call -->func[Functions App]
    func -. Response -.-> apim
    apim -. response -.-> 3rd
```

## Pros and Cons

When it comes to buy vs build, if you find yourself on the building side, you might not like APIM. But there are more positives than negatives. Here are just a few.

`validate-content` policy: Validate the incoming request against a schema and reject a request that doesn't adhare to the required scheme. Validations requiere compute power, that's likely taken away from the processing of proper requests. With APIM, you get it OOTB even before it hits your other services/compute. A fantastic feature for public API.

`rewrite-uri` policy: Ability to re-route from a public APIM URI to the internal URI w/o exposing it. Besides internalizing your services, this is extremely handy when APIs become more sophisticated, or routing depends on the client, or paramters, or something else. Having this ability OOTB is an effortless win.

`set-header` policy: Customizing headers by enriching during processing at APIM level. Header stampting, augementation, or even stripping.

And don't get me started about the security. Being able to provision an APIM subscription per client, with products (grouping of APIs) and giving access to products based on subscription is such a time saver.

## Verdict

Azure API Management is a handy service that is worth keeping.