---
title: Architecture
parent: Technical Docs
nav_order: 1
---



{: .no_toc }
# Architecture 

<details open markdown="block">

<summary>Table of contents</summary>
+ ToC
{: toc }
  
</details>

## Overview

Unser Projekt ist eine Webanwendung, die mit Flask entwickelt wurde. Der mit „flask run“ gestartete Server verwendet eine Datei mit den Routen, um die Navigation zwischen HTML-Seiten zu verwalten.

Wir nutzen die Yelp Fusion API, um Restaurantdaten abzurufen und sicherzustellen, dass keine doppelten Einträge vorhanden sind, indem wir einen Code implementiert haben, der eindeutige Restaurants überprüft und speichert. Der API-Schlüssel wird sicher in einer separaten JSON-Datei gespeichert und nicht auf das Repository gepushed, da sonst der Service Key von Firebase "disabled" wird.

Firestore wird zum Speichern der Restaurantdaten verwendet. Darüber hinaus nutzen wir die Firebase Authentication für die Benutzerregistrierung und -anmeldung.

## Codemap

### firebase.js
Der JavaScript-Code integriert Firebase-Dienste und konzentriert sich dabei auf Initialisierung und Benutzerauthentifizierung. Es werden wesentliche Funktionen aus dem Firebase SDK importiert: initializeApp zum Einrichten der Firebase-Anwendung und getAnalytics zum Aktivieren von Firebase Analytics. Die Firebase-App wird dann mit initializeApp(firebaseConfig) initialisiert und Analytics wird mit getAnalytics(app) aktiviert.
Drei Funktionen handhaben die Benutzerauthentifizierung: registerUser(email, password) erstellt ein neues Benutzerkonto mit der Methode createUserWithEmailAndPassword von Firebase Authentication, loginUser(email, password) meldet einen vorhandenen Benutzer mit der Methode signInWithEmailAndPassword an und logoutUser() meldet den aktuellen Benutzer mit der Methode signOut ab. Diese Funktionen werden zur Verwendung in anderen Teilen der Anwendung exportiert.

### __init__.py
In dieser Datei sind die Routen für unsere Flask-Webanwendung. Die Routen, die besonders wichtig sind für die Kernfunktion unserer Applikation, sind zum einen die Abfrage der Firestore-Datenbank, um alle Restaurants anzuzeigen (z. B. category/all), und die Routen, die die Restaurants mit gefilterten Listen anzeigen (z. B. category/vegan).

### save_to_firestore.py & yelp_api.py
Der Code in diesen Dateien sorgt dafür, dass die entsprechenden Yelp-Daten abgerufen und in Firestore (Firebase Datenbank) gespeichert werden. Wir haben die Suchanfragen auf 15 beschränkt, da wir nur eine begrenzte Anzahl an API-Calls hatten und versucht haben für jede Kategorie ca. 15 Restaurants bereitzustellen. 

### delizia-xxx.json
Das ist eine JSON-Datei, die wir mit einer Anleitung auf der Firebase-Webseite erstellt haben. Sie wird genutzt, um die Verbindung zur Firestore-Datenbank herzustellen und die Daten von Yelp zu speichern. Außerdem ist es wichtig zu erwähnen, dass wir diese Dateien nicht in unser GitHub-Repository pushen konnten, da Google die Verbindung automatisch sperrt, wenn dies versucht wird („Google automatically disables service account keys detected in public repositories.“).

### firebase_auth.py
Die Datei verwendet die Bibliothek „requests“, um über REST-API-Aufrufe mit Firebase Authentication zu interagieren und Funktionen für die Benutzerregistrierung und -anmeldung zu definieren. FIREBASE_WEB_API_KEY enthält den API-Schlüssel, der zur Authentifizierung von Anfragen an Firebase erforderlich ist.

Die Funktion „firebase_register“ registriert einen neuen Benutzer, indem sie eine E-Mail-Adresse und ein Kennwort entgegennimmt, die Anmelde-URL mit dem API-Schlüssel erstellt und eine POST-Anfrage mit den Benutzerdetails sendet. Sie gibt die JSON-Antwort des Servers zurück.
In ähnlicher Weise meldet die Funktion „firebase_login“ einen vorhandenen Benutzer an, indem sie eine E-Mail-Adresse und ein Kennwort entgegennimmt, die Anmelde-URL mit dem API-Schlüssel erstellt und eine POST-Anfrage mit den Benutzerdetails sendet. Sie gibt die JSON-Antwort des Servers zurück. Beide Funktionen geben die JSON-Antwort des Servers zurück, die Authentifizierungstoken und andere Benutzerdetails enthält.

### package-lock.json
Die Datei package-lock.json ist eine automatisch von Node Package Manager (npm) generierte Datei, die zum Sperren der genauen Versionen von Abhängigkeiten in einem Node.js-Projekt verwendet wird. Für unser Projekt gibt sie an, dass die Hauptabhängigkeit die Firebase-Version „^10.12.4“ ist. Diese Datei gewährleistet Konsistenz und Stabilität in verschiedenen Umgebungen, indem sie die genauen Versionen jedes installierten Pakets und seiner Abhängigkeiten aufzeichnet.

### package.json

Die package.json-Datei ist ebenfalls automatisch von npm generiert und verwaltet und wird in Node.js-Projekten zur Verwaltung von Abhängigkeiten verwendet. Er zeigt die direkten Abhängigkeiten des Projekts auf, in unserem Fall das Firebase-Paket mit einem Versionsbereich, der als „^10.12.4“ angegeben ist. Dies bedeutet, dass das Projekt mit allen kleineren oder Patch-Updates auf Version 10.12.4 kompatibel ist, z. B. 10.13.0 oder 10.12.5.


## Cross-cutting concerns

### Yelp Fusion API
Da uns nur für 30 Tage täglich 300 API-Aufrufe zur Verfügung standen, haben wir versucht pro Kategorie 15 Restaurants in unserer Firestore-Datenbank zu sammeln. Dabei mussten wir uns auch damit auseinandersetzen, dass  Restaurants nicht doppelt gesucht werden und wir deshalb API-Calls verlieren. Außerdem hatten wir das Problem, dass unser Service Account Key von Firebase gesperrt wurde, da wir die JSON-Datei mit dem Key in unser Github-Repository gepusht haben. Deshalb haben wir pro Person einen Service Key erstellt und haben somit das Problem gelöst. Das ist auch der Grund dafür, wieso wir für die Abgabe die JSON-Datei separat abgeben müssen.
