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
type Group = { heading: string; blurb: string; items: Item[] };
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
};
type Payload = { edition: Edition; as_of: string; editorial: string };
type Variant = "brief" | "alerts" | "scan";

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
        <p className="eyebrow">JHI Research &amp; Analytics · {ed.eyebrow}</p>
        <h2>{ed.title}</h2>
        <p className="news__edition">{ed.dateline}</p>
        <EditorialByline />
      </header>

      {ed.intro ? (
        <section className="news__lede">
          {variant === "brief" ? <h3>Executive summary</h3> : null}
          <p>{ed.intro}</p>
        </section>
      ) : null}

      {variant === "brief" && ed.groups.map((g) => (
        <section className="news__section" key={g.heading}>
          <h3>{g.heading}</h3>
          {g.blurb ? <p className="news__blurb">{g.blurb}</p> : null}
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
