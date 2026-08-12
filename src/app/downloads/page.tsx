// JHI-SIG: 69M2705M | Firm Documents / Downloads (staff-only) | JHI Research & Analytics Firm, Inc. (proprietary)
// Server-side STAFF gate. Middleware (src/proxy.ts) only proves a login token is present;
// it cannot tell staff from a subscriber. So this page (a server component) verifies
// staff via the backend `/auth/me` `is_staff` flag and redirects non-staff away before
// any confidential document metadata is rendered. The files themselves are streamed by a
// separate staff-gated backend endpoint (see src/components/firm-documents.tsx).
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { AppShell } from "@/components/app-shell";
import { FirmDocuments } from "@/components/firm-documents";
import { TOKEN_COOKIE } from "@/lib/auth";

export const dynamic = "force-dynamic";

// Server-side calls hit the backend directly (the same-origin /api/v1 rewrite target).
const BACKEND_BASE = process.env.API_PROXY_TARGET || "http://localhost:8000";

async function isStaffRequest(token: string): Promise<boolean> {
  try {
    const res = await fetch(`${BACKEND_BASE}/api/v1/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store"
    });
    if (!res.ok) return false;
    const me = await res.json();
    return Boolean(me?.is_staff);
  } catch {
    return false;
  }
}

export default async function DownloadsPage() {
  const token = (await cookies()).get(TOKEN_COOKIE)?.value;
  if (!token) {
    redirect("/login?next=/downloads");
  }
  const staff = await isStaffRequest(token);
  if (!staff) {
    // Non-staff (subscribers, free) are not authorized for the firm's internal documents.
    redirect("/home");
  }

  return (
    <AppShell
      eyebrow="Firm operations"
      title="Documents"
      description="Confidential firm models and reports — staff only. Files open in Excel / Numbers / Google Sheets (.xlsx) or Word / Pages / Google Docs (.docx)."
    >
      <FirmDocuments />
    </AppShell>
  );
}
