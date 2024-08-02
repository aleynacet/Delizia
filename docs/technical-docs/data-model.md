---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[Jane Dane]

# Data model

![Data_Model](./assets/images/data_model.png)

Das folgende Entity Relationship Diagramm stellt den Datenfluss zwischen verschiedenen Komponenten unseres Projektes dar. Die API stellt Daten zu Restaurants bereit, die dann in der Datenbank von Firebase gespeichert und verwaltet werden. Die Front-End-Anwendung, mit der Benutzer interagieren, ruft die Daten von Firebase ab. Außerdem müssen sich Benutzer, bevor sie die Daten abrufen, registrieren und einloggen. Dafür ruft die Web-App die in Firebase gespeicherten Benutzeranmeldeinformationen zu Authentifizierungszwecken ab. 