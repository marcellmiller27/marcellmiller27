// JHI-SIG: 69M2705M | Newsletter methodology disclosure (E1) | JHI Research & Analytics Firm, Inc. (proprietary)
// Standard methodology block per docs/EDITORIAL_STYLE_GUIDE.md — kept identical to the
// backend PDF (newsletter_content.METHODOLOGY) so screen and PDF match verbatim.
export function NewsletterMethodology() {
  return (
    <section className="news__section news__methodology">
      <h3>Methodology &amp; sources</h3>
      <p className="news__source">
        This edition is generated deterministically from JHI&apos;s polled public-data feeds
        (Federal Reserve/FRED · U.S. Bureau of Labor Statistics · BEA · market feeds). Commentary is
        rule-based on disclosed thresholds; figures are shown as last released (see &ldquo;as
        of&rdquo;). It is an independent professional read, not a forecast or advice.
      </p>
    </section>
  );
}
