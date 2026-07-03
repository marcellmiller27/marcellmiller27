"use client";

import { useEffect, useRef, useState } from "react";

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

type AgentReply = {
  agent_name: string;
  agent_role: string;
  answer: string;
  escalated: boolean;
  ticket_id: string | null;
  suggestions: string[];
};
type Msg = { role: "user" | "assistant"; text: string; meta?: string; suggestions?: string[] };

const GREETING: Msg = {
  role: "assistant",
  text:
    "I'm your JHI research assistant. Ask about the Opportunity Score, live market data, " +
    "an acquisition target, or how a platform feature works — I'll route you to the right specialist.",
  suggestions: [
    "How does the Opportunity Score work?",
    "Is the market data real-time?",
    "How do I analyze an SBA acquisition?",
    "What plans are available?"
  ]
};

export function LiveAssistant() {
  const [messages, setMessages] = useState<Msg[]>([GREETING]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const ask = async (question: string) => {
    const trimmed = question.trim();
    if (!trimmed || busy) return;
    setMessages((prev) => [...prev, { role: "user", text: trimmed }]);
    setInput("");
    setBusy(true);
    try {
      const response = await fetch(`${API_BASE}/agents/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed })
      });
      if (!response.ok) throw new Error(String(response.status));
      const data: AgentReply = await response.json();
      const meta = data.escalated
        ? `${data.agent_name} · forwarded to the founder${
            data.ticket_id ? ` · ticket ${data.ticket_id.slice(0, 8)}` : ""
          }`
        : `${data.agent_name} · ${data.agent_role}`;
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.answer, meta, suggestions: data.suggestions }
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "I couldn't reach the assistant service. Please try again shortly.",
          meta: "Connection error"
        }
      ]);
    } finally {
      setBusy(false);
    }
  };

  return (
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
        <div ref={endRef} />
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
          placeholder="Ask the research assistant…"
          aria-label="Your question"
        />
        <button type="submit" disabled={busy || !input.trim()}>
          {busy ? "…" : "Ask"}
        </button>
      </form>
    </div>
  );
}
