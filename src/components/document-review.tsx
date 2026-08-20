"use client";
// JHI-SIG: 69M2705M | Document Review (operational upload client) | JHI Research & Analytics Firm, Inc. (proprietary)
// Each of the four intake cards opens a real file picker and POSTs the file + doc_type
// to the auth-gated backend (POST /api/v1/document-review/upload) via apiFetch, which
// forwards the auth token as a Bearer header. The queue below is LIVE — it is fetched
// from GET /document-review/queue (the caller's own persisted, risk-scored reviews).

import { useCallback, useEffect, useRef, useState } from "react";
import { apiFetch } from "@/lib/api";

type Review = {
  id: string;
  doc_type: string;
  doc_type_label: string;
  filename: string;
  content_type: string;
  size_bytes: number;
  uploaded_by: string;
  status: "analyzed" | "manual_review_required";
  risk_score: number | null;
  risk_band: string;
  summary: string;
  flags: string[];
  questions: string[];
  disclaimer: string;
  uploaded_at: string;
};

type UploadCard = { docType: string; label: string };

const UPLOAD_CARDS: UploadCard[] = [
  { docType: "tax_returns", label: "Tax returns" },
  { docType: "pnl", label: "P&L statements" },
  { docType: "balance_sheet", label: "Balance sheets" },
  { docType: "bank_statements", label: "Bank statements" }
];

const ACCEPT = ".pdf,.csv,.xlsx";

function riskClass(band: string): string {
  const b = band.toLowerCase();
  if (b === "high" || b === "medium" || b === "low") return `risk risk--${b}`;
  return "risk";
}

function statusLabel(r: Review): string {
  if (r.status === "manual_review_required") return "Manual review required";
  return "Analyzed";
}

export function DocumentReview() {
  const [queue, setQueue] = useState<Review[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string>("");
  const [notice, setNotice] = useState<string>("");
  const inputs = useRef<Record<string, HTMLInputElement | null>>({});

  const loadQueue = useCallback(async () => {
    // `loading` starts true; we intentionally do NOT flip it back to true on refresh
    // (avoids a synchronous setState in the mount effect and keeps refreshes seamless).
    try {
      const res = await apiFetch("/document-review/queue");
      if (res.status === 401 || res.status === 403) {
        setError("Sign in with a subscriber account to review documents.");
        setQueue([]);
        return;
      }
      if (!res.ok) throw new Error(`Could not load the queue (HTTP ${res.status}).`);
      setQueue((await res.json()) as Review[]);
      setError("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not reach the document service.");
      setQueue([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // loadQueue only sets state after an awaited fetch resolves (never synchronously);
    // the lint heuristic can't see through the async boundary. Same pattern as role-provider.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void loadQueue();
  }, [loadQueue]);

  async function upload(card: UploadCard, file: File) {
    setError("");
    setNotice("");
    setBusy(card.docType);
    try {
      const form = new FormData();
      form.append("doc_type", card.docType);
      form.append("file", file);
      const res = await apiFetch("/document-review/upload", { method: "POST", body: form });
      if (!res.ok) {
        let detail = `Upload failed (HTTP ${res.status}).`;
        if (res.status === 401 || res.status === 403) {
          detail = "You must be signed in as a subscriber to upload documents.";
        } else if (res.status === 415) {
          detail = "Unsupported file type. Upload a PDF, CSV, or XLSX.";
        } else if (res.status === 413) {
          detail = "That file is too large (25 MB limit).";
        } else {
          try {
            const body = await res.json();
            if (body?.detail) detail = String(body.detail);
          } catch {
            /* keep default */
          }
        }
        setError(detail);
        return;
      }
      const review = (await res.json()) as Review;
      const scoreText =
        review.risk_score === null
          ? "routed for manual review"
          : `risk ${review.risk_score}/100 (${review.risk_band})`;
      setNotice(`Analyzed “${review.filename}” → ${scoreText}.`);
      await loadQueue();
    } catch {
      setError("Could not reach the document service.");
    } finally {
      setBusy(null);
    }
  }

  function onPick(card: UploadCard, event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    // Reset so re-uploading the same file fires onChange again.
    event.target.value = "";
    if (file) void upload(card, file);
  }

  return (
    <div>
      <section className="app-section app-section--split">
        <div>
          <p className="eyebrow">Document intake</p>
          <h2>Financial upload workflow</h2>
          <p>
            Click a card to upload a real financial document (PDF, CSV, or XLSX). The file is stored
            securely off the public web, extracted, and scored for risk — then it appears in your live
            diligence queue below with flags and generated diligence questions.
          </p>
          {notice ? (
            <p style={{ color: "var(--growth, #1f7a4d)", fontWeight: 700, marginTop: "0.6rem" }}>
              {notice}
            </p>
          ) : null}
          {error ? (
            <p style={{ color: "var(--severity, #c0392b)", fontWeight: 700, marginTop: "0.6rem" }}>
              {error}
            </p>
          ) : null}
        </div>
        <div className="upload-grid">
          {UPLOAD_CARDS.map((card) => {
            const uploading = busy === card.docType;
            return (
              <article
                key={card.docType}
                role="button"
                tabIndex={0}
                aria-label={`Upload ${card.label}`}
                aria-busy={uploading}
                onClick={() => !busy && inputs.current[card.docType]?.click()}
                onKeyDown={(e) => {
                  if ((e.key === "Enter" || e.key === " ") && !busy) {
                    e.preventDefault();
                    inputs.current[card.docType]?.click();
                  }
                }}
                style={{ cursor: busy ? "wait" : "pointer", position: "relative" }}
              >
                <span>{uploading ? "Uploading…" : "Upload"}</span>
                <strong>{card.label}</strong>
                <input
                  ref={(el) => {
                    inputs.current[card.docType] = el;
                  }}
                  type="file"
                  accept={ACCEPT}
                  onChange={(e) => onPick(card, e)}
                  style={{ display: "none" }}
                />
                {uploading ? (
                  <div
                    aria-hidden
                    style={{
                      position: "absolute",
                      left: 0,
                      right: 0,
                      bottom: 0,
                      height: 3,
                      overflow: "hidden",
                      background: "rgba(15,31,51,0.08)"
                    }}
                  >
                    <div
                      style={{
                        height: "100%",
                        width: "40%",
                        background: "var(--growth, #1f7a4d)",
                        animation: "docreview-progress 1s linear infinite"
                      }}
                    />
                  </div>
                ) : null}
              </article>
            );
          })}
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Diligence queue</p>
          <h2>Automated analysis results</h2>
        </div>

        {loading ? (
          <p className="live-market__muted">Loading your reviews…</p>
        ) : queue && queue.length > 0 ? (
          <div className="table-card">
            {queue.map((item) => (
              <article className="table-row" key={item.id} style={{ alignItems: "flex-start" }}>
                <div style={{ minWidth: 220 }}>
                  <span>{statusLabel(item)}</span>
                  <strong>{item.doc_type_label}</strong>
                  <p style={{ fontSize: "var(--fs-sm)", color: "var(--muted)", margin: "0.2rem 0 0" }}>
                    {item.filename}
                  </p>
                </div>
                <div style={{ flex: 1 }}>
                  <p style={{ margin: 0 }}>{item.summary}</p>
                  {item.flags.length ? (
                    <ul style={{ margin: "0.5rem 0 0", paddingLeft: "1.1rem" }}>
                      {item.flags.slice(0, 3).map((flag) => (
                        <li key={flag} style={{ fontSize: "var(--fs-sm)" }}>
                          {flag}
                        </li>
                      ))}
                    </ul>
                  ) : null}
                  {item.questions.length ? (
                    <details style={{ marginTop: "0.5rem" }}>
                      <summary style={{ cursor: "pointer", fontWeight: 700, fontSize: "var(--fs-sm)" }}>
                        {item.questions.length} diligence question
                        {item.questions.length === 1 ? "" : "s"}
                      </summary>
                      <ol style={{ margin: "0.4rem 0 0", paddingLeft: "1.2rem" }}>
                        {item.questions.map((q) => (
                          <li key={q} style={{ fontSize: "var(--fs-sm)" }}>
                            {q}
                          </li>
                        ))}
                      </ol>
                    </details>
                  ) : null}
                </div>
                <div className={riskClass(item.risk_band)}>
                  {item.risk_score === null
                    ? "Manual review"
                    : `${item.risk_band} risk · ${item.risk_score}/100`}
                </div>
              </article>
            ))}
          </div>
        ) : (
          <div className="table-card">
            <article className="table-row">
              <div>
                <span>Empty</span>
                <strong>No documents yet — upload to begin</strong>
              </div>
              <p>
                Upload tax returns, P&amp;L statements, balance sheets, or bank statements above. Each
                document is analyzed and appears here with a risk score, flags, and diligence questions.
              </p>
              <div className="risk risk--low">Awaiting upload</div>
            </article>
          </div>
        )}
      </section>

      <style jsx>{`
        @keyframes docreview-progress {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(350%);
          }
        }
      `}</style>
    </div>
  );
}
