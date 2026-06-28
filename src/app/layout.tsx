// JHI-SIG: 69M2705M | Frontend shell | John Henry Investments (proprietary)
import type { Metadata } from "next";
import type { ReactNode } from "react";
import "./globals.css";

export const metadata: Metadata = {
  title: "John Henry Investments Intelligence Platform",
  description:
    "Subscription investment intelligence platform for opportunity discovery, due diligence, macro research, and portfolio management."
};

export default function RootLayout({
  children
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
