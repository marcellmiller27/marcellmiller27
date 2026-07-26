// JHI-SIG: 69M2705M | Logout control | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useRouter } from "next/navigation";
import { useRole } from "@/components/role-provider";
import { clearCookie, TOKEN_COOKIE } from "@/lib/auth";

export function LogoutButton() {
  const router = useRouter();
  const { setRole } = useRole();
  return (
    <button
      type="button"
      className="button button--secondary"
      onClick={() => {
        clearCookie(TOKEN_COOKIE);
        setRole("public");
        router.push("/login");
        router.refresh();
      }}
    >
      Sign out
    </button>
  );
}
