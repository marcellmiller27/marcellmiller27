// JHI-SIG: 69M2705M | Canonical price formatter tests | JHI Research & Analytics Firm, Inc. (proprietary)
// Acceptance + boundary tests for the canonical frontend price formatter. Runs on the
// Node built-in test runner (no extra dependency):
//   node --test --experimental-strip-types src/lib/format.test.mts
// Uses the .mts extension so the app's tsc/next build (which type-checks **/*.ts) skips
// this test file, while Node's ESM type-stripping still runs it. Keep in lock-step with
// the backend twin (backend/tests/test_price_format.py).

import assert from "node:assert/strict";
import { test } from "node:test";

import { formatPrice, formatQuoteValue } from "./format.ts";

// --- The six founder exact strings (the acceptance test) --------------------
test("Gold: >=100 -> 2 decimals with thousands commas", () => {
  assert.equal(formatPrice(4585.8, { assetClass: "commodity" }), "$4,585.80");
});

test("BTC: >=100 -> 2 decimals with thousands commas", () => {
  assert.equal(formatPrice(72909.88, { assetClass: "crypto" }), "$72,909.88");
});

test("Sub-dollar crypto -> 4 decimals", () => {
  assert.equal(formatPrice(0.1811, { assetClass: "crypto" }), "$0.1811");
});

test("Low single-digit -> 3 decimals", () => {
  assert.equal(formatPrice(1.264, { assetClass: "crypto" }), "$1.264");
});

test("Forex EUR/USD -> 4 decimals, no $", () => {
  assert.equal(formatPrice(1.169, { assetClass: "fx" }), "1.1690");
  assert.equal(formatPrice(1.169, { forex: true }), "1.1690");
});

test("Forex USD/JPY -> 4 decimals regardless of magnitude, no $", () => {
  assert.equal(formatPrice(158.884, { assetClass: "fx" }), "158.8840");
});

// --- Magnitude band boundaries ----------------------------------------------
test("Just under 100 -> 3 decimals", () => {
  assert.equal(formatPrice(99.999, { assetClass: "equity" }), "$99.999");
});

test("Exactly 100 -> 2 decimals", () => {
  assert.equal(formatPrice(100.0, { assetClass: "equity" }), "$100.00");
});

test("Just under 1 -> 4 decimals", () => {
  assert.equal(formatPrice(0.9999, { assetClass: "crypto" }), "$0.9999");
});

test("Exactly 1 -> 3 decimals", () => {
  assert.equal(formatPrice(1.0, { assetClass: "crypto" }), "$1.000");
});

// --- Sub-0.0001 significant-figure safeguard --------------------------------
test("Sub-0.0001 -> 4 significant figures (not $0.0000)", () => {
  assert.equal(formatPrice(0.00001234, { assetClass: "crypto" }), "$0.00001234");
  assert.equal(formatPrice(0.000009876, { assetClass: "crypto" }), "$0.000009876");
});

test("Exactly 0.0001 stays 4 decimals", () => {
  assert.equal(formatPrice(0.0001, { assetClass: "crypto" }), "$0.0001");
});

// --- Forex is never dollar-signed even sub-1 --------------------------------
test("Forex sub-1 -> 4 decimals, no $", () => {
  assert.equal(formatPrice(0.6543, { assetClass: "fx" }), "0.6543");
});

// --- Negative values --------------------------------------------------------
test("Negative dollar value", () => {
  assert.equal(formatPrice(-4585.8, { assetClass: "commodity" }), "-$4,585.80");
});

test("Negative sub-dollar value", () => {
  assert.equal(formatPrice(-0.1811, { assetClass: "crypto" }), "-$0.1811");
});

test("Negative forex value", () => {
  assert.equal(formatPrice(-1.169, { forex: true }), "-1.1690");
});

// --- Robustness -------------------------------------------------------------
test("null / NaN render em dash", () => {
  assert.equal(formatPrice(null, { assetClass: "crypto" }), "—");
  assert.equal(formatPrice(NaN, { assetClass: "crypto" }), "—");
});

test("Zero dollar value", () => {
  assert.equal(formatPrice(0, { assetClass: "crypto" }), "$0.0000");
});

test("Asset class is case-insensitive for forex", () => {
  assert.equal(formatPrice(1.169, { assetClass: "FX" }), "1.1690");
});

// --- Quote dispatcher -------------------------------------------------------
test("formatQuoteValue: forex quote -> 4dp no $", () => {
  assert.equal(
    formatQuoteValue({ price: 1.169, unit: "USD", asset_class: "fx" }),
    "1.1690",
  );
});

test("formatQuoteValue: dollar-priced equity index -> $ magnitude", () => {
  assert.equal(
    formatQuoteValue({ price: 6240.5, unit: "index", asset_class: "index" }),
    "$6,240.50",
  );
});

test("formatQuoteValue: rate stays a percent", () => {
  assert.equal(
    formatQuoteValue({ price: 4.12, unit: "%", asset_class: "rate" }),
    "4.12%",
  );
});

test("formatQuoteValue: macro index level stays plain", () => {
  assert.equal(
    formatQuoteValue({ price: 65.4, unit: "index", asset_class: "macro" }),
    "65.4",
  );
});

test("formatQuoteValue: null price -> em dash", () => {
  assert.equal(formatQuoteValue({ price: null, unit: "USD", asset_class: "crypto" }), "—");
});
