"use client";
// JHI-SIG: 69M2705M | Newsletter edition renderer (backend-sourced) | JHI Research & Analytics Firm, Inc. (proprietary)
// Renders an edition from the backend content API (deterministic build + E2 LLM
// elevation, fact-locked). Single source of truth for on-screen, the PDF (which
// prints this page), and future email. Per-variant styling preserves each edition's look.
import Link from "next/link";
import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { EditorialByline } from "@/components/editorial-byline";
import { NewsletterDownloadButton } from "@/components/newsletter-download-button";
import { UpgradeGate } from "@/components/upgrade-gate";
import { useRole } from "@/components/role-provider";
import { canFullNewsletter } from "@/lib/roles";

type Item = {
  label: string;
  value: string;
  body: string;
  tags: string[];
  source: string | null;
  as_of_label?: string | null;
};
type Chart = { label: string; image: string; caption: string; source: string | null };
type Group = { heading: string; blurb: string; items: Item[]; charts?: Chart[] };
type PersonaPath = { label: string; blurb: string; href: string; gated?: boolean };
type CTA = { label: string; href: string };
type EditorLetter = {
  greeting: string;
  narrative: string;
  questions: string[];
  philosophy: string;
  persona_paths: PersonaPath[];
  cta: CTA | null;
};
type Hero = {
  wordmark: string;
  dateline: string;
  byline: string;
  thesis: string;
  regime_label: string | null;
  regime_caption: string | null;
  as_of: string | null;
  variant: string;
};
type VisualLayer = { hero: Hero | null; charts: Chart[] };
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
  editor_letter?: EditorLetter | null;
  visual_layer?: VisualLayer | null;
};
type Payload = { edition: Edition; as_of: string; editorial: string };
type Variant = "brief" | "alerts" | "scan" | "insider" | "acquirer";

// Sectioned editions (thesis/summary + analytical sections + items) share one layout.
const SECTIONED: Variant[] = ["brief", "insider"];

// The Main Street Acquirer is a distinct *deal/opportunity letter* — not the Economic
// Brief. Its signature sections get a dedicated "kind" so each renders with its own
// accent, kicker, and card treatment (see `.news--acquirer` / `.acq-*` in globals.css).
type AcquirerSection = { kind: string; kicker: string };
function acquirerSection(heading: string): AcquirerSection {
  const h = heading.toLowerCase();
  if (h.startsWith("sba")) return { kind: "sba", kicker: "Lending Intelligence" };
  if (h.includes("industry spotlight")) return { kind: "spotlight", kicker: "Industry Spotlight" };
  if (h.startsWith("acquisition playbook")) return { kind: "playbook", kicker: "The Playbook" };
  if (h.startsWith("deal teardown")) return { kind: "teardown", kicker: "Deal Teardown" };
  if (h.startsWith("financing corner")) return { kind: "financing", kicker: "Financing Corner" };
  if (h.startsWith("metric of the issue")) return { kind: "metric", kicker: "Metric of the Issue" };
  return { kind: "default", kicker: "" };
}

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

// The per-edition HERO masthead — a deterministic, typographic (NOT AI-image) band that
// LEADS the visual layer at the very top of the edition. It carries the edition wordmark,
// dateline + byline, a one-line thesis (reused from the editor's letter), the current
// macro-REGIME BADGE (from the Regime Quadrant), and the as-of timestamp. Rendered in
// HTML/CSS so it is crisp on screen and in the printed PDF (which prints this page).
function EditionHero({ hero }: { hero: Hero }) {
  const light = hero.variant === "light";
  return (
    <header className={`edition-hero${light ? " edition-hero--light" : ""}`} aria-label="Edition hero">
      <div className="edition-hero__top">
        <p className="edition-hero__wordmark">{hero.wordmark}</p>
        {hero.regime_label ? (
          <span className="edition-hero__regime" title={hero.regime_caption ?? undefined}>
            <span className="edition-hero__regime-eyebrow">Macro Regime</span>
            <span className="edition-hero__regime-label">{hero.regime_label}</span>
            {hero.regime_caption ? (
              <span className="edition-hero__regime-caption">{hero.regime_caption}</span>
            ) : null}
          </span>
        ) : null}
      </div>
      {hero.thesis ? <p className="edition-hero__thesis">{hero.thesis}</p> : null}
      <p className="edition-hero__meta">
        <span>{hero.dateline}</span>
        <span aria-hidden> · </span>
        <span>{hero.byline}</span>
        {hero.as_of ? (
          <>
            <span aria-hidden> · </span>
            <span className="edition-hero__asof">As of {hero.as_of}</span>
          </>
        ) : null}
      </p>
    </header>
  );
}

// The 42Macro-style editor's letter (a.k.a. lede). An ENHANCEMENT layer that LEADS the
// edition — the greeting, consensus-challenging narrative, three italic teaser questions,
// a "process over prediction" philosophy line, two persona-routing paths, and one CTA.
// It renders ABOVE the existing groups/charts, which are unchanged. Both persona paths
// show for everyone; the gated "Act on the Signals" path adds a subtle upgrade nudge for
// non-subscribers rather than hiding it.
function EditorLetter({ letter }: { letter: EditorLetter }) {
  const { role } = useRole();
  const isSubscriber = canFullNewsletter(role);
  return (
    <section className="editor-letter" aria-label="Editor's letter">
      {letter.greeting ? <p className="editor-letter__greeting">{letter.greeting}</p> : null}
      {letter.narrative ? <p className="editor-letter__narrative">{letter.narrative}</p> : null}
      {letter.questions && letter.questions.length > 0 ? (
        <ul className="editor-letter__questions">
          {letter.questions.map((q) => (
            <li key={q}>{q}</li>
          ))}
        </ul>
      ) : null}
      {letter.philosophy ? <p className="editor-letter__philosophy">{letter.philosophy}</p> : null}
      {letter.persona_paths && letter.persona_paths.length > 0 ? (
        <div className="editor-letter__paths">
          {letter.persona_paths.map((p) => {
            const showNudge = Boolean(p.gated) && !isSubscriber;
            return (
              <Link className="editor-letter__path" href={p.href} key={p.label}>
                <span className="editor-letter__path-head">
                  <span className="editor-letter__path-label">{p.label}</span>
                  {showNudge ? (
                    <span className="editor-letter__nudge">Subscriber · upgrade to unlock</span>
                  ) : null}
                </span>
                <span className="editor-letter__path-blurb">{p.blurb}</span>
              </Link>
            );
          })}
        </div>
      ) : null}
      {letter.cta ? (
        <Link className="button button--primary editor-letter__cta" href={letter.cta.href}>
          {letter.cta.label} <span aria-hidden>→</span>
        </Link>
      ) : null}
    </section>
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
  const isAcquirer = variant === "acquirer";

  return (
    <article className={isAcquirer ? "news news--acquirer" : "news"}>
      <NewsletterDownloadButton slug={slug} />

      <header className="news__masthead">
        {isAcquirer ? <p className="acq-badge">Deal &amp; Opportunity Letter</p> : null}
        <p className="eyebrow">Aegira · {ed.eyebrow}</p>
        <h2>{ed.title}</h2>
        <p className="news__edition">{ed.dateline}</p>
        {isAcquirer ? (
          <p className="acq-tagline">For SMB, search-fund &amp; ETA buyers · SBA · DSCR · deal teardowns</p>
        ) : null}
        <EditorialByline />
      </header>

      {/* The additive VISUAL LAYER leads the edition: the typographic hero at the top, then
          the editor's letter, then the regime quadrant + signal heat map — all ABOVE the
          existing executive summary, groups, charts, tables and data (unchanged below). */}
      {ed.visual_layer?.hero ? <EditionHero hero={ed.visual_layer.hero} /> : null}

      {/* The editor's letter LEADS the edition (additive enhancement layer). The existing
          executive summary, groups, charts, tables and data all render unchanged below. */}
      {ed.editor_letter ? <EditorLetter letter={ed.editor_letter} /> : null}

      {/* Regime Quadrant + Signal Heat Map — the visual-layer exhibits, above the body. */}
      {ed.visual_layer?.charts && ed.visual_layer.charts.length > 0 ? (
        <div className="news__visual-exhibits">
          <ChartFigures charts={ed.visual_layer.charts} />
        </div>
      ) : null}

      {ed.intro ? (
        <section className="news__lede" id="news-summary">
          {SECTIONED.includes(variant) || isAcquirer ? (
            <h3>
              {variant === "insider"
                ? "Thesis"
                : isAcquirer
                  ? "The acquirer's read"
                  : "Executive summary"}
            </h3>
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
                {it.as_of_label ? <p className="news__asof">{it.as_of_label}</p> : null}
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
                    {it.as_of_label ? <p className="news__asof">{it.as_of_label}</p> : null}
                    <p className="news__note">{it.body}</p>
                    {it.source ? <p className="news__source">{it.source}</p> : null}
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </>
      )}

      {isAcquirer && ed.groups.map((g) => {
        const { kind, kicker } = acquirerSection(g.heading);
        return (
          <section className={`acq-section acq-section--${kind}`} key={g.heading}>
            <div className="acq-section__bar" aria-hidden />
            <div className="acq-section__body">
              {kicker ? <p className="acq-section__kicker">{kicker}</p> : null}
              <h3 className="acq-section__title">{g.heading}</h3>
              {g.blurb ? <p className="news__blurb">{g.blurb}</p> : null}
              <ChartFigures charts={g.charts} />
              <ul className="acq-rows">
                {g.items.map((it) => (
                  <li className="acq-row" key={it.label}>
                    <div className="acq-row__head">
                      <span className="acq-row__label">{it.label}</span>
                      {it.value ? <strong className="acq-row__value">{it.value}</strong> : null}
                    </div>
                    {it.as_of_label ? <p className="news__asof">{it.as_of_label}</p> : null}
                    <p className="acq-row__note">{it.body}</p>
                    {it.tags && it.tags.length > 0 ? (
                      <div className="output-tags">
                        {it.tags.map((t) => (
                          <span className="tag" key={t}>{t}</span>
                        ))}
                      </div>
                    ) : null}
                    {it.source ? <p className="news__source">{it.source}</p> : null}
                  </li>
                ))}
              </ul>
            </div>
          </section>
        );
      })}

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
