# Agent Ideas & Architectural Concepts

This document summarizes agent design patterns, synthetic instruction generation strategies, and tool-calling concepts for Nepali NLP.

---

## 1. Synthetic Instruction Generation
- Multi-sentence batching (6-sentence translation batches) for high-throughput instruction-tuning datasets.
- Schema enforcement for tool-calling agents (`singleturn_json`, `hermes_tool_calling`).
- Register compliance testing: Honorifics (हजुर/तपाईँ/तँ) and formal/colloquial shift monitoring.

---

## 2. Prosody & Poetic Meter Scanning (Chhanda)
- Devanagari prosody scanner algorithm classifying syllables into Laghu (ह्रस्व) and Guru (दीर्घ).
- Identification of classical Nepali & Sanskrit meters (*Shikharini*, *Shardulavikridita*, *Mandakranta*, *Anushtup*).

---

## 3. Domain Tools Integration
- Financial quotes (NEPSE), weather/AQI, crop advisory, and house valuation tool-calling specs for Nepali LLM agents.
