# Glossary & Acronym Index — JHI Research & Analytics Firm, Inc.

> JHI-SIG: 69M2705M · The single reference for acronyms and terms used across JHI docs, code,
> and board minutes. **Maintenance rule:** whenever a new acronym is introduced anywhere, add it
> here. Keep alphabetical within the master table.

---

## 1. Priority levels (what "P0" means)
We prioritize with a **P0–P3** scale (highest → lowest):

| Level | Name | Meaning | Typical action |
|---|---|---|---|
| **P0** | Priority Zero | **Critical / launch-blocking / must-do-first.** Foundational; other work depends on it. | Do before anything built on top of it. |
| **P1** | Priority One | Important, not blocking. Needed before public/paid launch. | Schedule right after P0. |
| **P2** | Priority Two | Valuable; enhances maturity/scale. | After launch essentials. |
| **P3** | Priority Three | Nice-to-have / later. | Backlog. |

*(This mirrors the 🔴 High / 🟠 Medium / 🟡 Low severity used in audit docs: 🔴 ≈ P0/P1, 🟠 ≈ P1/P2, 🟡 ≈ P2/P3.)*

## 2. "System Admin P0 gatekeeper" (compound term)
- **Gatekeeper** — the access-control function that decides *who* (human or AI agent) may enter and *what* they may do: **authentication** (identity) + **authorization** (permission), enforced on every request. The platform's "bouncer."
- **System Admin P0 gatekeeper** — the highest-priority, foundational slice of the System Administrator module: **enforce auth + permissions across all endpoints** (close the currently-open ones), **require admin MFA**, **turn on full audit**, and provide the **minimal grant/revoke user management**. Everything else in the admin experience layers on top. See `docs/SYSTEM_ADMINISTRATOR_MODULE.md`.

---

## 3. Master acronym & term index (alphabetical)

| Acronym / Term | Expansion | Meaning in JHI context |
|---|---|---|
| 2FA | Two-Factor Authentication | Second login factor (e.g., TOTP code) on top of password. |
| ABAC | Attribute-Based Access Control | Access decided by attributes/policies; a more granular alternative/complement to RBAC. |
| ACH | Automated Clearing House | US bank-to-bank electronic payments (not yet integrated; Stripe is card today). |
| ADA | Americans with Disabilities Act | Accessibility compliance for the web app. |
| AP | Accounts Payable | Money JHI owes vendors (GL account 2000). |
| API | Application Programming Interface | The backend's `/api/v1/...` endpoints the frontend/mobile call. |
| AR | Accounts Receivable | Money owed to JHI by customers (GL account 1100). |
| ARPU | Average Revenue Per User | Revenue ÷ active users; an 8000-series management metric. |
| ARR | Annual Recurring Revenue | Annualized subscription revenue; 8000-series metric. |
| ASC 350-40 | Accounting Standards Codification 350-40 | US GAAP rules for capitalizing internal-use software costs. |
| BC / BCP | Business Continuity / Plan | Keeping the service running through disruptions (Phase XIX). |
| BD | Business Development | Sales/partnership function (e.g., PE BD). |
| BRD | Business Requirements Document | Formal statement of business needs for the software. |
| CAC | Customer Acquisition Cost | Cost to win a customer; 8000-series metric. |
| CCPA | California Consumer Privacy Act | California data-privacy law. |
| CDN | Content Delivery Network | Edge caching for fast static asset delivery. |
| CI/CD | Continuous Integration / Continuous Delivery | Automated build/test/deploy pipeline (not yet set up — `.github/` absent). |
| CIM | Confidential Information Memorandum | The seller's deal book a buyer analyzes (input to Deal X-Ray). |
| CLI | Command-Line Interface | Terminal tooling. |
| CORS | Cross-Origin Resource Sharing | Browser rule for cross-origin API calls (removed via same-origin proxy). |
| C-corp | C Corporation | JHI's entity type (WY Inc.). |
| CPA | Certified Public Accountant | Partner for signed Quality of Earnings; also the external auditor. |
| DAST | Dynamic Application Security Testing | Security testing of the running app. |
| DBA | Doing Business As | A registered trade name. |
| DCF | Discounted Cash Flow | Valuation method in the Deal X-Ray engine. |
| DNS | Domain Name System | Maps domain names to servers. |
| DPA | Data Processing Agreement | Contract governing how customer data is processed (privacy). |
| DR | Disaster Recovery | Restoring service/data after a major failure (Phase XIX). |
| DSCR | Debt Service Coverage Ratio | Cash flow ÷ debt payments; used in SBA/financing analysis. |
| EBITDA | Earnings Before Interest, Taxes, Depreciation & Amortization | Core profitability measure in the financial models. |
| EIN | Employer Identification Number | Federal tax ID for the corp. |
| ES256 | ECDSA using P-256 & SHA-256 | Signature algorithm used in WebAuthn verification. |
| ETA | Entrepreneurship Through Acquisition | The search-fund path (buy a business rather than start one) — a core ICP. |
| FINRA | Financial Industry Regulatory Authority | Broker-dealer regulator (JHI is a publisher, not a broker — monitored). |
| GAAP | Generally Accepted Accounting Principles | US accounting standards the financials target. |
| GDPR | General Data Protection Regulation | EU data-privacy law. |
| GL | General Ledger | The accounting system of record (chart of accounts + journal). |
| GP | General Partner | Fund manager (vs. LP); PE/VC term. |
| GRR | Gross Revenue Retention | Retained recurring revenue excluding expansion; 8000-series metric. |
| GTM | Go-To-Market | Marketing/sales strategy to reach customers. |
| HA | High Availability | Architecture that minimizes downtime. |
| IA | Information Architecture | How the app's navigation/screens are organized. |
| IAM | Identity & Access Management | Cloud permissions for users/services (AWS IAM, etc.). |
| IB | Investment Banking | A competitor-tool user segment (e.g., Capital IQ). |
| IC | Information Coefficient | Correlation between a signal and future returns; score-validation stat. |
| ICP | Ideal Customer Profile | The target buyer (searchers, SMB acquirers, family offices, RIAs). |
| Inc. | Incorporated | Corporation suffix (JHI Research & Analytics Firm, Inc.). |
| IP | Intellectual Property | The platform code, algorithms, brand, trade secrets. |
| ISO 27001 | ISO/IEC 27001 | Information-security management certification (readiness target). |
| JWT | JSON Web Token | Signed access token proving a logged-in principal. |
| K8s | Kubernetes | Container orchestration (planned infra, not deployed). |
| KPI | Key Performance Indicator | A tracked business metric. |
| LMM | Lower-Middle-Market | Deal-size segment above SMB, below mid-market. |
| LOI | Letter of Intent | Non-binding offer to buy a business. |
| LP | Limited Partner | Fund investor (vs. GP). |
| LTV | Lifetime Value | Total expected revenue per customer; 8000-series metric. |
| LLC | Limited Liability Company | Prior/family-office entity form. |
| M&A | Mergers & Acquisitions | Buying/selling companies. |
| MFA | Multi-Factor Authentication | Two-or-more login factors (superset of 2FA). |
| MRR | Monthly Recurring Revenue | Monthly subscription revenue; 8000-series metric. |
| MSA | Master Services Agreement | Umbrella customer/vendor contract (e.g., prepaid annual subscription). |
| MTTR | Mean Time To Recovery | Average time to restore after an incident. |
| MVP | Minimum Viable Product | Smallest launchable product. |
| NAICS | North American Industry Classification System | JHI = 513210 (Software Publishers). |
| NAV | Net Asset Value | Portfolio/holdings valuation term. |
| NDA | Non-Disclosure Agreement | Confidentiality contract (one-way / mutual). |
| NRR | Net Revenue Retention | Retained + expansion recurring revenue; 8000-series metric. |
| OOS | Out-Of-Sample | Data held back to test a model honestly (score validation). |
| ORM | Object-Relational Mapping | SQLAlchemy layer over Postgres (parameterized, injection-safe). |
| OWASP | Open Worldwide Application Security Project | Source of the "Top 10" web-security risks. |
| PBKDF2 | Password-Based Key Derivation Function 2 | Password-hashing algorithm in use. |
| PCI DSS | Payment Card Industry Data Security Standard | Card-data security (scope minimized — Stripe holds card data). |
| PE | Private Equity | Buyout investors; competitor-tool user segment. |
| PII | Personally Identifiable Information | Personal data requiring protection. |
| PIT | Point-In-Time | Data as it was known on a date (no look-ahead) — fundamentals rule. |
| PR | Pull Request | Proposed code change reviewed before merge to `main`. |
| PRD | Product Requirements Document | Detailed product spec. |
| P0–P3 | Priority Zero…Three | Priority scale (see §1). |
| QoE | Quality of Earnings | Diligence analysis normalizing a target's real earnings (CPA-signed). |
| RBAC | Role-Based Access Control | Permissions granted via roles (the admin model's foundation). |
| RCA | Root Cause Analysis | Post-incident investigation of the underlying cause. |
| RIA | Registered Investment Adviser | A regulated adviser (JHI is *not* one — research/publisher posture). |
| RPO | Recovery Point Objective | Max acceptable data loss (how far back a restore goes). |
| RTO | Recovery Time Objective | Max acceptable downtime before recovery. |
| SAST | Static Application Security Testing | Security analysis of source code. |
| SBA | Small Business Administration | US agency; SBA 7(a) loans in acquisition financing. |
| SCA | Software Composition Analysis | Scanning third-party/open-source dependencies for risk. |
| SDK | Software Development Kit | Libraries/tools for building on a platform. |
| SEC | Securities and Exchange Commission | US securities regulator (advertising/adviser rules monitored). |
| SF1 | Sharadar Core US Fundamentals (SF1) | The NASDAQ/Sharadar point-in-time fundamentals dataset. |
| SIEM | Security Information & Event Management | Centralized security-log analytics/alerting. |
| SLA | Service-Level Agreement | Committed uptime/support levels. |
| SMB | Small & Medium-sized Business | Core acquisition-target segment / ICP. |
| SoD | Separation of Duties | No single person controls a sensitive action end-to-end (four-eyes). |
| SOC | Security Operations Center | Team/function monitoring security events. |
| SOC 2 | System & Organization Controls 2 | Trust/security attestation (readiness target). |
| SOP | Standard Operating Procedure | Documented repeatable process. |
| SSO | Single Sign-On | One login across multiple systems. |
| SSL / TLS | Secure Sockets Layer / Transport Layer Security | Encryption in transit (HTTPS). |
| T&C | Terms & Conditions | Contract terms (e.g., NASDAQ data license). |
| TOC | Table of Contents | Index (this document is an acronym TOC). |
| TOTP | Time-based One-Time Password | The rotating 6-digit 2FA code (encrypted at rest). |
| ToS | Terms of Service | The user agreement governing platform use (to be adopted). |
| t-stat | t-statistic | Statistical significance measure; H5 bar is |t| ≥ 2.0. |
| UAT | User Acceptance Testing | End-user validation before release. |
| UI / UX | User Interface / User Experience | The look and the overall experience. |
| VC | Venture Capital | Startup investors; competitor-tool user segment. |
| VM | Virtual Machine | A virtualized server. |
| VPN | Virtual Private Network | Encrypted private network access. |
| WAF | Web Application Firewall | Filters malicious web traffic. |
| WebAuthn | Web Authentication | Standard for biometric/passkey login (ES256 in the mobile companion). |
| WY | Wyoming | State of incorporation. |
| H5 | Hypothesis 5 | JHI's pre-registered hypothesis/protocol for validating the Opportunity/Deal Score. |
| JHI-SIG | JHI Signature | Founder code-provenance token (`69M2705M`) stamped across the codebase. |

---

*Provenance: founder signature of record `69M2705M`. © 2026 JHI Research & Analytics Firm, Inc. All rights reserved. Confidential.*
