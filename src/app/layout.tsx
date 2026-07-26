import type { Metadata } from "next";
import type { ReactNode } from "react";
import { RoleProvider } from "@/components/role-provider";
import "./globals.css";

// Canonical/OG base for the owned company domain (johnhenrycapital.com). Overridable
// via NEXT_PUBLIC_SITE_URL for staging/preview. (Brand display copy is handled
// separately in the pending institutional copy pass.)
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://johnhenrycapital.com";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: "John Henry Investments Intelligence Platform",
  description:
    "Subscription investment intelligence platform for opportunity discovery, due diligence, macro research, and portfolio management.",
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url: "/",
    siteName: "JHI Research & Analytics Firm, Inc.",
    title: "John Henry Investments Intelligence Platform",
    description:
      "Institutional research and deal diligence — screening, valuation, Quality of Earnings, and multi-asset economic intelligence."
  }
};

export default function RootLayout({
  children
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <RoleProvider>{children}</RoleProvider>
      </body>
    </html>
  );
}
