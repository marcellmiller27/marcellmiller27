// JHI-SIG: 69M2705M | Current User Settings (language + visual mode) | JHI Research & Analytics Firm, Inc. (proprietary)
"use client";

import { useEffect, useRef, useState } from "react";
import { Settings as Gear } from "lucide-react";

type ThemeChoice = "system" | "light" | "dark";

const THEME_KEY = "aegira-theme";
const LANG_KEY = "aegira-lang";

// Browser default is English; content is English today, more languages added over time.
const LANGUAGES: { code: string; label: string }[] = [
  { code: "en", label: "English" },
  { code: "es", label: "Español" },
  { code: "fr", label: "Français" },
  { code: "de", label: "Deutsch" },
  { code: "pt", label: "Português" },
  { code: "zh", label: "中文" },
  { code: "ja", label: "日本語" }
];

function resolveTheme(choice: ThemeChoice): "light" | "dark" {
  if (choice === "dark") return "dark";
  if (choice === "light") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function applyTheme(choice: ThemeChoice): void {
  document.documentElement.dataset.theme = resolveTheme(choice);
}

const MODE_LABEL: Record<ThemeChoice, string> = {
  system: "Browser Default",
  light: "Light",
  dark: "Dark"
};

export function UserSettings() {
  const [open, setOpen] = useState(false);
  const [theme, setTheme] = useState<ThemeChoice>("system");
  const [lang, setLang] = useState("en");
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const savedTheme = (localStorage.getItem(THEME_KEY) as ThemeChoice) || "system";
    const savedLang = localStorage.getItem(LANG_KEY) || "en";
    // Client-only hydration from localStorage (not available during SSR).
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setTheme(savedTheme);
    setLang(savedLang);
    document.documentElement.lang = savedLang;
    // Keep "Browser Default" live if the OS theme changes while selected.
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => {
      if (((localStorage.getItem(THEME_KEY) as ThemeChoice) || "system") === "system") {
        applyTheme("system");
      }
    };
    mq.addEventListener("change", onChange);
    return () => mq.removeEventListener("change", onChange);
  }, []);

  useEffect(() => {
    if (!open) return;
    const onDoc = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", onDoc);
    return () => document.removeEventListener("mousedown", onDoc);
  }, [open]);

  const chooseTheme = (t: ThemeChoice) => {
    setTheme(t);
    localStorage.setItem(THEME_KEY, t);
    applyTheme(t);
  };

  const chooseLang = (l: string) => {
    setLang(l);
    localStorage.setItem(LANG_KEY, l);
    document.documentElement.lang = l;
  };

  return (
    <div className="user-settings" ref={ref}>
      <button
        type="button"
        className="user-settings__btn"
        aria-label="Settings"
        aria-haspopup="menu"
        aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
      >
        <Gear size={16} strokeWidth={2} aria-hidden />
      </button>
      {open && (
        <div className="user-settings__panel" role="menu">
          <p className="user-settings__title">Settings</p>

          <label className="user-settings__label" htmlFor="us-lang">
            Language
          </label>
          <select
            id="us-lang"
            name="language"
            className="user-settings__select"
            value={lang}
            onChange={(e) => chooseLang(e.target.value)}
          >
            {LANGUAGES.map((o) => (
              <option key={o.code} value={o.code}>
                {o.label}
              </option>
            ))}
          </select>
          <p className="user-settings__hint">Browser default is English. More languages coming.</p>

          <p className="user-settings__label">
            Visual mode <span className="user-settings__beta">beta</span>
          </p>
          <div className="user-settings__modes">
            {(["system", "light", "dark"] as ThemeChoice[]).map((t) => (
              <button
                key={t}
                type="button"
                className={`user-settings__mode${theme === t ? " is-active" : ""}`}
                onClick={() => chooseTheme(t)}
              >
                {MODE_LABEL[t]}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
