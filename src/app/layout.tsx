import type { Metadata } from "next";
import type { ReactNode } from "react";
import { RoleProvider } from "@/components/role-provider";
import "./globals.css";

// Canonical/OG base for the Aegira platform domain. Overridable via NEXT_PUBLIC_SITE_URL
// for staging/preview. (Aegira = platform brand; JHI Research & Analytics Firm, Inc. =
// corporate publisher.)
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://aegiraenterprise.com";

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
  // Pre-paint: apply the saved Visual Mode + language before first paint (no flash).
  // "Browser Default" resolves prefers-color-scheme. suppressHydrationWarning because we
  // mutate <html> before React hydrates.
  const themeInit = `(function(){try{var t=localStorage.getItem('aegira-theme')||'system';var d=t==='dark'||(t==='system'&&window.matchMedia('(prefers-color-scheme: dark)').matches);document.documentElement.dataset.theme=d?'dark':'light';var l=localStorage.getItem('aegira-lang');if(l){document.documentElement.lang=l;}}catch(e){}})();`;
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
        <RoleProvider>{children}</RoleProvider>
      </body>
    </html>
  );
}
