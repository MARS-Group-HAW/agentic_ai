# WP Agentic AI — Zusammenfassung von Diskussion und Ergebnissen

**Wahlpflichtprojekt „Agentic AI"** · Bachelor Informatik · HAW Hamburg · Prof. Dr. Thomas Clemen
Stand: 27. August 2026

Dieses Dokument fasst den Stand des Projekts zusammen: die Leitideen und Designentscheidungen aus der bisherigen Konzeptdiskussion sowie die drei bislang vorliegenden Ergebnisdokumente (Praktikums-Aufgabenstellung, Hausarbeits-Aufgabenstellung und Bewertungsraster).

---

## 1  Ausgangslage

Das Modul ist ein Wahlpflichtprojekt für das Wintersemester 2026/27 mit rund 17 Teilnehmenden (teils international), 12 Terminen und Englisch als Arbeitssprache. Ziel ist, dass Studierende nicht nur agentische Systeme bauen, sondern deren Wert **und** Grenzen — insbesondere im Zusammenspiel von Mensch und KI — selbst erfahren und anschließend fachlich reflektieren. Das Modul besteht aus zwei aufeinander bezogenen Prüfungsteilen: dem Gruppen-Praktikum als Bau- und Experimentierphase und der individuellen Hausarbeit als analytischer Reflexion.

---

## 2  Diskussion und Designentscheidungen

### 2.1  Leitidee und roter Faden
Die tragende Idee ist, ein reales agentisches System entlang der sechs Vorlesungskapitel zu entwickeln. Die Technik ist damit nicht Selbstzweck, sondern trägt den Lehrstoff: Jede Praktikumsphase liefert später den konkreten Analysegegenstand für ein Kapitel der Hausarbeit.

### 2.2  Zwei-Modus-Experiment (A/B) als gemeinsame Klammer
Als verbindende Struktur über alle Teams hinweg wurde ein A/B-Experiment festgelegt. Jedes Team baut dieselbe Aufgabe in zwei Modi:

- **Modus A – Full-Agentic:** Agenten handeln allein, der Mensch beobachtet nur.
- **Modus B – Mixed Team:** Eine menschliche Rolle ist Pflicht-Teammitglied mit Freigabe-, Korrektur- und Eskalationspunkten.

Gemessen wird an Durchsatz/Zeit, Qualität/Fehlerrate, Kosten (Tokens/Calls), Interventionen sowie Vertrauen/Übersteuerung. Dieses Experiment liefert die empirische Substanz für die Kapitel 4, 5 und 6 und dient als Grundlage für das Vertiefungskapitel (K7).

### 2.3  Vier wählbare Tracks
Als Projektinhalte stehen vier Tracks zur Wahl, die jeweils einen charakteristischen Mensch-KI-Konflikt in den Vordergrund rücken:

1. **Agentische Redaktion** — Recherche-/Autor-/Faktencheck-/Redakteur-Agenten mit menschlicher Chefredaktion. Kernkonflikt: Qualität vs. Tempo. Fokus auf RAG, Tool Use, Orchestrator/Worker und Safety (Fehlinformation, Prompt Injection).
2. **Ops-/Incident-Copilot** — Agenten triagieren und schlagen Remediation vor; ausführende Aktionen nur mit menschlicher Freigabe. Kernkonflikt: Trust Calibration. Technisch und sicherheitlich am anspruchsvollsten.
3. **Multi-Agent-Spiel/-Simulation** — Agenten und Menschen kooperieren oder konkurrieren (Verhandlung, Ressourcen, Social Deduction). Nah an MARS/MARL, sprachlich neutral, hohe Motivation.
4. **SW-Engineering-Agententeam** — Planner/Coder/Tester/Reviewer mit menschlichem Tech Lead. Starker Testing-Bezug; das Mixed Team wirkt am eigenen Entwicklungsprozess.

### 2.4  Technische Basis und Ablauf
Vereinbart wurden als gemeinsame Grundlage Python, ein geteiltes Repo-Template, ein zu begründendes Agenten-Framework, MCP für Tools sowie Tracing/Observability von Anfang an. Ein Rollen- und Hand-off-Protokoll macht die Mensch↔Agent-Schnittstelle selbst zur Designaufgabe. Der 12-Termine-Ablaufplan sieht vor, dass bis Termin 7 beide Modi lauffähig sind und ab Termin 10 gemessen wird. Abgaben des Praktikums: Repo, Demo (A + B), Experiment-Report (2–3 Seiten) und Abschlusspräsentation.

### 2.5  Offene Punkte
Aus der Diskussion sind einige Entscheidungen bewusst noch offen geblieben:

- **Betriebsmodell:** Bekommt jedes Team einen eigenen Track, oder bearbeiten alle Teams denselben Track (maximale Vergleichbarkeit)? Der Professor hatte hier „keine Präferenz" geäußert; im Dokument bleibt es offen.
- **Englische Fassung** der Aufgabenstellung für die Studierenden (optional).
- **Konkrete Framework-Empfehlung** und ein fertiges Repo-Template (optional).

---

## 3  Ergebnisse: die drei erstellten Dokumente

### 3.1  Praktikums-Aufgabenstellung (Konzept-Entwurf)
Der Word-Entwurf `WP_AgenticAI_Praktikum_Aufgabenstellung.docx` wurde bereits geliefert; das begleitende Konzeptdokument hält Leitidee, A/B-Experiment, die vier Tracks, die technische Basis, den 12-Termine-Ablauf, die Abgaben, eine Mapping-Tabelle (Praktikumsphase → Hausarbeit-Kapitel) und die Startliteratur fest (ReAct, Reflexion, Toolformer, Generative Agents, Voyager).

### 3.2  Hausarbeits-Aufgabenstellung
Die Hausarbeit ist eine **individuelle** schriftliche Prüfungsleistung (8–12 Seiten, PDF + GitHub-Link über Moodle) und vertieft die Gruppenarbeit analytisch. Kern ist die Anwendung der sechs Vorlesungskapitel auf das eigene Projekt — nicht als erneute Systembeschreibung (Systemüberblick auf ca. 0,5 Seiten begrenzt), sondern als strukturierte Reflexion.

Die vorgegebene Kapitelstruktur mit ihren Leitfragen:

| Kapitel | Umfang | Leitfrage |
| --- | --- | --- |
| 0. Systemüberblick | ~0,5 S. | Was haben wir gebaut? |
| 1. Agent-Analyse (Kap. 01) | ~1 S. | Was für ein Agent ist das? (PEAS, Taxonomie) |
| 2. Kognitive Architektur (Kap. 02) | ~1 S. | Wie nimmt er wahr, erinnert sich, plant er? (4 Schichten) |
| 3. LLM, RAG & Tool Use (Kap. 03) | ~1 S. | Wie ist der Agent sprach- und handlungsfähig? |
| 4. Multi-Agent-Entscheidung (Kap. 04) | ~1 S. | Single Agent oder MAS — und warum? |
| 5. Engineering & Testing (Kap. 05) | ~1 S. | Wie ist es gebaut und getestet? |
| 6. Safety-Analyse (Kap. 06) | ~1 S. | Was kann schiefgehen — und wie verhindert? |

Ein Kapitel wird als **Vertiefungskapitel** gewählt (ca. 3 statt 1 Seite) und muss eigenständige kritische Analyse, mindestens zwei literaturgestützte Verbesserungsvorschläge (je mit Nutzen und Trade-off) sowie eine systematische Trade-off-Diskussion enthalten. Zur inhaltlichen Vielfalt innerhalb einer Gruppe darf dasselbe Vertiefungskapitel nur von einer Person gewählt werden (*first come, first serve*, Deklaration bis 1. Juli 2026, Bestätigung durch den Professor). Formal gefordert sind u. a. 11 pt / 1,5-facher Zeilenabstand, mindestens 6 Quellen (davon ≥ 4 wissenschaftliche Paper) und eine Deklaration der KI-Nutzung. Das Dokument schließt mit einer Liste häufiger Fehler und besserer Alternativen.

### 3.3  Bewertungsraster
Das Raster ist auf eine schnelle Korrektur (15–20 Minuten pro Arbeit) ausgelegt. **Sieben Kriterien à 10 Punkte = 70 Punkte:** sechs Kapitelkriterien (K1–K6) plus K7 für Tiefe und Originalität des Vertiefungskapitels. Jedes Kriterium wird auf einer Skala 0 / 5 / 8 / 10 markiert, mit ausformulierten Niveaubeschreibungen. Ein Notenschlüssel übersetzt die Punktsumme in Noten (63–70 → 1,0–1,3; unter 35 → 5,0) und Kommentarfelder erfassen Stärken, Schwächen, Anmerkungen zum Vertiefungskapitel sowie zur KI-Deklaration.

---

## 4  Roter Faden zwischen den Dokumenten

Die drei Dokumente greifen konsistent ineinander: Das Praktikum erzeugt über das A/B-Experiment und die vier Tracks die konkreten Beobachtungen und Daten; die Hausarbeit strukturiert deren Reflexion strikt entlang der sechs Vorlesungskapitel; das Bewertungsraster spiegelt dieselben sechs Kapitel als K1–K6 und ergänzt K7 als individualisierendes Element. So ist von der Bauaufgabe über die Analyse bis zur Bewertung durchgängig derselbe rote Faden gespannt.

---

## 5  Nächste mögliche Schritte

- Betriebsmodell (ein Track je Team vs. gemeinsamer Track) final festlegen.
- Bei Bedarf englische Fassung der Praktikums- und Hausarbeits-Aufgabenstellung erstellen.
- Repo-Template und eine konkrete Framework-Empfehlung ausarbeiten.
- Termine im Ablaufplan mit dem tatsächlichen Semesterkalender WS 2026/27 abgleichen.

> **Hinweis:** In den Aufgaben-Dokumenten ist als Abgabetermin der Hausarbeit der **16. August 2026** und als Semesterkennung teils **SS 2026** angegeben, während das Praktikum für **WS 2026/27** konzipiert ist. Diese Datums-/Semesterangaben sollten vor der Veröffentlichung an die Studierenden noch vereinheitlicht werden.
