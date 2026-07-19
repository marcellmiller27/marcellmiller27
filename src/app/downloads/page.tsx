// JHI-SIG: 69M2705M | Firm Documents / Downloads | John Henry Investments (proprietary)
import { PlatformShell } from "@/components/platform-shell";

type DocItem = {
  title: string;
  description: string;
  href: string;
  kind: string;
};

const documents: DocItem[] = [
  {
    title: "Sales Commission & EBITDA Model",
    description:
      "Editable workbook: 24-month commission schedule, Year-1 by mix, a monthly EBITDA & operating-cost statement, and the prepaid-MSA salesperson-bonus sheet (bonus = 10% of EBITDA).",
    href: "/downloads/JHI_Sales_Commission_EBITDA_Model.xlsx",
    kind: "Excel workbook (.xlsx)"
  },
  {
    title: "Sales Commission — Prepaid MSA (15% Upfront + Year-End Bonus)",
    description:
      "Editable forecast for full-paid (prepaid annual, 12-month MSA) subscriptions: a 15% upfront commission on net contract value, a year-end MSA-completion bonus, a full P&L with ALL expenditures at 100 closes/mo \u2192 1,200 subs/yr, month-by-month breakdowns (bookings/cash and accrual/ASC 606), plus a Tier-1 mix sensitivity.",
    href: "/downloads/JHI_Sales_Commission_Prepaid_MSA.xlsx",
    kind: "Excel workbook (.xlsx)"
  },
  {
    title: "Competitor Deep-Dive & Reverse-Engineering Audit",
    description:
      "Mergr, S&P Global (Capital IQ Pro), and CB Insights: per-competitor teardown, synthesis matrix, the \u201cdiamond in the rough\u201d thesis, cost/risk/reward, verified pricing, and a board recommendation.",
    href: "/downloads/JHI_Competitor_Deep_Dive_Mergr_SPGlobal_CBInsights.docx",
    kind: "Word document (.docx)"
  },
  {
    title: "Data-Sources Comparison",
    description:
      "Breakdown of 11 market & economic data sources (Nasdaq Data Link, Twelve Data, FRED, SEC EDGAR, BLS, BEA, Treasury, Federal Reserve, IMF, OECD, World Bank) by coverage, cost, and \u2014 critically \u2014 redistribution rights to subscribers. Includes a FRED datasets sheet and a redistribution-rights matrix.",
    href: "/downloads/JHI_Data_Sources_Comparison.xlsx",
    kind: "Excel workbook (.xlsx)"
  }
];

const cardStyle = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  gap: "1rem",
  flexWrap: "wrap" as const,
  marginBottom: "0.9rem"
};

const btnStyle = {
  display: "inline-block",
  padding: "0.6rem 1.2rem",
  borderRadius: "999px",
  background: "var(--growth, #1f7a4d)",
  color: "#fff",
  fontWeight: 800,
  fontSize: "0.9rem",
  textDecoration: "none",
  whiteSpace: "nowrap" as const
};

export default function DownloadsPage() {
  return (
    <PlatformShell
      eyebrow="Firm operations"
      title="Documents"
      description="Download the firm's models and reports. Files open in Excel / Numbers / Google Sheets (.xlsx) or Word / Pages / Google Docs (.docx)."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Downloads</p>
          <h2>Models &amp; reports</h2>
        </div>
        {documents.map((doc) => (
          <article className="app-card" key={doc.href} style={cardStyle}>
            <div style={{ flex: 1, minWidth: "240px" }}>
              <strong style={{ fontSize: "1.02rem" }}>{doc.title}</strong>
              <p style={{ color: "var(--muted)", fontSize: "0.72rem", fontWeight: 800, textTransform: "uppercase", margin: "0.2rem 0" }}>
                {doc.kind}
              </p>
              <p style={{ color: "var(--muted)", fontSize: "0.88rem", margin: 0 }}>{doc.description}</p>
            </div>
            <a href={doc.href} download style={btnStyle}>
              Download
            </a>
          </article>
        ))}
        <p style={{ color: "var(--muted)", fontSize: "0.8rem", marginTop: "0.5rem" }}>
          Confidential — for internal use. Provenance: JHI-SIG 69M2705M.
        </p>
      </section>
    </PlatformShell>
  );
}
