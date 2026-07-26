"use client";
// JHI-SIG: 69M2705M | Newsletter PDF download button | JHI Research & Analytics Firm, Inc. (proprietary)
import { useState } from "react";
import { downloadNewsletterPdf } from "@/lib/newsletter-format";

// Server-side PDF download — replaces the old window.print() button, which crashed
// the forwarded/desktop viewer.
export function NewsletterDownloadButton({ slug }: { slug: string }) {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);

  async function onClick() {
    setBusy(true);
    setError(false);
    try {
      await downloadNewsletterPdf(slug);
    } catch {
      setError(true);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="news__actions">
      <button
        type="button"
        className="button button--secondary"
        onClick={onClick}
        disabled={busy}
      >
        {busy ? "Preparing PDF…" : "Download PDF"}
      </button>
      {error ? (
        <span className="news__dl-error" role="alert">
          Couldn&apos;t generate the PDF. Please try again.
        </span>
      ) : null}
    </div>
  );
}
