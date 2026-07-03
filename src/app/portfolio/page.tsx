import { LiveMarket } from "@/components/live-market";
import { LiveValuations } from "@/components/live-valuations";
import { PlatformShell } from "@/components/platform-shell";
import { portfolioHoldings } from "@/lib/platform-data";

const scenarioMetrics = [
  { label: "Bull case", value: "$18.4M", note: "15% annualized growth" },
  { label: "Base case", value: "$12.7M", note: "9% annualized growth" },
  { label: "Bear case", value: "$7.9M", note: "4% annualized growth" }
];

export default function PortfolioPage() {
  return (
    <PlatformShell
      eyebrow="Portfolio management"
      title="Track assets, cash flow, and wealth projection scenarios"
      description="Combine brokerage, banking, crypto, real estate, and private equity holdings into one portfolio operating system."
    >
      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Live holdings feed</p>
          <h2>Real-time prices across your asset classes</h2>
        </div>
        <LiveMarket symbols="BTC,ETH,SPX,GOLD,UST10Y,VNQ" />
      </section>

      <section className="app-section">
        <div className="app-section__heading">
          <p className="eyebrow">Live modeled valuations</p>
          <h2>Illiquid asset estimates from public inputs</h2>
        </div>
        <LiveValuations />
      </section>

      <section className="app-grid app-grid--four">
        {portfolioHoldings.map((holding) => (
          <article className="app-card" key={holding.name}>
            <span>{holding.assetClass}</span>
            <strong>{holding.allocation}</strong>
            <h3>{holding.name}</h3>
            <p>{holding.returnProfile}</p>
            <div className="cash-flow">{holding.cashFlow}</div>
          </article>
        ))}
      </section>

      <section className="app-section app-section--split">
        <div>
          <p className="eyebrow">Wealth projection engine</p>
          <h2>Scenario planning for family office growth</h2>
          <p>
            Model retirement outcomes, trust planning, generational wealth, liquidity events, and
            reinvestment strategies across bull, base, and bear cases.
          </p>
        </div>
        <div className="scenario-grid">
          {scenarioMetrics.map((scenario) => (
            <article key={scenario.label}>
              <span>{scenario.label}</span>
              <strong>{scenario.value}</strong>
              <p>{scenario.note}</p>
            </article>
          ))}
        </div>
      </section>
    </PlatformShell>
  );
}
