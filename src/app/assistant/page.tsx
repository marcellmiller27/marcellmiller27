import { LiveAssistant } from "@/components/live-assistant";
import { PlatformShell } from "@/components/platform-shell";
import { assistantWorkflows } from "@/lib/platform-data";

export default function AssistantPage() {
  return (
    <PlatformShell
      eyebrow="AI research assistant"
      title="Private investment analyst for research and acquisition review"
      description="Ask questions about securities, SBA loans, business targets, Bitcoin cycles, dividend portfolios, and portfolio risk."
    >
      <section className="assistant-panel">
        <div className="assistant-panel__sidebar">
          <p className="eyebrow">Live assistant</p>
          <h2>Ask the AI research team</h2>
          <p>
            Questions are routed to the right specialist (product, market data, security,
            billing) and technical issues escalate to the founder as a tracked ticket.
          </p>
        </div>
        <LiveAssistant />
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Sample prompts</p>
          <h2>Research workflows</h2>
        </div>
        <div className="chat-stack">
          {assistantWorkflows.map((workflow) => (
            <article className="chat-card" key={workflow.prompt}>
              <div className="chat-card__prompt">{workflow.prompt}</div>
              <div className="chat-card__response">
                <p>{workflow.response}</p>
                <div className="output-tags">
                  {workflow.outputs.map((output) => (
                    <span key={output}>{output}</span>
                  ))}
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>
    </PlatformShell>
  );
}
