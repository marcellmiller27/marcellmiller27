"use client";
// JHI-SIG: 69M2705M | Firm Documents (staff-only download client) | JHI Research & Analytics Firm, Inc. (proprietary)
// Confidential firm files are no longer statically served from public/. Each download
// hits the staff-gated backend endpoint (GET /api/v1/firm-documents/{name}) via apiFetch,
// which forwards the auth token as a Bearer header. A non-staff/anonymous request gets
// 401/403 and never receives the bytes.

import { useState } from "react";
import { apiFetch } from "@/lib/api";

type DocItem = {
  title: string;
  description: string;
  name: string;
  kind: string;
};

const documents: DocItem[] = [
  {
    title: "Sales Commission & EBITDA Model",
    description:
      "Editable workbook: 24-month commission schedule, Year-1 by mix, a monthly EBITDA & operating-cost statement, and the prepaid-MSA salesperson-bonus sheet (bonus = 10% of EBITDA).",
    name: "Aegira_Sales_Commission_EBITDA_Model.xlsx",
    kind: "Excel workbook (.xlsx)"
  },
  {
    title: "Competitor Deep-Dive & Reverse-Engineering Audit",
    description:
      "Mergr, S&P Global (Capital IQ Pro), and CB Insights: per-competitor teardown, synthesis matrix, the \u201cdiamond in the rough\u201d thesis, cost/risk/reward, verified pricing, and a board recommendation.",
    name: "Aegira_Competitor_Deep_Dive_Mergr_SPGlobal_CBInsights.docx",
    kind: "Word document (.docx)"
  },
  {
    title: "Data-Sources Comparison",
    description:
      "Breakdown of 11 market & economic data sources (Nasdaq Data Link, Twelve Data, FRED, SEC EDGAR, BLS, BEA, Treasury, Federal Reserve, IMF, OECD, World Bank) by coverage, cost, and \u2014 critically \u2014 redistribution rights to subscribers. Includes a FRED datasets sheet and a redistribution-rights matrix.",
    name: "Aegira_Data_Sources_Comparison.xlsx",
    kind: "Excel workbook (.xlsx)"
  },
  {
    title: "5-Year Consolidated Projections",
    description:
      "Audited-realistic three-statement model: monthly P&L, Cash Flow, and Balance Sheet with cohort-based renewals, EBITDA-gated staffing, and full reconciliation toward the growth plan.",
    name: "Aegira_5yr_Consolidated_Projections.xlsx",
    kind: "Excel workbook (.xlsx)"
  },
  {
    title: "Sales Commission — Prepaid MSA",
    description:
      "Commission model for the prepaid-MSA structure (15% upfront + year-end MSA bonus), with the schedule, Year-1 by mix, and the salesperson-bonus sheet.",
    name: "Aegira_Sales_Commission_Prepaid_MSA.xlsx",
    kind: "Excel workbook (.xlsx)"
  },
  {
    title: "Company Book — Policy · Procedures · Processes",
    description:
      "The firm's operating handbook: governance, policies, standard procedures, and core processes across the platform and back office.",
    name: "Aegira_Company_Book_Policy_Procedures_Processes.docx",
    kind: "Word document (.docx)"
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
  fontSize: "var(--fs-base)",
  border: "none",
  cursor: "pointer",
  textDecoration: "none",
  whiteSpace: "nowrap" as const
};

export function FirmDocuments() {
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function download(doc: DocItem) {
    setError(null);
    setBusy(doc.name);
    try {
      const res = await apiFetch(`/firm-documents/${encodeURIComponent(doc.name)}`);
      if (!res.ok) {
        setError(
          res.status === 401 || res.status === 403
            ? "You are not authorized to download this document."
            : `Download failed (HTTP ${res.status}).`
        );
        return;
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = doc.name;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch {
      setError("Could not reach the documents service.");
    } finally {
      setBusy(null);
    }
  }

  return (
    <section className="app-section">
      <div className="app-section__heading">
        <p className="eyebrow">Downloads</p>
        <h2>Models &amp; reports</h2>
      </div>
      {error ? (
        <p style={{ color: "#c0392b", fontSize: "var(--fs-sm)", fontWeight: 700 }}>{error}</p>
      ) : null}
      {documents.map((doc) => (
        <article className="app-card" key={doc.name} style={cardStyle}>
          <div style={{ flex: 1, minWidth: "240px" }}>
            <strong style={{ fontSize: "var(--fs-lg)" }}>{doc.title}</strong>
            <p style={{ color: "var(--muted)", fontSize: "var(--fs-xs)", fontWeight: 800, textTransform: "uppercase", margin: "0.2rem 0" }}>
              {doc.kind}
            </p>
            <p style={{ color: "var(--muted)", fontSize: "var(--fs-base)", margin: 0 }}>{doc.description}</p>
          </div>
          <button type="button" onClick={() => download(doc)} disabled={busy === doc.name} style={btnStyle}>
            {busy === doc.name ? "Downloading…" : "Download"}
          </button>
        </article>
      ))}
      <p style={{ color: "var(--muted)", fontSize: "var(--fs-sm)", marginTop: "0.5rem" }}>
        Confidential — for internal use. Provenance: JHI-SIG 69M2705M.
      </p>
    </section>
  );
}
