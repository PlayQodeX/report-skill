---
title: Payments API Security Review
subtitle: "Static review of the Payments API across auth, input validation, and data handling. 9 findings: Critical 1 · High 2 · Medium 4 · Low 2. Overall score: 7 / 10."
kind: audit
status: final
date: 2026-06-21
author: Jane Doe
app: Payments API
org: Your Brand
org_tld: example.com
---

# Payments API Security Review

## 1. Executive Summary

The Payments API is **well-structured but ships one critical authentication gap**.
Total findings: 9. Critical: 1 | High: 2 | Medium: 4 | Low: 2. Overall score: 7 / 10.
The critical item — a missing signature check on the refund webhook — must be closed
before the next release; everything else is hardening.

## 2. Scope and Approach

A static review of the `payments-api` service: route handlers, the auth middleware,
input validation, and outbound webhook handling. Runtime penetration testing and a
load test were out of scope.

## 3. Findings

| Severity | Finding | Location | Action Required |
|----------|---------|----------|-----------------|
| **CRITICAL** | Refund webhook accepts unsigned payloads | `src/webhooks/refund.ts:42` | Verify the provider signature before processing; reject on mismatch |
| **HIGH** | No rate limit on `POST /charges` | `src/routes/charges.ts:18` | Add per-key rate limiting; return `429` over the threshold |
| **HIGH** | Error responses leak stack traces in production | `src/middleware/error.ts:7` | Return a generic message in prod; log the detail server-side |
| **MEDIUM** | Amounts parsed as floats | `src/lib/money.ts:11` | Use integer minor units throughout |
| **PASS** | Secrets are read from the environment, never committed | `src/config.ts` | None — confirmed sound |

## 4. Risk Summary

| # | Residual item / Risk | Impact | Likelihood | Type |
|---|----------------------|--------|------------|------|
| 1 | Forged refund webhook drains balance | High | Medium | Security |
| 2 | Charge endpoint abuse / cost run-up | Medium | Medium | Abuse |

## 5. Recommendations

**Immediate** — close the webhook signature gap and ship a patch release.
**Short-term** — add rate limiting and switch money to integer minor units.
**Medium-term** — add contract tests for every webhook and a coverage gate in CI.

## 6. Conclusion

The service is close to production-ready. With the refund webhook signed and rate
limiting in place, the Payments API clears the bar for a controlled rollout.

---

## Appendix A — Files reviewed

`src/routes/`, `src/webhooks/`, `src/middleware/`, `src/lib/money.ts`, `src/config.ts`.
