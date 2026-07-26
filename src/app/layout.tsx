import type { Metadata } from "next";
import type { ReactNode } from "react";
import { RoleProvider } from "@/components/role-provider";
import "./globals.css";

// Canonical/OG base for the Aegira platform domain. Overridable via NEXT_PUBLIC_SITE_URL
// for staging/preview. (Aegira = platform brand; JHI Research & Analytics Firm, Inc. =
// corporate publisher.)
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://aegira.com";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: "Aegira — Institutional Intelligence for Global Markets",
  description:
    "Aegira is an institutional intelligence platform for economic research, multi-asset markets, opportunity discovery, and deal diligence. Published by JHI Research & Analytics Firm, Inc.",
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    url: "/",
    siteName: "Aegira",
    title: "Aegira — Institutional Intelligence for Global Markets",
    description:
      "Institutional research and deal diligence — screening, valuation, Quality of Earnings, and multi-asset economic intelligence. Published by JHI Research & Analytics Firm, Inc."
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
