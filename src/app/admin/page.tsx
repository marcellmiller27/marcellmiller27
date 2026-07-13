// JHI-SIG: 69M2705M | Admin (System Administrator) page | John Henry Investments (proprietary)
import { AdminConsole } from "@/components/admin-console";
import { PlatformShell } from "@/components/platform-shell";

export default function AdminPage() {
  return (
    <PlatformShell
      eyebrow="System administration"
      title="Admin — the platform gatekeeper"
      description="Grant and revoke access, manage users and roles, and review the audit trail. Restricted to platform administrators; every change is logged."
    >
      <AdminConsole />
    </PlatformShell>
  );
}
