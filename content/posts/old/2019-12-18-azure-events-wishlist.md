---
title: Announcing Azure Events Wishlist
slug: azure-events-wishlist
date: '2019-12-18T17:46:00'
updated: '2019-12-18T17:48:09.360127+00:00'
draft: false
tags:
- EventGrid
author: Sean Feldman
---
Azure Event Grid is by far not a new kid on the block. [Announced](https://azure.microsoft.com/en-ca/blog/announcing-the-general-availability-of-azure-event-grid/) in January 2018, the service promised to get us closer to the event-driven architecture and replace the cumbersome polling for communication between services with a simple mechanism - pub/sub. Other the course of two years, we've seen some Azure services adding a few events, unleashing the power of Event Grid. Yet the list of services and their corresponding events are still shy to call it done-done. Current services providing _some_ events are:

- [Azure Subscriptions](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-subscriptions) 9
- [Blob Storage](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-blob-storage) 2
- [Container Registry](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-container-registry) 4
- [EventHubs](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-container-registry) 1
- [IoT Hub](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-iot-hub) 5
- [Key Vault](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-key-vault) 9
- [Media Services](https://docs.microsoft.com/en-us/azure/media-services/latest/media-services-event-schemas) 7
- [Resource Groups](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-resource-groups) 9
- [Service Bus](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-service-bus) 2
- [Azure Maps](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-azure-maps) 3
- [Azure App Configuration](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-app-configuration) 2
- [Azure SignalR](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-azure-signalr) 2
- [Azure Machine Learning](https://docs.microsoft.com/en-us/azure/event-grid/event-schema-machine-learning) 4

While the list is impressive, not all Azure services have been on-boarded, and many events are still missing — event for the services that have already been on-boarded. While EventGrid is the underlying engine, each Azure product team manages its backlog of the requested events. Sometimes it's via UserVoice forums. Other times it's via internal backlogs. And often, via service-specific various channels that are not always easy to access, track, participate, and get updated until today.

Say hello to the Azure Events Wishlist repository. This has a particular objective - help Azure services teams and users bridge the gap of identifying, requesting, discussing, and get notified about new events added. 

How does it work?

Are you looking for an event to be provided by a specific Azure service? Raise an issue describing what the event should be, tag it against one of the 100+ Azure services. By doing so, you'll be sending a message to the service team and allow them to interact with the community to understand how valuable an event is and wherever it should be added.

Found an already created event idea? No problem. Help the community to emphasize the importance of the event by upvoting the idea. Participate in the discussions by adding real-world use cases via comments.

The repository will serve as a consolidated source of the ideas, hopefully enabling a conversation about the needed events from various services in **the open**, and allow everyone interested track it with an ease GitHub is providing.

So, what are you waiting for? Add the missing events and spread the word about [https://github.com/SeanFeldman/azure-events-wishlist](https://github.com/SeanFeldman/azure-events-wishlist).
