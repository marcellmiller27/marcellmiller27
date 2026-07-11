export type PricingTier = {
  name: string;
  audience: string;
  price: string;
  target: string;
  revenue: string;
  features: string[];
};

export type PlatformModule = {
  phase: string;
  name: string;
  summary: string;
  features: string[];
  output?: string;
};

export type ScoreCategory = {
  assetClass: string;
  factors: string[];
};

export type StackLayer = {
  layer: string;
  tools: string[];
};

export type DashboardMetric = {
  label: string;
  value: string;
  change: string;
  tone: "positive" | "neutral" | "warning";
};

export type MarketSignal = {
  name: string;
  value: string;
  insight: string;
};

export type Opportunity = {
  name: string;
  category: string;
  score: number;
  recommendation: "Buy" | "Watch" | "Pass";
  thesis: string;
  metrics: string[];
};

export type DueDiligenceItem = {
  document: string;
  status: string;
  finding: string;
  risk: "Low" | "Medium" | "High";
};

export type PortfolioHolding = {
  name: string;
  assetClass: string;
  allocation: string;
  returnProfile: string;
  cashFlow: string;
};

export type IntelligenceReport = {
  title: string;
  cadence: string;
  audience: string;
  highlights: string[];
};

export type AssistantWorkflow = {
  prompt: string;
  response: string;
  outputs: string[];
};

export const pricingTiers: PricingTier[] = [
  {
    name: "Consumer Plan",
    audience: "Retail investors and wealth builders",
    price: "$50 / month",
    target: "50,000 subscribers",
    revenue: "$2.5M monthly recurring revenue",
    features: [
      "Portfolio tracker",
      "AI research assistant",
      "Market intelligence",
      "Opportunity scanner"
    ]
  },
  {
    name: "Professional Plan",
    audience: "Acquisition entrepreneurs and advisors",
    price: "$299 / month",
    target: "5,000 subscribers",
    revenue: "$1.495M monthly recurring revenue",
    features: [
      "Business acquisition engine",
      "Due diligence tools",
      "Business analysis",
      "Capital raising workflows"
    ]
  },
  {
    name: "Enterprise / Family Office",
    audience: "Family offices, investment firms, CPAs, attorneys, and bankers",
    price: "$1,500+ / month",
    target: "500 subscribers",
    revenue: "$750K+ monthly recurring revenue",
    features: [
      "Team accounts and role permissions",
      "Branded intelligence reports",
      "Portfolio and entity oversight",
      "Custom research workflows"
    ]
  }
];

export const userTypes = [
  "Retail Investor",
  "Accredited Investor",
  "Business Buyer",
  "Family Office",
  "Investment Firm",
  "CPA",
  "Attorney",
  "Banker"
];

export const dashboardWidgets = [
  "BTC",
  "Gold",
  "S&P 500",
  "Treasury Rates",
  "Inflation",
  "Real Estate Trends"
];

export const platformModules: PlatformModule[] = [
  {
    phase: "Phase 1 - Core Platform",
    name: "User Management",
    summary: "Secure identity, profile, team, and permission management for every investor type.",
    features: [
      "User registration",
      "Multi-factor authentication",
      "Profile management",
      "Team accounts",
      "Role permissions"
    ]
  },
  {
    phase: "Phase 1 - Core Platform",
    name: "Dashboard",
    summary: "Home screen for portfolio value, watch lists, market alerts, economic indicators, and AI recommendations.",
    features: [
      "Portfolio value",
      "Watch lists",
      "Market alerts",
      "Economic indicators",
      "Acquisition opportunities",
      "AI recommendations"
    ]
  },
  {
    phase: "Phase 2 - AI Opportunity Engine",
    name: "Investment Discovery Engine",
    summary: "Screens public, private, real estate, bond, and cryptocurrency opportunities.",
    features: [
      "Revenue growth",
      "EBITDA",
      "Debt ratios",
      "Dividend yield",
      "Insider buying",
      "Valuation metrics"
    ],
    output: "Investment Score: 0-100"
  },
  {
    phase: "Phase 2 - AI Opportunity Engine",
    name: "Business Acquisition Engine",
    summary: "Analyzes SBA opportunities, listed businesses, franchises, distressed assets, and family-owned companies.",
    features: [
      "EBITDA",
      "Seller discretionary earnings",
      "SBA qualification",
      "Debt service coverage ratio",
      "Valuation models"
    ],
    output: "Recommendation: Buy, Watch, or Pass"
  },
  {
    phase: "Phase 2 - AI Opportunity Engine",
    name: "AI Due Diligence Center",
    summary: "Uploads and reviews financial documents for acquisition, lending, and investment diligence.",
    features: [
      "Tax return upload",
      "P&L statement upload",
      "Balance sheet upload",
      "Bank statement upload",
      "Risk assessment",
      "Fraud indicators"
    ],
    output: "Risk assessment, cash flow analysis, fraud indicators, and opportunity score"
  },
  {
    phase: "Phase 3 - John Henry Intelligence Center",
    name: "Global Macro Dashboard",
    summary: "Tracks central banks, rates, commodities, Bitcoin, money supply, and economic cycles.",
    features: [
      "Federal Reserve",
      "ECB",
      "BOJ",
      "PBOC",
      "Treasury markets",
      "CPI, PPI, M2, GDP, unemployment"
    ],
    output: "Recession probability, inflation outlook, and liquidity trends"
  },
  {
    phase: "Phase 3 - John Henry Intelligence Center",
    name: "Weekly Intelligence Reports",
    summary: "Automated branded reports for macro, crypto, acquisitions, and dividend opportunities.",
    features: [
      "John Henry Weekly Macro Report",
      "Crypto Intelligence Report",
      "Business Acquisition Report",
      "Dividend Opportunities Report",
      "PDF downloads",
      "Branded reports"
    ]
  },
  {
    phase: "Phase 3 - John Henry Intelligence Center",
    name: "AI Research Assistant",
    summary: "Private AI assistant for security analysis, acquisition review, SBA comparisons, and portfolio construction.",
    features: [
      "Analyze Tesla",
      "Evaluate this business",
      "Compare SBA loans",
      "Build dividend portfolio",
      "Analyze Bitcoin cycle"
    ],
    output: "Charts, reports, risk scores, and recommendations"
  },
  {
    phase: "Phase 4 - Portfolio Management",
    name: "Portfolio Tracking",
    summary: "Connects banks, brokerages, crypto exchanges, and private holdings into one wealth dashboard.",
    features: [
      "Stocks",
      "ETFs",
      "Crypto",
      "Real estate",
      "Private equity",
      "ROI, IRR, Sharpe ratio, and cash flow"
    ]
  },
  {
    phase: "Phase 4 - Portfolio Management",
    name: "Wealth Projection Engine",
    summary: "Projects retirement, family office growth, trust planning, and generational wealth scenarios.",
    features: ["Bull case", "Base case", "Bear case", "Retirement", "Trust planning"]
  },
  {
    phase: "Phase 5 - Business Owner Platform",
    name: "Corporate Governance Center",
    summary: "Generates entity governance documents for LLCs and corporations.",
    features: [
      "Operating agreements",
      "Meeting minutes",
      "Stock certificates",
      "Board resolutions",
      "Shareholder agreements"
    ]
  },
  {
    phase: "Phase 5 - Business Owner Platform",
    name: "Capital Raising Center",
    summary: "Helps companies prepare investor, lender, SBA, and financial model packages.",
    features: [
      "Investor decks",
      "Loan packages",
      "SBA packages",
      "Financial models",
      "Investor tracking",
      "Funding status"
    ]
  },
  {
    phase: "Phase 6 - AI Scoring System",
    name: "John Henry Opportunity Score",
    summary: "Proprietary 0-100 score across public markets, business acquisitions, and crypto assets.",
    features: [
      "Valuation",
      "Growth",
      "Risk",
      "Industry quality",
      "Liquidity",
      "Institutional activity"
    ],
    output: "Overall Score: 0-100"
  }
];

export const scoreCategories: ScoreCategory[] = [
  {
    assetClass: "Stocks",
    factors: ["Valuation", "Growth", "Risk"]
  },
  {
    assetClass: "Businesses",
    factors: ["EBITDA", "Industry", "Competition"]
  },
  {
    assetClass: "Crypto",
    factors: ["Adoption", "Liquidity", "Institutional Activity"]
  }
];

export const techStack: StackLayer[] = [
  {
    layer: "Front End",
    tools: ["React", "Next.js", "TypeScript"]
  },
  {
    layer: "Mobile",
    tools: ["Flutter", "React Native"]
  },
  {
    layer: "Backend",
    tools: ["Python", "FastAPI"]
  },
  {
    layer: "Database",
    tools: ["PostgreSQL", "Supabase"]
  },
  {
    layer: "AI Layer",
    tools: ["OpenAI", "Anthropic", "Custom Financial Models"]
  },
  {
    layer: "Cloud",
    tools: ["Amazon Web Services", "Vercel", "Private Cloud"]
  }
];

export const dashboardMetrics: DashboardMetric[] = [
  {
    label: "Portfolio value",
    value: "$4.82M",
    change: "+8.4% YTD",
    tone: "positive"
  },
  {
    label: "Watch list alerts",
    value: "18",
    change: "5 high priority",
    tone: "warning"
  },
  {
    label: "Acquisition pipeline",
    value: "$12.6M",
    change: "7 active targets",
    tone: "neutral"
  },
  {
    label: "Macro risk",
    value: "Moderate",
    change: "Liquidity improving",
    tone: "neutral"
  }
];

export const marketSignals: MarketSignal[] = [
  {
    name: "BTC",
    value: "$112,450",
    insight: "Institutional flows remain positive while volatility compresses."
  },
  {
    name: "Gold",
    value: "$3,180",
    insight: "Safe-haven demand remains elevated against fiscal deficit risk."
  },
  {
    name: "S&P 500",
    value: "6,240",
    insight: "Earnings breadth is improving but valuation multiples remain extended."
  },
  {
    name: "Treasury rates",
    value: "4.12%",
    insight: "Curve steepening supports bank margins and credit monitoring."
  },
  {
    name: "Inflation",
    value: "2.8%",
    insight: "Services inflation is the key factor for rate-cut timing."
  },
  {
    name: "Real estate",
    value: "Selective",
    insight: "Industrial and cash-flowing small multifamily remain preferred screens."
  }
];

export const opportunities: Opportunity[] = [
  {
    name: "Dividend Compounder Basket",
    category: "Public equities",
    score: 84,
    recommendation: "Buy",
    thesis: "High free-cash-flow companies with durable margins and dividend growth.",
    metrics: ["3.8% dividend yield", "12% five-year dividend CAGR", "Low leverage"]
  },
  {
    name: "Regional HVAC Services Platform",
    category: "Business acquisition",
    score: 79,
    recommendation: "Watch",
    thesis: "Recurring maintenance revenue and fragmented local competition support roll-up potential.",
    metrics: ["$1.2M EBITDA", "2.1x DSCR", "SBA eligible"]
  },
  {
    name: "Bitcoin Cycle Allocation",
    category: "Digital assets",
    score: 72,
    recommendation: "Watch",
    thesis: "Liquidity and adoption signals are favorable, but position sizing should respect volatility.",
    metrics: ["ETF inflows positive", "Liquidity trend up", "High volatility"]
  },
  {
    name: "Distressed Retail Strip Center",
    category: "Real estate",
    score: 48,
    recommendation: "Pass",
    thesis: "Tenant concentration and refinancing risk outweigh current cap-rate discount.",
    metrics: ["62% occupancy", "Near-term debt maturity", "Weak tenant mix"]
  }
];

export const dueDiligenceQueue: DueDiligenceItem[] = [
  {
    document: "Three-year tax returns",
    status: "Analyzed",
    finding: "Revenue trend reconciles with bank deposits.",
    risk: "Low"
  },
  {
    document: "Profit and loss statements",
    status: "Needs review",
    finding: "Owner add-backs require supporting documentation.",
    risk: "Medium"
  },
  {
    document: "Balance sheet",
    status: "Analyzed",
    finding: "Working-capital swing appears seasonal.",
    risk: "Low"
  },
  {
    document: "Bank statements",
    status: "Flagged",
    finding: "Two large irregular withdrawals need explanation.",
    risk: "High"
  }
];

export const portfolioHoldings: PortfolioHolding[] = [
  {
    name: "Core equity portfolio",
    assetClass: "Stocks and ETFs",
    allocation: "42%",
    returnProfile: "11.2% IRR",
    cashFlow: "$86K annual dividends"
  },
  {
    name: "Acquired operating businesses",
    assetClass: "Private equity",
    allocation: "28%",
    returnProfile: "18.5% IRR",
    cashFlow: "$410K owner distributions"
  },
  {
    name: "Income real estate",
    assetClass: "Real estate",
    allocation: "21%",
    returnProfile: "9.4% cash-on-cash",
    cashFlow: "$168K net operating income"
  },
  {
    name: "Digital assets",
    assetClass: "Crypto",
    allocation: "9%",
    returnProfile: "High volatility",
    cashFlow: "No current yield"
  }
];

export const intelligenceReports: IntelligenceReport[] = [
  {
    title: "John Henry Weekly Macro Report",
    cadence: "Weekly",
    audience: "All paid subscribers",
    highlights: ["Federal Reserve policy", "Treasury liquidity", "Inflation outlook"]
  },
  {
    title: "Business Acquisition Report",
    cadence: "Weekly",
    audience: "Professional and Enterprise",
    highlights: ["SBA deal screens", "Valuation trends", "Debt-service analysis"]
  },
  {
    title: "Crypto Intelligence Report",
    cadence: "Biweekly",
    audience: "Consumer and Professional",
    highlights: ["Bitcoin cycle", "ETF flows", "Liquidity and adoption signals"]
  },
  {
    title: "Dividend Opportunities Report",
    cadence: "Monthly",
    audience: "All paid subscribers",
    highlights: ["Dividend growth", "Balance-sheet quality", "Income portfolio ideas"]
  }
];

export const assistantWorkflows: AssistantWorkflow[] = [
  {
    prompt: "Analyze Tesla for a long-term investor.",
    response: "Compare valuation, margin durability, capital intensity, and competitive pressure.",
    outputs: ["Bull/base/bear case", "Risk score", "Comparable valuation"]
  },
  {
    prompt: "Evaluate this HVAC acquisition target.",
    response: "Normalize EBITDA, estimate SBA debt service, and flag diligence questions.",
    outputs: ["Buy/Watch/Pass", "DSCR estimate", "Document request list"]
  },
  {
    prompt: "Build a dividend portfolio for monthly income.",
    response: "Blend yield, dividend growth, sector exposure, and balance-sheet strength.",
    outputs: ["Model allocation", "Expected yield", "Rebalancing rules"]
  }
];
