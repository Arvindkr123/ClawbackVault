# System Architecture: Relationship Signal Engine

## 1. Project Overview
The **Relationship Signal Engine** is a security-first pipeline designed to identify at-risk client relationships for insurance and mortgage brokers. It transforms raw mailbox data into a "Morning Digest" while maintaining extreme privacy and data security.

---

## 🗺️ System Flow
**Mailbox** $\rightarrow$ **Watchlist Gate** $\rightarrow$ **Masking Layer** $\rightarrow$ **Signal Detection** $\rightarrow$ **Zero-Storage DB** $\rightarrow$ **Morning Digest**

### Visual Process:
1. **Watchlist Gate:** Filters out all emails except those from approved clients.
2. **Masking Layer:** Hides PII (Names, Numbers) before any AI analysis.
3. **Signal Detection:** Identifies risks using Math (Silence) and AI (Language).
4. **Zero-Storage:** Saves only the risk signal; deletes the original email text.
5. **Morning Digest:** Generates a clean report for the broker.

---

## 🛠️ Technical Implementation

### A. Privacy & Security (The "Privacy Wall")
To ensure a "fail-closed" security model, the system implements three layers:
- **Access Control:** The **Watchlist Gate** ensures no unauthorized email content is ever fetched.
- **Anonymization:** The **Masking Layer** replaces real identities with tags (e.g., `[PERSON_1]`, `[NUMBER]`).
- **Data Minimization:** A **Zero-Storage Policy** ensures that email bodies are processed in memory and never stored on disk.

### B. Signal Intelligence
The system uses a hybrid detection strategy:
- **Statistical (Math):** Detects **Silence** and **Drift** by calculating the time gap since the last client interaction.
- **Linguistic (AI):** Detects **Explicit Risks** (e.g., "cheaper quote") and **Implicit Risks** (e.g., tone shifts) using keyword analysis and LLM stubs.
- **Robustness:** The system is designed to be immune to **Prompt Injection** attacks by using a strict pipeline instead of relying solely on LLM instructions.

### C. Operational Design
- **Tenant Isolation:** Every query is locked to a specific `firm_id` to prevent data leakage between different firms.
- **Efficiency:** Designed to operate within provider rate limits (250 reads/min) and budget constraints ($3/seat/month).

---

## 🛡️ Security Matrix

| Threat | Control Measure | Result |
| :--- | :--- | :--- |
| **PII Leak** | Masking Layer | AI sees intent, not identity. |
| **Data Breach** | Zero-Storage Policy | No email bodies stored to be stolen. |
| **Cross-Tenant Leak** | `firm_id` Isolation | Firm A cannot access Firm B data. |
| **Prompt Injection** | Pipeline Logic | Client text cannot change system rules. |

---