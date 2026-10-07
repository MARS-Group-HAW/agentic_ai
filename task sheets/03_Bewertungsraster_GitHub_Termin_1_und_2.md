# Bewertungsraster für GitHub-Snapshots – Termin 1 und Termin 2

## 1. Zweck

Nach Termin 1 und Termin 2 wird der GitHub-Stand jeder Firma automatisiert evaluiert.

Das Projekt ist unbenotet. Der Score dient als **Engineering Health Indicator** und als konkretes Feedback für den nächsten Projekttag.

Maximal:

**100 Punkte pro Termin**

---

# 2. Nur Team-Delta bewerten

Alle Firmen starten mit demselben Starter Repository.

Der Evaluator muss strikt zwischen Baseline und studentischer Leistung unterscheiden.

## Niemals als Teamleistung werten

```text
examples/**
tests/starter/**
pytest.ini
```

Ebenfalls nicht automatisch werten:

- vorhandener FastAPI-Health-Endpunkt,
- vorhandene PostgreSQL-/pgvector-Verkabelung,
- unveränderte GitHub-Actions-CI,
- unverändertes Docker Compose,
- unveränderte Trace-Hilfsfunktionen,
- unveränderte Starter-Templates.

Templates zählen nur nach sinnvoller Team-Anpassung.

Maßgeblich:

```text
docs/STARTER_BOUNDARY.md
STARTER_MANIFEST.json
```

Grundregel:

> **Bewerte das Delta zum Starter, nicht den Starter selbst.**

---

# 3. Evidence over claims

Bevorzugte Evidenz:

1. eigener ausführbarer Code,
2. eigene automatisierte Tests,
3. Execution Traces,
4. strukturierte Outputs / Messdaten,
5. GitHub Issues / Commit-Historie,
6. team-spezifische Konfiguration,
7. technische Dokumentation.

Wenn eine Funktion technisch überprüfbar wäre, genügt eine README-Behauptung nicht.

### Standard-Testlauf

Für lokale Ausführung und CI gilt:

```bash
python -m pytest
```

`pytest.ini` ist Bestandteil des Starters und zählt nicht als studentische Leistung. Team-eigene Tests müssen im Standard-Testlauf enthalten und ausführbar sein.

---

# 4. Termin 1 – Bewertungsraster

## A. Company & Roles – 20 Punkte

### A1. Rollenmodell vollständig – 8 Punkte

Prüfe `organization/roles.yaml`.

- **8**: alle 12 Rollen enthalten `current_actor_type`, `target_actor_type` und `accountable_human`
- **5**: 9–11 Rollen vollständig
- **2**: 6–8 Rollen vollständig
- **0**: weniger als 6

### A2. Human-Agent-Zielbild – 6 Punkte

Bewerte:

- plausible current/target-Zuordnung,
- erkennbare Planung für Mixed-Team-Arbeit,
- keine Schein-Agenten als `operational`.

Nicht die Anzahl geplanter Agenten bewerten.

### A3. Entscheidungs- und Eskalationsregeln – 3 Punkte

Prüfe `organization/company.md`.

### A4. Drei Pflichtentscheidungen begründet – 3 Punkte

Gesucht:

- erste agentisch unterstützte Rolle,
- bewusst menschliche Rolle,
- Human Approval Gate.

---

## B. Technical Platform – 15 Punkte

### B1. Team Setup nachvollziehbar – 4 Punkte

README enthält team-spezifische Angaben zu:

- Entwicklungsumgebung,
- Ollama oder ICC,
- Setup-Abweichungen,
- bekannten Einschränkungen.

### B2. Architektur team-spezifisch angepasst – 6 Punkte

`docs/architecture.md` zeigt mindestens:

- eigenen Agenten,
- Tool,
- LLM-Pfad,
- Human Gate / Eskalation,
- Trace-/Cost-Pfad.

Unveränderte Starter-Architektur: **0 Punkte**.

### B3. Starter sinnvoll weiterverwendet – 3 Punkte

Keine unnötige parallele Ersatzinfrastruktur für bereits bereitgestellte Komponenten.

### B4. Stack-Disziplin – 2 Punkte

- **2**: Pflichtstack eingehalten oder gewünschte Abweichung per Issue begründet
- **0**: zentrale zusätzliche Technologie ohne Absprache eingeführt

---

## C. First Own Agent – 35 Punkte

### C1. Eigener ausführbarer LangGraph-Agent – 15 Punkte

Nur team-eigene Implementierung, z. B. unter `src/agents/**`.

- **15**: eigenständig und plausibel ausführbar
- **10**: weitgehend implementiert, kleinere Lücken
- **5**: Fragment / nur eingeschränkt ausführbar
- **0**: kein eigener Agent

`examples/**` zählt niemals.

### C2. Echter LLM-Aufruf über Provider-Abstraktion – 5 Punkte

- **5**: technisch nachvollziehbar
- **2**: teilweise / direkte providerspezifische Kopplung ohne Begründung
- **0**: kein echter LLM-Einsatz

### C3. Reales Tool – 5 Punkte

- **5**: Tool im nachgewiesenen Run tatsächlich verwendet
- **3**: Tool vorhanden, Nutzung nicht belegt
- **0**: reine Textgenerierung

### C4. Strukturierter Input / Output – 5 Punkte

Bevorzugt:

- Pydantic,
- TypedDict,
- JSON Schema,
- definierter LangGraph State.

### C5. Sinnvolle Fehlerbehandlung – 5 Punkte

Beispiele:

- ungültiger Input,
- Tool-Fehler,
- fehlende Datei,
- LLM-Fehler,
- definierte Terminierung.

---

## D. Testing & Evidence – 15 Punkte

### D1. Eigener sinnvoller pytest-Test – 6 Punkte

Nur Tests außerhalb `tests/starter/**`.

Volle Punkte nur, wenn die team-eigenen Tests mit `python -m pytest` ausführbar sind.

### D2. Team-eigener Execution Trace – 5 Punkte

Trace muss dem eigenen Agentenlauf zuordenbar sein.

### D3. Reproduzierbarer Agentenaufruf – 4 Punkte

Aus Repository / README ist nachvollziehbar, wie der Agent ausgeführt wird.

---

## E. Cost Measurement – 10 Punkte

Termin 1 bewertet **Messfähigkeit**, nicht Kostenoptimierung.

### E1. Human Hours – 3 Punkte

Tatsächliche Team-Arbeitszeit grob erfasst.

### E2. Agent Usage – 4 Punkte

Mindestens:

- eigener Agent,
- Modell,
- Laufzeit,
- Runs,
- Tokens, falls verfügbar.

### E3. Credits berechnet – 3 Punkte

Tatsächliche Nutzungsdaten werden mit dem Kurs-Kostenmodell in Credits übersetzt.

---

## F. Engineering Process – 5 Punkte

### F1. Sinnvolle GitHub Issues – 3 Punkte

Mindestens drei relevante Issues für tatsächlich bearbeitete Themen.

### F2. Nachvollziehbare Commit-Historie – 2 Punkte

Nicht die Anzahl der Commits bewerten.

Pull Requests sind an Termin 1 optional.

---

## Termin 1 – Gesamt

| Bereich | Punkte |
|---|---:|
| A. Company & Roles | 20 |
| B. Technical Platform | 15 |
| C. First Own Agent | 35 |
| D. Testing & Evidence | 15 |
| E. Cost Measurement | 10 |
| F. Engineering Process | 5 |
| **Gesamt** | **100** |

---

# 5. Interpretation Termin 1

| Score | Bedeutung |
|---:|---|
| **85–100** | deutlich über Tagesziel |
| **70–84** | Tagesziel erreicht |
| **55–69** | teilweise erreicht |
| **40–54** | wesentliche Lücken |
| **<40** | technische Basis noch nicht arbeitsfähig |

**70 Punkte sind ein vollständig zufriedenstellender Projekttag.**

Der Score ist ausdrücklich keine Note.

---

# 6. Harte Caps Termin 1

### Kein eigener ausführbarer Agent

**Gesamtscore maximal 50/100**

### Kein eigener Test

Wenn ausschließlich `tests/starter/**` vorhanden ist:

**Gesamtscore maximal 75/100**

### Team-eigene Tests nicht mit Standard-Testlauf ausführbar

Wenn team-eigene Tests vorhanden sind, aber `python -m pytest` nicht erfolgreich durchläuft:

**Testing & Evidence maximal 8/15**

### Kein team-eigener Execution Trace

**Gesamtscore maximal 75/100**

### Keine tatsächlichen Nutzungsdaten

Wenn nur das unveränderte Cost-Template existiert:

**Gesamtscore maximal 75/100**

### Nur Starter + Dokumentation

Wenn der technische Stand weitgehend dem Starter entspricht und hauptsächlich Markdown geändert wurde:

**Gesamtscore maximal 40/100**

---

# 7. Termin 2 – Bewertungsraster

Termin 2 bewertet den aktuellen Stand nach zwei Terminen.

## A. Operational Mixed Team – 20 Punkte

### A1. Mindestanzahl operativer agentischer/hybrider Rollen – 10 Punkte

Erforderlich:

```text
12 - Anzahl menschlicher Teammitglieder
```

- **10**: Mindestzahl erreicht und technisch belegt
- **7**: eine Rolle unter Mindestzahl
- **4**: zwei Rollen unter Mindestzahl
- **0**: deutlich darunter

Eine Rolle zählt nur bei technisch nachweisbarem Verhalten.

### A2. Accountable Humans / Human Gates konsistent – 5 Punkte

### A3. Rollenmodell entspricht tatsächlicher Implementierung – 5 Punkte

Keine `operational`-Kennzeichnung ohne Evidenz.

---

## B. Agent Platform – 25 Punkte

### B1. Mindestens drei unterscheidbare Agentenfähigkeiten – 10 Punkte

- **10**: mindestens 3
- **7**: 2
- **3**: 1
- **0**: keine

Ein Agent darf mehrere Rollen unterstützen, wenn Verhalten und Trace unterscheidbar sind.

### B2. Gemeinsames Task-/State-Modell – 5 Punkte

Mindestens zwei Agenten verwenden es tatsächlich.

### B3. Agent-to-Agent-Workflow – 7 Punkte

Technische Übergabe über LangGraph State / strukturierte Daten.

### B4. Human Gate – 3 Punkte

Expliziter Approval- oder Escalation-Punkt.

---

## C. Workflow Quality & Tests – 20 Punkte

### C1. Strukturierte Outputs – 4 Punkte

### C2. Erfolgsfall getestet – 5 Punkte

Volle Punkte nur, wenn der Test im Standard-Testlauf `python -m pytest` enthalten ist.

### C3. Fehlerfall getestet – 5 Punkte

Volle Punkte nur, wenn der Test im Standard-Testlauf `python -m pytest` enthalten ist.

### C4. Terminierung / Schleifenbegrenzung – 3 Punkte

### C5. Reproduzierbarer Workflow-Run – 3 Punkte

---

## D. Internal Dry Run – 20 Punkte

### D1. Persistente Work-Item-Funktion – 8 Punkte

Mindestens:

- anlegen,
- auflisten,
- erledigen oder löschen,
- PostgreSQL-Persistenz.

### D2. API-Tests – 4 Punkte

Team-eigene Tests, die über `python -m pytest` ausführbar sind.

### D3. Agentic Contribution Traceability – 5 Punkte

Nachvollziehbare Kette:

```text
Issue → Task → Agent/Human → Artifact → Test/Review
```

### D4. `docs/dry-run-01.md` – 3 Punkte

Kurz, konkret, auf tatsächliche Evidenz bezogen.

---

## E. Cost Engineering – 10 Punkte

### E1. Task-bezogene Agentenkosten – 4 Punkte

### E2. Human Review / Correction Effort – 3 Punkte

### E3. Konkrete Optimierungsidee aus den Messdaten – 3 Punkte

Es genügt eine begründete Hypothese für den nächsten Task.

---

## F. Engineering Discipline – 5 Punkte

### F1. Issues / Commits spiegeln den Dry Run – 3 Punkte

### F2. Architektur / Rollenmodell aktualisiert – 2 Punkte

---

## Termin 2 – Gesamt

| Bereich | Punkte |
|---|---:|
| A. Operational Mixed Team | 20 |
| B. Agent Platform | 25 |
| C. Workflow Quality & Tests | 20 |
| D. Internal Dry Run | 20 |
| E. Cost Engineering | 10 |
| F. Engineering Discipline | 5 |
| **Gesamt** | **100** |

---

# 8. Interpretation Termin 2

| Score | Bedeutung |
|---:|---|
| **85–100** | deutlich über Tagesziel |
| **70–84** | Tagesziel erreicht |
| **55–69** | teilweise erreicht |
| **40–54** | wesentliche Lücken |
| **<40** | Agentic Development Platform noch nicht arbeitsfähig |

---

# 9. Harte Caps Termin 2

### Mindestzahl operativer agentischer/hybrider Rollen deutlich verfehlt

Wenn mehr als zwei Rollen zur Mindestzahl fehlen:

**Gesamtscore maximal 60/100**

### Weniger als zwei eigene Agentenfähigkeiten

**Gesamtscore maximal 55/100**

### Kein technischer Agent-to-Agent-Workflow

**Gesamtscore maximal 65/100**

### Keine eigenen Workflow-/API-Tests

**Gesamtscore maximal 65/100**

### Team-eigene Tests nicht mit Standard-Testlauf ausführbar

Wenn die relevanten team-eigenen Tests mit `python -m pytest` nicht erfolgreich ausführbar sind:

**Workflow Quality & Tests maximal 10/20**

### Dry Run nur Mock / keine Persistenz

**Gesamtscore maximal 75/100**

---

# 10. Beide Termine: Security Critical Finding

Committed Secrets wie:

- API Keys,
- Passwörter,
- Tokens,
- private Schlüssel

werden immer als **Critical Finding** ausgewiesen.

---

# 11. Keine Punkte für unnötige Komplexität

Nicht positiv bewerten:

- mehr Agenten als nötig,
- mehr Frameworks,
- größere Modelle,
- mehr LLM Calls,
- unnötige Multi-Agent-Schichten.

Technische Einfachheit ist kein Nachteil, wenn die Lösung zuverlässig und nachvollziehbar funktioniert.

---

# 12. Ausgabeformat für die automatische Evaluation

```json
{
  "company": "NAME",
  "session": 1,
  "score": 78,
  "interpretation": "Tagesziel erreicht",
  "dimensions": {
    "company_roles": 16,
    "technical_platform": 12,
    "first_own_agent": 27,
    "testing_evidence": 11,
    "cost_measurement": 8,
    "engineering_process": 4
  },
  "evidence": [
    {
      "criterion": "C1",
      "score": 13,
      "files": [
        "src/agents/qa_agent.py"
      ],
      "reason": "..."
    }
  ],
  "strengths": [
    "..."
  ],
  "critical_findings": [
    "..."
  ],
  "missing_evidence": [
    "..."
  ],
  "top_3_actions_next_session": [
    "...",
    "...",
    "..."
  ],
  "confidence": 0.9
}
```

Für Termin 2 werden die Dimension Keys entsprechend dem Termin-2-Raster angepasst.

---

# 13. Instruktion an das Bewertungsmodell

> Vergleiche den Repository-Stand mit dem bereitgestellten Starter und bewerte ausschließlich team-eigene Änderungen und team-eigene Ausführungsevidenz.  
> `examples/**`, `tests/starter/**` und `pytest.ini` sind vollständig von der Bewertung als studentische Leistung auszuschließen.  
> Unveränderte Starter-Infrastruktur darf keine Punkte als studentische Leistung erzeugen.  
> Unterstelle keine Funktionalität aus Dokumentation. Suche bei technisch überprüfbaren Behauptungen nach Code, Tests, Traces oder strukturierten Daten.  
> Team-eigene Tests müssen im Standard-Testlauf `python -m pytest` enthalten und ausführbar sein.  
> Nenne bei jeder wesentlichen Bewertung konkrete Dateien bzw. GitHub-Artefakte als Evidenz.  
> Bewerte Einfachheit nicht negativ.  
> Bewerte zusätzliche Frameworks nicht positiv.  
> Ziehe keine Punkte für Funktionen ab, die für den jeweiligen Termin noch nicht gefordert sind.  
> Ein Score von 70–84 bedeutet, dass das Tagesziel erreicht wurde; behandle 70 Punkte nicht als schwache Leistung.  
> Weise Unsicherheit explizit aus, wenn eine Funktion aus einem statischen Repository-Snapshot nicht zuverlässig verifiziert werden kann.
