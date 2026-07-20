// JHI-SIG: 69M2705M | Entity/relationship graph (Phase 3 depth foundation) | JHI Research & Analytics Firm, Inc. (proprietary)
//
// The entity graph is the spine of the deep-dive product: Company · Firm · Advisor ·
// Transaction (keystone). Records link to each other so the subscriber can pivot
// across the graph with no dead ends. Seed data below is illustrative; the Postgres
// schema + EDGAR / client-upload depth land in later sub-phases (3.1 backend, Phase 5).

export type EntityKind = "company" | "firm" | "advisor" | "transaction";

export type KeyValue = { label: string; value: string };

export type FinancialRow = { metric: string; values: string[] };

export type Filing = { form: string; date: string; description: string };

export type RiskFlag = { area: string; level: "Low" | "Medium" | "High"; note: string };

export type NewsItem = { date: string; headline: string; source: string };

export type Ownership = "Public" | "Private" | "PE-backed" | "Subsidiary";

export type Company = {
  kind: "company";
  slug: string;
  name: string;
  ticker?: string;
  sector: string;
  industry: string;
  hq: string;
  founded: string;
  employees: string;
  ownership: Ownership;
  status: string;
  description: string;
  // Facets — a field left undefined renders a graceful "not yet mapped" state.
  financials?: { years: string[]; rows: FinancialRow[]; basis: string };
  ratios?: KeyValue[];
  valuation?: { rows: KeyValue[]; comps: string[]; basis: string };
  filings?: Filing[];
  governance?: KeyValue[];
  riskFlags?: RiskFlag[];
  transactionIds?: string[];
  advisorSlugs?: string[];
  news?: NewsItem[];
  analytics?: { rows: KeyValue[]; macroOverlay: string };
};

export type Firm = {
  kind: "firm";
  slug: string;
  name: string;
  type: "Private Equity" | "Strategic Acquirer" | "Family Office";
  hq: string;
  founded: string;
  aum?: string;
  strategy: string;
  description: string;
  portfolioCompanySlugs?: string[];
  transactionIds?: string[];
};

export type Advisor = {
  kind: "advisor";
  slug: string;
  name: string;
  type: "M&A Advisory" | "Investment Bank" | "Business Broker";
  hq: string;
  coverage: string;
  description: string;
  transactionIds?: string[];
};

export type Transaction = {
  kind: "transaction";
  id: string;
  date: string;
  type: "Acquisition" | "Investment" | "Recapitalization" | "Merger";
  targetSlug: string;
  acquirerSlug: string;
  acquirerKind: "firm" | "company";
  advisorSlugs: string[];
  value: string;
  stake: string;
  summary: string;
};

// ── Seed graph ──────────────────────────────────────────────────────────────

export const companies: Company[] = [
  {
    kind: "company",
    slug: "apex-hvac-services",
    name: "Apex HVAC Services",
    sector: "Industrials",
    industry: "HVAC & Mechanical Services",
    hq: "Charlotte, NC",
    founded: "2006",
    employees: "310",
    ownership: "PE-backed",
    status: "Active",
    description:
      "Regional commercial HVAC installation and recurring maintenance provider across the Carolinas, acquired by Blue Harbor Capital in 2024.",
    financials: {
      years: ["FY22", "FY23", "FY24"],
      basis: "Company-provided; unaudited management accounts.",
      rows: [
        { metric: "Revenue", values: ["$38.2M", "$44.6M", "$52.1M"] },
        { metric: "Gross profit", values: ["$11.1M", "$13.4M", "$16.0M"] },
        { metric: "Adjusted EBITDA", values: ["$5.0M", "$6.3M", "$7.8M"] },
        { metric: "EBITDA margin", values: ["13.1%", "14.1%", "15.0%"] },
        { metric: "Recurring revenue %", values: ["41%", "45%", "49%"] }
      ]
    },
    ratios: [
      { label: "Revenue CAGR (2y)", value: "16.8%" },
      { label: "Net debt / EBITDA", value: "2.1x" },
      { label: "DSCR", value: "2.4x" },
      { label: "FCF conversion", value: "72%" }
    ],
    valuation: {
      basis: "Indicative — Limited Scope Review. Not an audit or fairness opinion.",
      rows: [
        { label: "Entry EV", value: "$48.0M" },
        { label: "EV / EBITDA (FY24)", value: "6.2x" },
        { label: "EV / Revenue (FY24)", value: "0.92x" },
        { label: "Implied equity value", value: "$31.6M" }
      ],
      comps: ["northwind-industrial"]
    },
    governance: [
      { label: "Board seats", value: "5 (3 sponsor, 1 mgmt, 1 independent)" },
      { label: "Audit", value: "Reviewed (not audited)" },
      { label: "Key-person risk", value: "Founder retained 24-mo earnout" }
    ],
    riskFlags: [
      { area: "Customer concentration", level: "Medium", note: "Top 5 customers = 34% of revenue." },
      { area: "Labor", level: "Medium", note: "Skilled technician turnover above sector median." },
      { area: "Backlog", level: "Low", note: "9-month contracted maintenance backlog." }
    ],
    transactionIds: ["txn-apex-2024"],
    advisorSlugs: ["bristol-group-advisors"],
    news: [
      { date: "2024-09-12", headline: "Blue Harbor Capital acquires Apex HVAC Services", source: "Deal wire" },
      { date: "2024-10-02", headline: "Apex names new CFO to support buy-and-build", source: "Company release" }
    ],
    analytics: {
      macroOverlay:
        "Nonresidential construction spend and services PPI support pricing; watch skilled-labor wage inflation.",
      rows: [
        { label: "JHI Opportunity Score", value: "79 / 100" },
        { label: "Sector momentum", value: "Improving" },
        { label: "Rate sensitivity", value: "Moderate" }
      ]
    }
  },
  {
    kind: "company",
    slug: "summit-mechanical",
    name: "Summit Mechanical",
    sector: "Industrials",
    industry: "Mechanical Contracting",
    hq: "Richmond, VA",
    founded: "1998",
    employees: "180",
    ownership: "Subsidiary",
    status: "Active",
    description:
      "Mechanical contracting and facility services company; acquired by Evergreen Facility Group in 2023 as a platform for the Mid-Atlantic.",
    financials: {
      years: ["FY22", "FY23"],
      basis: "Company-provided; unaudited.",
      rows: [
        { metric: "Revenue", values: ["$24.9M", "$28.7M"] },
        { metric: "Adjusted EBITDA", values: ["$3.1M", "$3.9M"] },
        { metric: "EBITDA margin", values: ["12.4%", "13.6%"] }
      ]
    },
    ratios: [
      { label: "Revenue growth", value: "15.3%" },
      { label: "Net debt / EBITDA", value: "1.7x" }
    ],
    valuation: {
      basis: "Indicative — Limited Scope Review.",
      rows: [
        { label: "Entry EV", value: "$22.5M" },
        { label: "EV / EBITDA (FY23)", value: "5.8x" }
      ],
      comps: ["apex-hvac-services", "northwind-industrial"]
    },
    governance: [{ label: "Audit", value: "Reviewed (not audited)" }],
    riskFlags: [
      { area: "Integration", level: "Medium", note: "First platform add-on for Evergreen; systems migration in progress." }
    ],
    transactionIds: ["txn-summit-2023"],
    advisorSlugs: ["bristol-group-advisors"],
    news: [
      { date: "2023-06-20", headline: "Evergreen Facility Group acquires Summit Mechanical", source: "Deal wire" }
    ],
    analytics: {
      macroOverlay: "Mid-Atlantic nonresidential backlog steady; margin depends on labor availability.",
      rows: [
        { label: "JHI Opportunity Score", value: "71 / 100" },
        { label: "Sector momentum", value: "Stable" }
      ]
    }
  },
  {
    kind: "company",
    slug: "northwind-industrial",
    name: "Northwind Industrial Corp.",
    ticker: "NWIN",
    sector: "Industrials",
    industry: "Diversified Industrial Services",
    hq: "Columbus, OH",
    founded: "1979",
    employees: "4,200",
    ownership: "Public",
    status: "Active",
    description:
      "Publicly listed diversified industrial services roll-up; used as a public comparable for HVAC and mechanical-services valuation.",
    financials: {
      years: ["FY22", "FY23", "FY24"],
      basis: "Sourced from SEC filings (EDGAR). Selected line items.",
      rows: [
        { metric: "Revenue", values: ["$1.42B", "$1.55B", "$1.63B"] },
        { metric: "EBITDA", values: ["$212M", "$238M", "$251M"] },
        { metric: "EBITDA margin", values: ["14.9%", "15.4%", "15.4%"] }
      ]
    },
    ratios: [
      { label: "EV / EBITDA", value: "9.4x" },
      { label: "Net debt / EBITDA", value: "2.6x" },
      { label: "Dividend yield", value: "1.8%" }
    ],
    valuation: {
      basis: "Public market multiples (EDGAR-sourced fundamentals).",
      rows: [
        { label: "Market cap", value: "$2.1B" },
        { label: "Enterprise value", value: "$2.36B" },
        { label: "EV / EBITDA (FY24)", value: "9.4x" },
        { label: "EV / Revenue (FY24)", value: "1.45x" }
      ],
      comps: ["apex-hvac-services", "summit-mechanical"]
    },
    filings: [
      { form: "10-K", date: "2025-02-24", description: "Annual report, fiscal year 2024" },
      { form: "10-Q", date: "2025-05-06", description: "Quarterly report, Q1 2025" },
      { form: "8-K", date: "2025-03-11", description: "Acquisition of regional mechanical services platform" }
    ],
    governance: [
      { label: "Board independence", value: "8 of 10 independent" },
      { label: "Auditor", value: "Big Four (audited)" },
      { label: "Say-on-pay", value: "94% approval" }
    ],
    riskFlags: [
      { area: "Cyclicality", level: "Medium", note: "Exposure to nonresidential construction cycle." },
      { area: "Leverage", level: "Low", note: "Investment-grade credit profile." }
    ],
    transactionIds: [],
    news: [
      { date: "2025-03-11", headline: "Northwind announces platform acquisition", source: "SEC 8-K" }
    ],
    analytics: {
      macroOverlay: "Rate cuts would support nonresidential starts; services PPI passthrough intact.",
      rows: [
        { label: "JHI Opportunity Score", value: "74 / 100" },
        { label: "Sector momentum", value: "Improving" }
      ]
    }
  }
];

export const firms: Firm[] = [
  {
    kind: "firm",
    slug: "blue-harbor-capital",
    name: "Blue Harbor Capital",
    type: "Private Equity",
    hq: "Boston, MA",
    founded: "2011",
    aum: "$1.8B",
    strategy: "Lower-middle-market buy-and-build in industrial and facility services.",
    description:
      "Private equity firm focused on control investments in founder-owned industrial services businesses, executing buy-and-build strategies.",
    portfolioCompanySlugs: ["apex-hvac-services"],
    transactionIds: ["txn-apex-2024"]
  },
  {
    kind: "firm",
    slug: "evergreen-facility-group",
    name: "Evergreen Facility Group",
    type: "Strategic Acquirer",
    hq: "Atlanta, GA",
    founded: "2015",
    strategy: "Strategic consolidator of mechanical and facility-services companies.",
    description:
      "Operating platform acquiring regional mechanical and facility-services businesses to build a Southeast/Mid-Atlantic network.",
    portfolioCompanySlugs: ["summit-mechanical"],
    transactionIds: ["txn-summit-2023"]
  }
];

export const advisors: Advisor[] = [
  {
    kind: "advisor",
    slug: "bristol-group-advisors",
    name: "Bristol Group Advisors",
    type: "M&A Advisory",
    hq: "Philadelphia, PA",
    coverage: "East Coast lower-middle-market",
    description:
      "Sell-side M&A advisory serving founder-owned industrial and services businesses across the East Coast.",
    transactionIds: ["txn-apex-2024", "txn-summit-2023"]
  }
];

export const transactions: Transaction[] = [
  {
    kind: "transaction",
    id: "txn-apex-2024",
    date: "2024-09-12",
    type: "Acquisition",
    targetSlug: "apex-hvac-services",
    acquirerSlug: "blue-harbor-capital",
    acquirerKind: "firm",
    advisorSlugs: ["bristol-group-advisors"],
    value: "$48.0M",
    stake: "Majority (control)",
    summary:
      "Blue Harbor Capital acquired a majority stake in Apex HVAC Services; founder retained a minority position and 24-month earnout."
  },
  {
    kind: "transaction",
    id: "txn-summit-2023",
    date: "2023-06-20",
    type: "Acquisition",
    targetSlug: "summit-mechanical",
    acquirerSlug: "evergreen-facility-group",
    acquirerKind: "company",
    advisorSlugs: ["bristol-group-advisors"],
    value: "$22.5M",
    stake: "100%",
    summary:
      "Evergreen Facility Group acquired Summit Mechanical as its platform entry into the Mid-Atlantic mechanical-services market."
  }
];

// ── Lookups & helpers ─────────────────────────────────────────────────────────

export function getCompany(slug: string): Company | undefined {
  return companies.find((c) => c.slug === slug);
}
export function getFirm(slug: string): Firm | undefined {
  return firms.find((f) => f.slug === slug);
}
export function getAdvisor(slug: string): Advisor | undefined {
  return advisors.find((a) => a.slug === slug);
}
export function getTransaction(id: string): Transaction | undefined {
  return transactions.find((t) => t.id === id);
}

export function entityHref(kind: EntityKind, slug: string): string {
  switch (kind) {
    case "company":
      return `/companies/${slug}`;
    case "firm":
      return `/firms/${slug}`;
    case "advisor":
      return `/advisors/${slug}`;
    case "transaction":
      return `/companies/${slug}`; // transactions surface on their target record
  }
}

export type ResolvedAcquirer =
  | { kind: "firm"; entity: Firm }
  | { kind: "company"; entity: Company };

export type ResolvedTransaction = {
  txn: Transaction;
  target?: Company;
  acquirer?: ResolvedAcquirer;
  advisorList: Advisor[];
};

export function resolveTransaction(id: string): ResolvedTransaction | undefined {
  const txn = getTransaction(id);
  if (!txn) return undefined;
  const target = getCompany(txn.targetSlug);
  let acquirer: ResolvedAcquirer | undefined;
  if (txn.acquirerKind === "firm") {
    const entity = getFirm(txn.acquirerSlug);
    if (entity) acquirer = { kind: "firm", entity };
  } else {
    const entity = getCompany(txn.acquirerSlug);
    if (entity) acquirer = { kind: "company", entity };
  }
  const advisorList = txn.advisorSlugs
    .map((s) => getAdvisor(s))
    .filter((a): a is Advisor => Boolean(a));
  return { txn, target, acquirer, advisorList };
}

export type SearchResult = {
  kind: EntityKind;
  slug: string;
  name: string;
  sub: string;
  href: string;
};

export function searchEntities(query: string): SearchResult[] {
  const q = query.trim().toLowerCase();
  const results: SearchResult[] = [
    ...companies.map((c) => ({
      kind: "company" as const,
      slug: c.slug,
      name: c.name,
      sub: `${c.industry} · ${c.hq}`,
      href: entityHref("company", c.slug)
    })),
    ...firms.map((f) => ({
      kind: "firm" as const,
      slug: f.slug,
      name: f.name,
      sub: `${f.type} · ${f.hq}`,
      href: entityHref("firm", f.slug)
    })),
    ...advisors.map((a) => ({
      kind: "advisor" as const,
      slug: a.slug,
      name: a.name,
      sub: `${a.type} · ${a.hq}`,
      href: entityHref("advisor", a.slug)
    }))
  ];
  if (!q) return results;
  return results.filter(
    (r) => r.name.toLowerCase().includes(q) || r.sub.toLowerCase().includes(q)
  );
}
