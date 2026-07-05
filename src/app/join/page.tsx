import Link from "next/link";
import { Logo } from "@/components/logo";
import { WaitlistForm } from "@/components/waitlist-form";

const POINTS = [
  "Institutional-grade research & the John Henry Opportunity Score",
  "Live multi-asset market data — crypto, equities, FX, rates, and more",
  "AI due diligence, portfolio tracking, and a 24/7 AI assistant"
];

export default function JoinPage() {
  return (
    <main className="join">
      <Link className="join__brand" href="/">
        <Logo size={40} />
        John Henry Investments
      </Link>
      <p className="eyebrow">Early access</p>
      <h1 className="join__title">Invest with institutional intelligence.</h1>
      <p className="join__lead">
        Join the waitlist for early access to the John Henry Investments platform —
        built to put institutional-grade research and modern technology in the hands of
        everyday investors.
      </p>
      <ul className="join__points">
        {POINTS.map((point) => (
          <li key={point}>{point}</li>
        ))}
      </ul>
      <div className="join__form">
        <WaitlistForm source="join" />
      </div>
      <p className="join__back">
        <Link href="/">← Back to overview</Link>
      </p>
    </main>
  );
}
