// JHI-SIG: 69M2705M | Global site footer (site-wide utility) | JHI Research & Analytics Firm, Inc. (proprietary)
import Link from "next/link";

// Persistent, site-wide utility footer — the institutional counterpart to the
// per-module "Where to next" CTA block (src/components/module-footer.tsx). This
// one renders once, at the bottom of EVERY page, from the root layout. Grouped
// utility links (monochrome, dense, low-key) in the spirit of Bloomberg,
// PitchBook, ARK Invest, Mergr, and 42Macro. Only routes that exist (or are
// created in this PR) are linked.
type FooterLink = { href: string; label: string };
type FooterGroup = { heading: string; links: FooterLink[] };

const GROUPS: FooterGroup[] = [
  {
    heading: "Company",
    links: [
      { href: "/about", label: "About" },
      { href: "/team", label: "Team" },
      { href: "/contact", label: "Contact" }
    ]
  },
  {
    heading: "Product",
    links: [
      { href: "/pricing", label: "Pricing" },
      { href: "/newsletters", label: "Newsletters" },
      { href: "/framework", label: "Framework" }
    ]
  },
  {
    heading: "Support",
    links: [
      { href: "/help", label: "Help" },
      { href: "/support", label: "Support" },
      { href: "/contact", label: "Contact" }
    ]
  },
  {
    heading: "Legal",
    links: [
      { href: "/privacy", label: "Privacy" },
      { href: "/terms", label: "Terms" },
      { href: "/legal", label: "Legal & Disclosures" }
    ]
  }
];

export function SiteFooter() {
  const year = new Date().getFullYear();
  return (
    <footer className="site-footer" aria-label="Site footer">
      <div className="site-footer__inner">
        <div className="site-footer__brand">
          <p className="site-footer__wordmark">Aegira</p>
          <p className="site-footer__tagline">
            Institutional-grade market, economic, and deal intelligence — for the
            independent investor and acquirer.
          </p>
        </div>
        <nav className="site-footer__nav" aria-label="Footer navigation">
          {GROUPS.map((group) => (
            <div className="site-footer__group" key={group.heading}>
              <p className="site-footer__heading">{group.heading}</p>
              <ul>
                {group.links.map((link) => (
                  <li key={`${group.heading}-${link.href}-${link.label}`}>
                    <Link href={link.href}>{link.label}</Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </nav>
      </div>
      <div className="site-footer__legal">
        <p className="site-footer__copyright">
          © {year} Aegira — a product of JHI Research &amp; Analytics Firm, Inc.
        </p>
        <p className="site-footer__disclaimer">
          Research and analytics are informational only and are not investment
          advice, a recommendation, or an offer to buy or sell any security.
        </p>
        <p className="site-footer__sig">JHI-SIG: 69M2705M</p>
      </div>
    </footer>
  );
}
