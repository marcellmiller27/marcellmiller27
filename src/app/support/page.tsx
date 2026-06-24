"use client";

import { useEffect, useRef, useState } from "react";
import { PlatformShell } from "@/components/platform-shell";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type FaqItem = { id: string; category: string; question: string; answer: string };
type AskResponse = {
  answer: string;
  matched_question: string | null;
  category: string | null;
  confidence: number;
  escalate: boolean;
  suggestions: string[];
};
type ChatMessage = {
  role: "user" | "assistant";
  text: string;
  meta?: string;
  suggestions?: string[];
};

const GREETING: ChatMessage = {
  role: "assistant",
  text:
    "Hi! I'm the John Henry Investments assistant. Ask me about plans, sign-in and " +
    "security, market data, the mobile app, or crypto — or pick a question below.",
  suggestions: [
    "How much does it cost?",
    "Is the market data real-time?",
    "Do you store my crypto wallet private keys?",
    "How do I enable two-factor authentication?"
  ]
};

export default function SupportPage() {
  const [faqs, setFaqs] = useState<FaqItem[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>([GREETING]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/support/faq`)
      .then((response) => response.json())
      .then((data) => setFaqs(data.items ?? []))
      .catch(() => setFaqs([]));
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const ask = async (question: string) => {
    const trimmed = question.trim();
    if (!trimmed || busy) return;
    setMessages((prev) => [...prev, { role: "user", text: trimmed }]);
    setInput("");
    setBusy(true);
    try {
      const response = await fetch(`${API_BASE}/support/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed })
      });
      const data: AskResponse = await response.json();
      const meta = data.escalate
        ? "Not confident · escalate to a human"
        : `${data.category ?? "Answer"} · confidence ${(data.confidence * 100).toFixed(0)}%`;
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.answer, meta, suggestions: data.suggestions }
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "I couldn't reach the support service. Please try again in a moment.",
          meta: "Connection error"
        }
      ]);
    } finally {
      setBusy(false);
    }
  };

  const categories = Array.from(new Set(faqs.map((item) => item.category)));

  return (
    <PlatformShell
      eyebrow="Help center"
      title="Support & frequently asked questions"
      description="Ask the AI assistant a question, or browse common answers about plans, security, market data, and the mobile app."
    >
      <section className="assistant-panel" aria-label="Support assistant">
        <div className="assistant-panel__sidebar">
          <p className="eyebrow">Assistant</p>
          <h2 style={{ fontSize: "1.4rem", margin: "0.4rem 0 0.6rem" }}>Ask us anything</h2>
          <p>
            Answers are drawn from our help knowledge base. For anything else, the
            assistant will point you to a human.
          </p>
          <div className="output-tags">
            {(GREETING.suggestions ?? []).map((q) => (
              <button
                type="button"
                className="tag"
                key={q}
                onClick={() => ask(q)}
                style={{ cursor: "pointer", border: "1px solid var(--border)", background: "transparent", color: "inherit", font: "inherit" }}
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        <div>
          <div className="chat-stack">
            {messages.map((message, index) => (
              <div className="chat-card" key={index}>
                {message.role === "user" ? (
                  <div className="chat-card__prompt">{message.text}</div>
                ) : (
                  <div className="chat-card__response">
                    {message.meta ? <p className="support-meta">{message.meta}</p> : null}
                    <p style={{ margin: 0 }}>{message.text}</p>
                    {message.suggestions && message.suggestions.length > 0 ? (
                      <div className="output-tags" style={{ marginTop: "0.75rem" }}>
                        {message.suggestions.map((s) => (
                          <button
                            type="button"
                            className="tag"
                            key={s}
                            onClick={() => ask(s)}
                            style={{ cursor: "pointer", border: "1px solid var(--border)", background: "transparent", color: "inherit", font: "inherit" }}
                          >
                            {s}
                          </button>
                        ))}
                      </div>
                    ) : null}
                  </div>
                )}
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          <form
            className="support-form"
            onSubmit={(event) => {
              event.preventDefault();
              ask(input);
            }}
          >
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Type your question…"
              aria-label="Your question"
            />
            <button type="submit" disabled={busy || !input.trim()}>
              {busy ? "…" : "Ask"}
            </button>
          </form>
        </div>
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Knowledge base</p>
          <h2>Frequently asked questions</h2>
        </div>
        {categories.map((category) => (
          <div key={category} style={{ marginTop: "1.5rem" }}>
            <p className="eyebrow">{category}</p>
            <div className="app-grid app-grid--two">
              {faqs
                .filter((item) => item.category === category)
                .map((item) => (
                  <article className="app-card" key={item.id}>
                    <h3 style={{ margin: "0 0 0.5rem" }}>{item.question}</h3>
                    <p>{item.answer}</p>
                    <button
                      type="button"
                      className="m-link"
                      onClick={() => ask(item.question)}
                      style={{ marginTop: "0.5rem", color: "var(--growth)", background: "none", border: 0, cursor: "pointer", font: "inherit", fontWeight: 800, padding: 0 }}
                    >
                      Ask the assistant →
                    </button>
                  </article>
                ))}
            </div>
          </div>
        ))}
      </section>
    </PlatformShell>
  );
}
