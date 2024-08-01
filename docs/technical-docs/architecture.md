---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Jane Dane]

{: .no_toc }
# Architecture

{: .attention }
> This page describes how the application is structured and how important parts of the app work. It should give a new-joiner sufficient technical knowledge for contributing to the codebase.
> 
> See [this blog post](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html) for an explanation of the concept and these examples:
>
> + <https://github.com/rust-lang/rust-analyzer/blob/master/docs/dev/architecture.md>
> + <https://github.com/Uriopass/Egregoria/blob/master/ARCHITECTURE.md>
> + <https://github.com/davish/obsidian-full-calendar/blob/main/src/README.md>
> 
> For structural and behavioral illustration, you might want to leverage [Mermaid](../ui-components.md), e.g., by charting common [C4](https://c4model.com/) or [UML](https://www.omg.org/spec/UML) diagrams.
> 
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

Unser Projekt ist eine Webanwendung, die mit Flask entwickelt wurde. Der mit „flask run“ gestartete Server verwendet eine Datei mit den Routen, um die Navigation zwischen HTML-Seiten zu verwalten.

Wir nutzen die Yelp Fusion API, um Restaurantdaten abzurufen und sicherzustellen, dass keine doppelten Einträge vorhanden sind, indem wir einen Code implementiert haben, der eindeutige Restaurants überprüft und speichert. Der API-Schlüssel wird sicher in einer separaten JSON-Datei gespeichert und nicht auf das Repository gepushed, da sonst der Service Key von Firebase "disabled" wird.

Firestore wird zum Speichern der Restaurantdaten verwendet. Darüber hinaus nutzen wir die Firebase Authentication für die Benutzerregistrierung und -anmeldung.

## Codemap

[Describe how your app is structured. Don't aim for completeness, rather describe *just* the most important parts.]

### firebase.js

### __inti__,py

### save_to_firestore.py

### delizia-xxx.json

### firebase_auth.py

### package-lock.json

### package.json

### yelp_api.py



## Cross-cutting concerns

[Describe anything that is important for a solid understanding of your codebase. Most likely, you want to explain the behavior of (parts of) your application. In this section, you may also link to important [design decisions](../design-decisions.md).]

### Yelp Fusion API

