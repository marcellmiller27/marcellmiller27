import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTypescript from "eslint-config-next/typescript";

export default defineConfig([
  ...nextVitals,
  ...nextTypescript,
  globalIgnores([
    ".next/**",
    "node_modules/**",
    "out/**",
    "next-env.d.ts",
    // Python virtualenv (may contain Playwright's bundled JS driver) — never our source.
    ".venv/**",
    "**/site-packages/**"
  ])
]);
