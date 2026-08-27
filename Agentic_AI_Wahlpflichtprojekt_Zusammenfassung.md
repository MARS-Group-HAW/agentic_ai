# Wahlpflichtprojekt Agentic AI – Zusammenfassung der bisherigen Diskussionen und Ergebnisse

**Stand:** 27. August 2026  
**Kontext:** Bachelor Informatik, Wintersemester 2026/27  
**Format:** Wahlpflichtprojekt ohne begleitende Vorlesung, ca. 12 Praktikumstermine

---

## 1. Ausgangspunkt und Zielsetzung

Das Wahlpflichtprojekt soll sich nicht auf die reine Implementierung von KI-Agenten beschränken. Zentral ist vielmehr, dass die Studierenden **Agentic AI als sozio-technisches System** erleben und insbesondere Erfahrungen mit **Mixed Teams aus Menschen und KI-Agenten** sammeln.

Die Studierenden sollen daher lernen,

- Agenten technisch zu entwerfen und zu implementieren,
- Aufgaben sinnvoll zwischen Menschen und Agenten aufzuteilen,
- Agenten als echte Teammitglieder in Arbeitsprozesse zu integrieren,
- Fähigkeiten und Grenzen von Agenten realistisch einzuschätzen,
- Delegation, Kontrolle, Kommunikation und Eskalation in Mixed Teams zu gestalten,
- mit nicht-deterministischem Verhalten umzugehen,
- Qualität und Zuverlässigkeit agentischer Systeme zu evaluieren,
- selbstständig neue fachliche Domänen zu erschließen,
- und Softwareentwicklung als organisatorischen Prozess zu verstehen, nicht nur als Programmieraufgabe.

Ein wichtiges Lernziel ist ausdrücklich, dass die Studierenden **Vorteile und Herausforderungen der Zusammenarbeit zwischen Menschen und Agenten selbst erfahren**.

---

## 2. Rahmenbedingungen

Aus den bisherigen Diskussionen ergeben sich folgende Rahmenbedingungen:

- ca. **15–20 Studierende**
- Bachelor Informatik
- ca. **12 Projekttermine**
- jeweils **montags von 10:00 bis 16:00 Uhr**
- damit steht pro Termin ein vollständiger Projekttag zur Verfügung
- **keine Benotung**
- keine klassische begleitende Vorlesung
- projektorientiertes und weitgehend selbstständiges Arbeiten
- es kann vorkommen, dass der Lehrende an einzelnen Terminen **nicht anwesend** ist
- daher muss das Projekt organisatorisch so robust sein, dass die Teams weitgehend autonom arbeiten können
- technisch sollen möglichst **Open-Source-Komponenten** verwendet werden
- die Aufgaben dürfen anspruchsvoll sein; die Studierenden sollen sich bewusst auch in unbekannte Domänen einarbeiten

---

## 3. Ursprüngliche Themenüberlegungen

Zu Beginn wurden mehrere mögliche Projektdomänen betrachtet.

### 3.1 Agentisches ERP-System

Eine Idee war ein ERP-System, in dem Agenten operative oder dispositive Aufgaben übernehmen, beispielsweise:

- Aufträge bearbeiten,
- Bestände prüfen,
- Lieferungen disponieren,
- Angebote vorbereiten,
- Ausnahmen erkennen,
- Entscheidungen eskalieren,
- oder Benutzer proaktiv unterstützen.

Diese Domäne eignet sich gut, weil sie ausreichend komplex ist und verschiedene Rollen, Datenquellen und Geschäftsprozesse beinhaltet.

### 3.2 Agentische Unternehmensberatung

Eine weitere Idee war eine agentische Unternehmensberatung, beispielsweise mit Agenten für:

- Recherche,
- Datenanalyse,
- Marktanalyse,
- Strategie,
- Präsentation,
- Qualitätsprüfung,
- Projektmanagement.

Die fehlenden fachlichen Vorkenntnisse der Studierenden wurden zunächst als mögliches Problem betrachtet. Gleichzeitig wurde festgehalten, dass genau die **Einarbeitung in unbekannte Domänen** eine relevante Kompetenz für Informatikerinnen und Informatiker darstellt.

### 3.3 Amateurfunk / Funktechnik

Aufgrund des fachlichen Umfelds wurde auch über ein Projekt aus dem Bereich Amateurfunk nachgedacht. Denkbar wären beispielsweise Agenten für:

- Frequenz- und Bandplanung,
- Contest-Unterstützung,
- Logbuchanalyse,
- Ausbreitungsprognosen,
- Stationsautomatisierung,
- oder kooperative Funknetze.

### 3.4 Alternative Themen

Zwischendurch wurden allgemeinere Agentic-AI-Projektthemen diskutiert. Diese erschienen teilweise zu bekannt oder „abgegriffen“. Daraus ergab sich ein wichtiger Grundsatz:

> Die Projektdomäne darf anspruchsvoll und zunächst fremd sein. Die Studierenden sollen lernen, sich eine neue Fachdomäne strukturiert zu erschließen.

---

## 4. Zentrale konzeptionelle Weiterentwicklung: Mixed Teams

Die wesentliche Weiterentwicklung bestand darin, das Projekt **nicht primär über verschiedene Projektthemen**, sondern über die Organisation der Zusammenarbeit zu definieren.

Die Studierenden sollen in **Teams aus vier Personen** arbeiten und jeweils eine kleine Softwarefirma bilden.

Diese Softwarefirma erhält Aufträge von einem Kunden – in diesem Fall vom Lehrenden.

Jedes Team muss ein Projekt mit vorgegebenen Randbedingungen realisieren.

Die entscheidende Besonderheit:

> Für das Projekt werden mehr notwendige Rollen definiert, als menschliche Teammitglieder vorhanden sind.

Dadurch werden die Teams gezwungen, einen Teil der Rollen durch **KI-Agenten** zu besetzen.

Agenten sind damit nicht nur Bestandteil des entwickelten Produkts, sondern **Mitglieder des Entwicklungsteams selbst**.

---

## 5. Grundmodell der studentischen „Softwarefirmen“

Ein Team besteht beispielsweise aus:

- 4 menschlichen Studierenden
- mehreren KI-Agenten

Gemeinsam bilden sie eine virtuelle Softwarefirma.

Mögliche Rollen sind beispielsweise:

### Menschliche oder agentische Rollen

- Product Owner / Requirements Engineer
- Software Architect
- Backend Developer
- Frontend Developer
- Data Engineer
- AI / Agent Engineer
- QA Engineer / Tester
- DevOps Engineer
- Security Engineer
- Technical Writer
- Project Manager
- Business Analyst
- Code Reviewer
- Scrum Master / Team Facilitator

Da nicht alle Rollen menschlich besetzt werden können, müssen die Studierenden entscheiden:

- Welche Rolle sollte ein Mensch übernehmen?
- Welche Rolle kann ein Agent übernehmen?
- Welche Rolle benötigt Human-in-the-Loop?
- Welche Entscheidungen darf ein Agent autonom treffen?
- Welche Ergebnisse müssen kontrolliert werden?
- Wie kommunizieren menschliche und agentische Rollen miteinander?

Damit entsteht ein **praktisches Experiment zur Arbeitsteilung zwischen Menschen und KI**.

---

## 6. Der Lehrende als Kunde

Der Lehrende übernimmt primär die Rolle des **Kunden bzw. Auftraggebers**.

Die Teams erhalten beispielsweise:

- eine Projektbeschreibung,
- fachliche Anforderungen,
- nichtfunktionale Anforderungen,
- technische Vorgaben,
- Abnahmekriterien,
- neue Änderungswünsche,
- Change Requests,
- zusätzliche Daten,
- unerwartete Ereignisse,
- oder Fehlerberichte.

Die Kommunikation kann bewusst wie in einem realen Kundenprojekt organisiert werden.

Dadurch müssen die Teams nicht nur Software entwickeln, sondern auch:

- Anforderungen interpretieren,
- Rückfragen formulieren,
- Prioritäten setzen,
- Änderungen bewerten,
- Risiken kommunizieren,
- Entscheidungen dokumentieren,
- und Releases liefern.

---

## 7. Open-Source-ERP als gemeinsame Unternehmensumgebung

Als besonders geeignete Erweiterung wurde die Integration eines **Open-Source-ERP-Systems** diskutiert.

Das ERP kann zwei unterschiedliche Funktionen übernehmen.

### 7.1 ERP als Entwicklungsgegenstand

Die Teams könnten Erweiterungen oder agentische Funktionen für ein ERP entwickeln.

### 7.2 ERP als Betriebssystem der studentischen Softwarefirma

Didaktisch interessanter ist möglicherweise, das ERP als organisatorische Infrastruktur der virtuellen Firma zu verwenden.

Darin könnten beispielsweise verwaltet werden:

- Kunden
- Projekte
- Aufgaben
- Tickets
- Arbeitszeiten
- Projektbudgets
- Angebote
- Aufträge
- Rechnungen
- Ressourcen
- Dokumente
- Releases

Dadurch wird das Softwareprojekt stärker als **realer Unternehmensprozess** erlebt.

### Potenzielle Open-Source-Systeme

Als Kandidaten kommen grundsätzlich Systeme wie folgende infrage:

- **ERPNext**
- **Odoo Community**
- ggf. weitere schlanke Open-Source-ERP- oder Projektmanagementsysteme

Für das Lehrprojekt erscheint ein System sinnvoll, das:

- Docker-basiert bereitgestellt werden kann,
- eine API besitzt,
- eine überschaubare Installation ermöglicht,
- Projekte, Tasks und einfache Geschäftsprozesse unterstützt,
- und sich durch Agenten automatisieren lässt.

ERPNext erscheint dafür grundsätzlich besonders interessant.

---

## 8. Agenten können auf zwei Ebenen eingesetzt werden

Ein wichtiges Ergebnis der Diskussion ist die Trennung zweier Agentenebenen.

### Ebene A – Agenten im Entwicklungsteam

Beispiele:

- Coding Agent
- Test Agent
- Documentation Agent
- Requirements Agent
- Project-Management Agent
- Code-Review Agent
- Research Agent

Diese Agenten unterstützen die Entwicklung des Produkts.

### Ebene B – Agenten im entwickelten Produkt

Beispiele:

- Einkaufsagent
- Logistikagent
- Beratungsagent
- Planungssystem
- Kundenservice-Agent
- Monitoring-Agent
- Workflow-Agent

Dadurch können Studierende gleichzeitig zwei Perspektiven kennenlernen:

1. **Agentic AI als Werkzeug der Softwareentwicklung**
2. **Agentic AI als Architekturprinzip eines Softwaresystems**

---

## 9. Möglicher Ablauf über 12 Projekttage

Die Diskussionen führten zu einem projektorientierten Ablauf, bei dem jeder Montag einen klaren Meilenstein besitzt.

## Termin 1 – Company Foundation & Agent Onboarding

Ziele:

- Teams bilden
- virtuelle Softwarefirma gründen
- Rollen definieren
- Projektauftrag erhalten
- erste Agenten auswählen bzw. konfigurieren
- gemeinsame Arbeitsumgebung aufsetzen

Ergebnisse:

- Team Charter
- Rollenmatrix Mensch / Agent
- Repository
- Projektstruktur
- erste Agenten
- initiales Backlog

---

## Termin 2 – Requirements & Domain Discovery

Ziele:

- Kundendomäne analysieren
- Anforderungen strukturieren
- offene Fragen identifizieren
- erste Architekturidee entwickeln

Besonders wichtig:

Die Studierenden sollen Agenten gezielt zur **Domänenerschließung** einsetzen.

Ergebnisse:

- Requirements-Dokument
- Domain Model
- User Stories
- Risiken und offene Fragen
- Architektur-Skizze

---

## Termin 3 – Architecture & Agent Organization

Ziele:

- Systemarchitektur festlegen
- Agentenrollen im Produkt definieren
- Agentenrollen im Entwicklungsteam prüfen
- Kommunikationswege definieren

Ergebnisse:

- Architekturentscheidung
- Agentenübersicht
- Tool- und Datenzugriffe
- Human-in-the-Loop-Konzept

---

## Termin 4 – MVP Sprint I

Ziele:

- erster funktionsfähiger End-to-End-Workflow
- möglichst früh ein lauffähiges System erzeugen

Ergebnisse:

- MVP
- automatisierte Tests
- Demo

---

## Termin 5 – MVP Sprint II

Ziele:

- Funktionsumfang erweitern
- Agenten stärker integrieren
- erste Qualitätsmetriken einführen

Mögliche Metriken:

- Erfolgsquote
- Bearbeitungszeit
- Anzahl menschlicher Eingriffe
- Fehlentscheidungen
- Agentenkosten bzw. Rechenaufwand
- Rework

---

## Termin 6 – Change Request / Customer Event

Der Kunde verändert Anforderungen.

Beispiele:

- neue Schnittstelle
- zusätzliche Nutzerrolle
- geänderte Prioritäten
- Datenschutzanforderung
- zusätzliche Datenquelle

Lernziel:

**Wie robust ist ein Mixed Team gegenüber Veränderungen?**

---

## Termin 7 – Failure Day / Agent Incident

Gezielt werden Probleme provoziert.

Beispiele:

- Agent produziert falschen Code
- Testagent übersieht Fehler
- Requirements Agent interpretiert eine Anforderung falsch
- Agent überschreibt Informationen
- widersprüchliche Agentenantworten
- Tool oder Datenquelle fällt aus

Lernziel:

- Fehler erkennen
- Verantwortlichkeit klären
- Agenten überwachen
- Recovery-Prozesse entwickeln

---

## Termin 8 – Optimization Sprint

Ziel:

Die Teams optimieren nicht primär das Produkt, sondern ihre **Mensch-Agent-Zusammenarbeit**.

Fragestellungen:

- Welche Agenten liefern tatsächlich Mehrwert?
- Wo erzeugen Agenten zusätzlichen Aufwand?
- Welche Aufgaben sollten wieder Menschen übernehmen?
- Welche Aufgaben können stärker automatisiert werden?
- Welche Review-Schritte sind notwendig?

---

## Termin 9 – Autonomous Company Challenge

Die Teams erhalten einen größeren Arbeitsauftrag mit deutlich weniger Eingriffen des Lehrenden.

Ziel:

Die studentische Softwarefirma soll möglichst autonom funktionieren.

Messbar wäre beispielsweise:

- Anzahl notwendiger Rückfragen
- Anzahl manueller Eingriffe
- Bearbeitungsdauer
- Qualität des Ergebnisses
- Qualität der Dokumentation

---

## Termin 10 – Red Team / Cross-Team Review

Teams überprüfen gegenseitig ihre Lösungen.

Mögliche Aufgaben:

- Code Review
- Architekturreview
- Agent Security Review
- Prompt Injection Tests
- Fehlerprovokation
- Usability Review

Damit entsteht ein zusätzlicher Wettbewerbs- und Lernfaktor.

---

## Termin 11 – Release Candidate

Ziele:

- Produkt stabilisieren
- Dokumentation abschließen
- Demo vorbereiten
- Architektur und Agentenorganisation dokumentieren
- Lessons Learned vorbereiten

---

## Termin 12 – Demo Day & Retrospective

Abschluss als Kombination aus:

- Kundendemonstration
- Produktabnahme
- Vorstellung der Mixed-Team-Architektur
- Reflexion der Mensch-Agent-Zusammenarbeit

Wichtig ist dabei, nicht nur das entwickelte Produkt zu präsentieren.

Mindestens ebenso wichtig ist die Frage:

> Wie hat sich die Arbeitsorganisation durch Agenten verändert?

---

## 10. Gamification

Eine Gamification wurde als sinnvoll betrachtet, sollte aber nicht zu zusätzlichem Betreuungsaufwand führen.

Daher bietet sich ein leichtgewichtiges Unternehmens- bzw. Wettbewerbsspiel an.

### Mögliche Spielmechaniken

Teams erhalten eine virtuelle Firmenidentität und können Punkte oder Kennzahlen sammeln.

Beispiele:

- Kundenzufriedenheit
- Delivery Reliability
- Softwarequalität
- Automatisierungsgrad
- Agent Efficiency
- Resilience
- Dokumentationsqualität
- technische Schulden
- Anzahl erfolgreicher Releases

### Zusätzliche Events

Der Kunde kann „Event Cards“ auslösen:

- wichtiger Entwickler fällt aus
- neue Datenschutzanforderung
- Kunde verlangt kurzfristige Änderung
- Agent produziert unzuverlässige Ergebnisse
- Budget wird reduziert
- neues Legacy-System muss integriert werden
- Sicherheitsproblem wird entdeckt
- API wird geändert

Dadurch entstehen kontrollierte Störungen, ohne dass der Lehrende permanent eingreifen muss.

---

## 11. Keine klassische Benotung

Da das Wahlpflichtprojekt nicht benotet wird, kann stärker experimentiert werden.

Das ist für dieses Lehrformat ein Vorteil.

Statt einer klassischen Bewertung kann mit:

- Badges,
- Achievements,
- Meilensteinen,
- Demo-Erfolgen,
- Teammetriken,
- oder einem abschließenden „Company Award“

gearbeitet werden.

Mögliche Auszeichnungen:

- Best Mixed Team
- Best Agent Architecture
- Most Resilient Company
- Best Customer Solution
- Best Human-Agent Collaboration
- Most Useful Failure
- Best Autonomous Workflow

Damit kann auch ein bewusst gescheitertes Experiment einen hohen Lernwert besitzen.

---

## 12. Selbstorganisation bei Abwesenheit des Lehrenden

Da eine Anwesenheit des Lehrenden nicht an jedem Termin garantiert werden kann, muss das Format **low-touch** funktionieren.

Dafür sind wichtig:

### Standardisierte Projektstruktur

Jedes Team arbeitet mit denselben Basiselementen:

- Git Repository
- Issue Board
- Backlog
- Definition of Done
- Architecture Decision Records
- Agent Registry
- Weekly Status
- Decision Log

### Klare Tagesmissionen

Für jeden Montag existiert ein vorbereitetes Mission Sheet mit:

- Ziel
- Inputs
- Deliverables
- optionalen Challenges
- Abnahmekriterien

### Agenten als organisatorische Unterstützung

Beispielsweise kann jedes Team einen:

- Project Manager Agent,
- Scrum Agent,
- Documentation Agent,
- oder Quality Agent

verwenden.

Damit wird die organisatorische Selbstständigkeit selbst Teil des Experiments.

---

## 13. Beobachtung und Evaluation der Mixed Teams

Obwohl keine Benotung vorgesehen ist, sollte die Zusammenarbeit systematisch beobachtet werden.

Interessante Kennzahlen sind beispielsweise:

### Leistungskennzahlen

- Anzahl abgeschlossener Tasks
- Durchlaufzeit
- Anzahl Bugs
- Testabdeckung
- Anzahl Releases

### Agentenkennzahlen

- Anteil agentisch bearbeiteter Tasks
- Anteil akzeptierter Agentenergebnisse
- Anzahl notwendiger Korrekturen
- Anzahl Human Interventions
- Agent Failure Rate

### Teamkennzahlen

- Delegationsmuster
- Wartezeiten
- Kommunikationsaufwand
- Rework
- Aufgabenverschiebungen zwischen Mensch und Agent

### Reflexionsfragen

- Welche Aufgaben konnten Agenten besser erledigen als erwartet?
- Welche Aufgaben funktionierten schlechter als erwartet?
- Wann war eine menschliche Kontrolle unverzichtbar?
- Welche Rollen ließen sich vollständig automatisieren?
- Welche Rollen sollten nicht automatisiert werden?
- Hat die Integration von Agenten das Team tatsächlich schneller gemacht?
- Wo entstanden neue Bottlenecks?
- Wie veränderte sich Vertrauen in Agenten während des Projekts?

---

## 14. Didaktischer Kern des Projekts

Das Projekt sollte bewusst **nicht** als Wettbewerb darum verstanden werden, möglichst viele Agenten einzusetzen.

Das eigentliche Lernziel lautet:

> Die Studierenden sollen herausfinden, für welche Aufgaben Menschen, Agenten oder hybride Arbeitsformen jeweils am besten geeignet sind.

Ein Team, das am Ende einen zunächst eingesetzten Agenten wieder abschafft, kann deshalb genauso erfolgreich sein wie ein Team mit hohem Automatisierungsgrad.

Entscheidend ist die begründete Gestaltung des Gesamtsystems.

---

## 15. Mögliche technische Architektur

Eine konkrete technische Plattform wurde noch nicht endgültig festgelegt.

Ein sinnvolles Basissetup könnte jedoch aus folgenden Komponenten bestehen:

### Entwicklungsumgebung

- GitHub / GitHub Classroom
- Docker / Docker Compose
- Python
- REST APIs
- lokale oder universitäre LLM-Infrastruktur

### Agenten

Je nach didaktischem Ziel beispielsweise:

- LangGraph
- eigene Python-Agenten
- MCP-basierte Toolintegration
- lokale LLMs
- ggf. n8n für ausgewählte Workflows

### Unternehmenssoftware

- ERPNext oder vergleichbares Open-Source-ERP

### Observability

- strukturierte Logs
- Agent Action Logs
- Tool Calls
- Task History
- einfache Metriken

Die konkrete Agentenplattform sollte eher einfach bleiben. Das zentrale Lernziel ist nicht das Erlernen eines bestimmten Frameworks, sondern die **Gestaltung und Evaluation agentischer Arbeitssysteme**.

---

## 16. Empfohlenes gemeinsames Projektszenario

Aus den bisherigen Überlegungen ergibt sich als besonders schlüssiges Gesamtformat:

> Mehrere studentische Softwarefirmen konkurrieren bzw. arbeiten parallel an Kundenprojekten. Jede Firma besteht aus vier menschlichen Mitarbeitenden und mehreren selbst gewählten oder vorgeschriebenen Agenten. Die Teams nutzen eine gemeinsame technische Infrastruktur und müssen über zwölf Wochen ein reales Softwareprodukt entwickeln. Der Kunde erzeugt während des Projekts neue Anforderungen und Störungen. Am Ende werden sowohl Produkt als auch Organisationsmodell des Mixed Teams reflektiert.

Dieses Szenario verbindet:

- Software Engineering
- Agentic AI
- Multi-Agent Systems
- Human-AI Collaboration
- Projektmanagement
- Organisationsdesign
- Requirements Engineering
- DevOps
- Qualitätssicherung
- und fachliche Domänenerschließung.

---

## 17. Wichtigste bisherige Entscheidungen

Die bisherige Diskussion lässt sich auf folgende Entscheidungen verdichten:

1. **Mixed Teams stehen im Mittelpunkt**, nicht nur die Implementierung einzelner Agenten.
2. Die Studierenden arbeiten in **Teams von vier Personen**.
3. Jedes Team bildet eine **virtuelle Softwarefirma**.
4. Es existieren **mehr Projektrollen als menschliche Teammitglieder**.
5. Deshalb müssen bestimmte Rollen durch **Agenten** übernommen werden.
6. Der Lehrende agiert primär als **Kunde / Auftraggeber**.
7. Die Projekte dürfen fachlich anspruchsvoll und zunächst unbekannt sein.
8. Ein **Open-Source-ERP** kann als gemeinsame organisatorische Infrastruktur integriert werden.
9. Das Projekt läuft über **12 vollständige Projekttage à etwa sechs Stunden**.
10. Jeder Projekttag sollte über eine klare **Mission und Deliverables** strukturiert werden.
11. Gamification ist sinnvoll, sollte aber **leichtgewichtig und weitgehend selbstlaufend** sein.
12. Das Projekt muss auch funktionieren, wenn der Lehrende an einzelnen Terminen **nicht anwesend** ist.
13. Die Bewertung erfolgt nicht klassisch über Noten, sondern primär über **Lernerfolg, Meilensteine, Reflexion und optional spielerische Kennzahlen**.
14. Der Erfolg eines Agenten wird nicht an seiner bloßen Existenz gemessen, sondern an seinem **nachweisbaren Beitrag zum Team**.
15. Der Abschluss sollte sowohl das **Softwareprodukt** als auch die **Erfahrungen mit der Mixed-Team-Organisation** sichtbar machen.

---

## 18. Noch offene Entscheidungen

Vor Beginn der Lehrveranstaltung sollten insbesondere folgende Punkte noch festgelegt werden:

### Projektdomäne

- ein gemeinsamer Auftrag für alle Teams
- unterschiedliche Kundenprojekte
- oder 2–3 verschiedene Domänen

### ERP

- ERPNext
- Odoo Community
- oder Verzicht auf ein vollständiges ERP zugunsten einer schlankeren Plattform

### Agentenplattform

- ein verbindliches Framework
- mehrere zugelassene Frameworks
- oder freie Wahl mit einer Minimal-API

### LLM-Infrastruktur

- lokale Modelle auf Studierendenrechnern
- zentrale universitäre Infrastruktur
- Ollama
- vLLM / Kubernetes
- Kombination daraus

### Wettbewerb

- Punkte und Ranking
- nur Badges
- oder stärker kooperatives Modell

### Kundenaufträge

Es werden ausreichend konkrete Projektbeschreibungen und vorbereitete Change Requests benötigt.

### Evaluation

Zu entscheiden ist, welche Kennzahlen von allen Teams verbindlich erfasst werden sollen.

---

## 19. Sinnvolle nächste Vorbereitungsschritte

Als nächste konkrete Arbeitspakete bieten sich an:

1. verbindliches Gesamtszenario festlegen
2. technische Referenzarchitektur definieren
3. Open-Source-ERP auswählen und als Docker-Setup vorbereiten
4. Vorlage für die virtuelle Softwarefirma erstellen
5. Rollen-Katalog erstellen
6. Agent Profile / Agent Cards vorbereiten
7. Projektbriefing für den ersten Kundenauftrag schreiben
8. zwölf Mission Sheets erstellen
9. Event Cards / Change Requests vorbereiten
10. gemeinsames GitHub-Classroom-Template erstellen
11. Logging- und Evaluationsschema definieren
12. Demo-Day- und Retrospektivenformat vorbereiten

---

## 20. Gesamtfazit

Aus einer zunächst klassischen Idee für ein Agentic-AI-Projekt hat sich ein deutlich stärkeres Lehrkonzept entwickelt.

Der eigentliche Gegenstand der Lehrveranstaltung ist nicht mehr lediglich:

> „Wie programmiert man einen KI-Agenten?“

sondern:

> **„Wie entwirft, betreibt und verbessert man ein Arbeitssystem, in dem Menschen und autonome Agenten gemeinsam komplexe Aufgaben lösen?“**

Damit verbindet das Wahlpflichtprojekt technische, organisatorische und soziale Aspekte von Agentic AI und bietet den Studierenden die Möglichkeit, Mixed Teams nicht nur theoretisch zu diskutieren, sondern über ein vollständiges Semester praktisch zu erleben.
