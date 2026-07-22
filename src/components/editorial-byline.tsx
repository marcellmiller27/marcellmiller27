// JHI-SIG: 69M2705M | Editorial byline (VP of Editorial) | JHI Research & Analytics Firm, Inc. (proprietary)
// Shared byline shown on every edition — the VP of Editorial's photo + attribution.

export function EditorialByline() {
  return (
    <p className="news__byline">
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img className="news__byline-avatar" src="/team/vp-editorial.png" alt="Ellery Vance" />
      <span>By Ellery Vance · VP of Editorial, JHI Research &amp; Analytics (AI)</span>
    </p>
  );
}
