"use client";
// JHI-SIG: 69M2705M | Newsletter edition renderer (backend-sourced) | JHI Research & Analytics Firm, Inc. (proprietary)
// Renders an edition from the backend content API (deterministic build + E2 LLM
// elevation, fact-locked). Single source of truth for on-screen, the PDF (which
// prints this page), and future email. Per-variant styling preserves each edition's look.
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { EditorialByline } from "@/components/editorial-byline";
import { NewsletterDownloadButton } from "@/components/newsletter-download-button";
import { UpgradeGate } from "@/components/upgrade-gate";

type Item = { label: string; value: string; body: string; tags: string[]; source: string | null };
type Chart = { label: string; image: string; caption: string; source: string | null };
type Group = { heading: string; blurb: string; items: Item[]; charts?: Chart[] };
type Edition = {
  slug: string;
  title: string;
  eyebrow: string;
  dateline: string;
  intro: string;
  groups: Group[];
  footer: string;
  disclaimer: string;
  methodology: string;
  teaser: boolean;
  charts?: Chart[];
};
type Payload = { edition: Edition; as_of: string; editorial: string };
type Variant = "brief" | "alerts" | "scan" | "insider";

// Sectioned editions (thesis/summary + analytical sections + items) share one layout.
const SECTIONED: Variant[] = ["brief", "insider"];

// Server-rendered charts embedded as base64 data-URIs (the PDF prints these too).
function ChartFigures({ charts }: { charts?: Chart[] }) {
  if (!charts || charts.length === 0) return null;
  return (
    <div className="news__charts">
      {charts.map((c) => (
        <figure className="news__chart" key={c.label}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={c.image} alt={c.label} className="news__chart-img" />
          {c.caption ? <figcaption className="news__chart-caption">{c.caption}</figcaption> : null}
          {c.source ? <p className="news__source">{c.source}</p> : null}
        </figure>
      ))}
    </div>
  );
}

export function NewsletterEdition({ slug, variant }: { slug: string; variant: Variant }) {
  const [data, setData] = useState<Payload | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    apiFetch(`/newsletters/${slug}`)
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(`HTTP ${r.status}`))))
      .then((d: Payload) => active && setData(d))
      .catch((e) => active && setError(String(e.message ?? e)));
    return () => {
      active = false;
    };
  }, [slug]);

  if (error) return <p className="rec-empty">Unable to reach the data service ({error}).</p>;
  if (!data) return <p className="rec-empty">Generating the latest edition from live data…</p>;

  const ed = data.edition;

  return (
    <article className="news">
      <NewsletterDownloadButton slug={slug} />

      <header className="news__masthead">
        <p className="eyebrow">Aegira · {ed.eyebrow}</p>
        <h2>{ed.title}</h2>
        <p className="news__edition">{ed.dateline}</p>
        <EditorialByline />
      </header>

      {ed.intro ? (
        <section className="news__lede">
          {SECTIONED.includes(variant) ? (
            <h3>{variant === "insider" ? "Thesis" : "Executive summary"}</h3>
          ) : null}
          <p>{ed.intro}</p>
        </section>
      ) : null}

      {/* Edition-level exhibits (e.g. the Economic Brief macro chart). */}
      <ChartFigures charts={ed.charts} />

      {SECTIONED.includes(variant) && ed.groups.map((g) => (
        <section className="news__section" key={g.heading}>
          <h3>{g.heading}</h3>
          {g.blurb ? <p className="news__blurb">{g.blurb}</p> : null}
          <ChartFigures charts={g.charts} />
          <ul className="news__rows">
            {g.items.map((it) => (
              <li className="news__row" key={it.label}>
                <div className="news__row-head">
                  <span className="news__metric">{it.label}</span>
                  <strong className="news__value">{it.value}</strong>
                </div>
                <p className="news__note">{it.body}</p>
                {it.source ? <p className="news__source">{it.source}</p> : null}
              </li>
            ))}
          </ul>
        </section>
      ))}

      {variant === "alerts" && (
        (ed.groups[0]?.items.length ?? 0) === 0 ? (
          <p className="rec-empty">All clear — no red alerts. Tracked indicators are within normal bands.</p>
        ) : (
          <ul className="alert-list">
            {ed.groups[0].items.map((a, i) => (
              <li className={`alert alert--${a.label.toLowerCase()}`} key={i}>
                <div className="alert__head">
                  <span className="alert__sev">{a.label}</span>
                  <strong className="alert__title">{a.value}</strong>
                </div>
                <p className="alert__detail">{a.body}</p>
                <div className="output-tags">
                  {a.tags.map((c) => (
                    <span className="tag" key={c}>{c}</span>
                  ))}
                </div>
              </li>
            ))}
          </ul>
        )
      )}

      {variant === "scan" && (
        <>
          <div className="scan-grid">
            {ed.groups[0]?.items.map((idea) => (
              <article className="scan-card" key={idea.label}>
                <div className="scan-card__head">
                  <span className="scan-card__class">{idea.label}</span>
                  <span className="scan-card__signal">{idea.value}</span>
                </div>
                <p className="scan-card__thesis">{idea.body}</p>
              </article>
            ))}
          </div>
          {/* Additional sections (e.g. the SF1-derived top equity opportunities + charts). */}
          {ed.groups.slice(1).map((g) => (
            <section className="news__section" key={g.heading}>
              <h3>{g.heading}</h3>
              {g.blurb ? <p className="news__blurb">{g.blurb}</p> : null}
              <ChartFigures charts={g.charts} />
              <ul className="news__rows">
                {g.items.map((it) => (
                  <li className="news__row" key={it.label}>
                    <div className="news__row-head">
                      <span className="news__metric">{it.label}</span>
                      <strong className="news__value">{it.value}</strong>
                    </div>
                    <p className="news__note">{it.body}</p>
                    {it.source ? <p className="news__source">{it.source}</p> : null}
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </>
      )}

      {ed.teaser ? <UpgradeGate /> : null}

      <section className="news__section news__methodology">
        <h3>Methodology &amp; sources</h3>
        <p className="news__source">{ed.methodology}</p>
      </section>

      <footer className="news__footer">
        <p>
          Prepared by JHI Research &amp; Analytics Firm, Inc. {ed.footer} As of{" "}
          {new Date(data.as_of).toLocaleString("en-US")}.
        </p>
        <p className="news__disclaimer">{ed.disclaimer}</p>
      </footer>
    </article>
  );
}
