// JHI-SIG: 69M2705M | Acquisition Intelligence Framework — hub + lead-gen funnel | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRole } from "@/components/role-provider";
import { FREE_COOKIE, setCookie } from "@/lib/auth";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/api/v1";

type Element = {
  id: string;
  name: string;
  summary: string;
  explainer: { how_to: string; what_to_look_for: string[]; why_it_matters: string };
  tool: { label: string; href: string; description: string };
  checklist: string[];
};

type ToolkitResource = { title: string; body: string; href: string | null };
type Toolkit = {
  status: string;
  message: string;
  resources: ToolkitResource[];
  cta_label: string;
  cta_href: string;
  disclaimer: string;
};

const SUBTOOLS = [
  { href: "/framework/ratios", label: "Key Financial Ratios", blurb: "Compute + interpret every deal ratio." },
  { href: "/framework/due-diligence", label: "Due-Diligence Checklist", blurb: "Categorized, exportable, pipeline-tracked." },
  { href: "/framework/industry-analysis", label: "Industry Benchmarks", blurb: "Derived sector margins & multiples." },
  { href: "/framework/market-analysis", label: "Market Analysis Template", blurb: "TAM/SAM/SOM + five forces." }
];

function downloadCsv(filename: string, rows: string[][]): void {
  const esc = (v: string) => `"${v.replace(/"/g, '""')}"`;
  const csv = rows.map((r) => r.map(esc).join(",")).join("\r\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

export function FrameworkHub() {
  const { setRole } = useRole();
  const [elements, setElements] = useState<Element[]>([]);
  const [openId, setOpenId] = useState<string | null>(null);
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [toolkit, setToolkit] = useState<Toolkit | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/framework/elements`)
      .then((r) => r.json())
      .then((d) => setElements(d.elements ?? []))
      .catch(() => setElements([]));
  }, []);

  const unlock = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const r = await fetch(`${API_BASE}/framework/toolkit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, full_name: name })
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data: Toolkit = await r.json();
      setToolkit(data);
      setCookie(FREE_COOKIE, "1", 90);
      setRole("free");
    } catch {
      setError("Couldn't unlock the toolkit right now — please try again shortly.");
    } finally {
      setBusy(false);
    }
  };

  const exportChecklist = (el: Element) => {
    const rows: string[][] = [["Element", "Checklist item", "Done"]];
    el.checklist.forEach((item) => rows.push([el.name, item, ""]));
    downloadCsv(`Aegira_${el.id}_checklist.csv`, rows);
  };

  const exportAll = () => {
    const rows: string[][] = [["Element", "Checklist item", "Done"]];
    elements.forEach((el) => el.checklist.forEach((item) => rows.push([el.name, item, ""])));
    downloadCsv("Aegira_acquisition_framework_checklist.csv", rows);
  };

  return (
    <div>
      {/* Lead-gen funnel: email-gated free toolkit */}
      <section className="app-section">
        <div className="news-subscribe" style={{ alignItems: "flex-start" }}>
          <div>
            <p className="eyebrow">Free · email-gated</p>
            <h3>Unlock the Acquisition Intelligence toolkit</h3>
            <p className="news-subscribe__blurb">
              A free walkthrough of the ten-element framework plus the ratios calculator,
              due-diligence checklist, and industry/market templates. Enter your email to
              unlock — then take it live with the paid tools.
            </p>
          </div>
          {toolkit ? (
            <div style={{ width: "100%" }}>
              <p className="news-subscribe__ok">{toolkit.message}</p>
              <div className="app-grid app-grid--two" style={{ marginTop: "0.75rem" }}>
                {toolkit.resources.map((res) => (
                  <article className="app-card" key={res.title}>
                    <h4 style={{ margin: "0 0 0.4rem" }}>{res.title}</h4>
                    <p style={{ fontSize: "var(--fs-sm)" }}>{res.body}</p>
                    {res.href ? (
                      <Link className="opportunity-card__link" href={res.href}>
                        Open →
                      </Link>
                    ) : null}
                  </article>
                ))}
              </div>
              <div className="upgrade-gate" style={{ marginTop: "1rem" }}>
                <p className="eyebrow">Take it live</p>
                <h3>Ready to run a real deal?</h3>
                <p>
                  The framework is the map. Aegira&apos;s Professional tier runs it end-to-end —
                  screening, valuation, earnings quality, and diligence — on your target.
                </p>
                <div className="upgrade-gate__actions">
                  <Link className="button button--primary" href={toolkit.cta_href}>
                    {toolkit.cta_label}
                  </Link>
                  <Link className="button button--secondary" href="/register">
                    Create a free account
                  </Link>
                </div>
              </div>
            </div>
          ) : (
            <form className="news-subscribe__row" onSubmit={unlock} style={{ flexWrap: "wrap" }}>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name (optional)"
                aria-label="Your name"
                className="dir-search"
              />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@firm.com"
                aria-label="Email address"
                className="dir-search"
              />
              <button type="submit" className="button button--primary" disabled={busy}>
                {busy ? "Unlocking…" : "Unlock free toolkit"}
              </button>
              {error ? <p className="news-subscribe__err">{error}</p> : null}
            </form>
          )}
        </div>
      </section>

      {/* Gap-fill sub-tools */}
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Interactive tools</p>
          <h2>Run the framework</h2>
        </div>
        <div className="app-grid app-grid--two">
          {SUBTOOLS.map((t) => (
            <Link className="app-card" key={t.href} href={t.href} style={{ textDecoration: "none", color: "inherit" }}>
              <h3 style={{ margin: "0 0 0.3rem" }}>{t.label}</h3>
              <p style={{ fontSize: "var(--fs-sm)" }}>{t.blurb}</p>
              <span className="opportunity-card__link">Open →</span>
            </Link>
          ))}
        </div>
      </section>

      {/* The ten elements */}
      <section className="app-section">
        <div className="app-section__heading" style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", gap: "1rem", flexWrap: "wrap" }}>
          <div>
            <p className="eyebrow">The framework</p>
            <h2>Ten elements of an acquisition analysis</h2>
          </div>
          {elements.length ? (
            <button type="button" className="button button--secondary" onClick={exportAll}>
              Export full checklist (CSV)
            </button>
          ) : null}
        </div>
        <div className="app-grid app-grid--two">
          {elements.map((el) => {
            const open = openId === el.id;
            return (
              <article className="app-card" key={el.id}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: "0.5rem" }}>
                  <h3 style={{ margin: "0 0 0.3rem" }}>{el.name}</h3>
                </div>
                <p style={{ fontSize: "var(--fs-sm)" }}>{el.summary}</p>

                <button
                  type="button"
                  className="m-link"
                  onClick={() => setOpenId(open ? null : el.id)}
                  style={{ marginTop: "0.4rem", color: "var(--growth)", background: "none", border: 0, cursor: "pointer", font: "inherit", fontWeight: 800, padding: 0 }}
                >
                  {open ? "Hide explainer −" : "Read explainer +"}
                </button>

                {open ? (
                  <div style={{ marginTop: "0.6rem", borderTop: "1px solid var(--border)", paddingTop: "0.6rem" }}>
                    <p className="eyebrow">How to do it</p>
                    <p style={{ fontSize: "var(--fs-sm)" }}>{el.explainer.how_to}</p>
                    <p className="eyebrow" style={{ marginTop: "0.5rem" }}>What to look for</p>
                    <ul style={{ fontSize: "var(--fs-sm)", margin: "0.2rem 0 0", paddingLeft: "1.1rem" }}>
                      {el.explainer.what_to_look_for.map((w) => (
                        <li key={w}>{w}</li>
                      ))}
                    </ul>
                    <p className="eyebrow" style={{ marginTop: "0.5rem" }}>Why it matters</p>
                    <p style={{ fontSize: "var(--fs-sm)" }}>{el.explainer.why_it_matters}</p>
                    <p className="eyebrow" style={{ marginTop: "0.5rem" }}>Checklist</p>
                    <ul style={{ fontSize: "var(--fs-sm)", margin: "0.2rem 0 0", paddingLeft: "1.1rem" }}>
                      {el.checklist.map((c) => (
                        <li key={c}>{c}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}

                <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginTop: "0.8rem" }}>
                  <Link className="button button--primary" href={el.tool.href}>
                    {el.tool.label}
                  </Link>
                  <button type="button" className="button button--secondary" onClick={() => exportChecklist(el)}>
                    Download checklist (CSV)
                  </button>
                </div>
                <p className="live-market__muted" style={{ fontSize: "var(--fs-xs, 0.72rem)", marginTop: "0.4rem" }}>
                  {el.tool.description}
                </p>
              </article>
            );
          })}
        </div>
      </section>
    </div>
  );
}
