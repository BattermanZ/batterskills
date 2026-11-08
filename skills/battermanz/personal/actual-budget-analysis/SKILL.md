---
name: actual-budget-analysis
description: Analyze and explain financial data from the Actual Budget MCP with transaction-level reconciliation and accounting sanity checks. Use for questions about spending, income, funding, transfers, refunds, reimbursements, balances, cash flow, category totals, account averages, trends, or comparisons in Actual Budget, especially when the user's wording must be translated into a precise metric.
metadata:
  version: "1.0.0"
---

# Actual Budget analysis

Use the Actual Budget MCP as the source of truth. Keep analysis read-only unless the user explicitly requests a mutation.

## Establish the metric

Translate the question into one primary metric before querying:

- **Gross spending / money paid out:** absolute sum of genuine expense outflows.
- **Net spending:** gross spending less genuine merchant refunds and expense reimbursements. State exactly what is deducted.
- **Funding:** money added to an account, including internal transfers and external top-ups. Funding is not negative spending.
- **Cash flow / balance change:** all inflows minus all outflows, including funding.
- **Budget performance:** budgeted, spent, and available category amounts; do not substitute account cash flow.

If two interpretations are materially plausible, calculate both when practical and lead with the one that best matches ordinary language. Ask only when the choice cannot be resolved from context or data.

## Reconcile the data

1. Resolve account, category, and payee names to IDs before querying transactions.
2. Use an explicit date range. For "past 12 months," state whether the range is 12 complete calendar months or a rolling 12-month window.
3. Inspect raw transactions before aggregating. Do not infer economic meaning from amount sign, category, payee, or `transfer_id` alone.
4. Reconcile all representations of money movement:
   - linked internal transfers;
   - external bank or card top-ups;
   - imported or historical movements;
   - merchant refunds, reversals, deposits, and pre-authorizations;
   - reimbursements from people;
   - split, parent, duplicate, tombstoned, and starting-balance transactions.
5. Group month by month first, then total and average. Preserve zero-activity months in the denominator when averaging over a fixed period.
6. Use transaction notes and counterparties to classify ambiguous credits. Leave genuinely unexplained items labelled unknown; never invent an explanation.

Actual's technical classification may not match the user's real-world model. Treat labels such as historical movements, unknown receipts, imported top-ups, and transfer metadata as evidence, not conclusions.

## Validate

Before answering, verify:

- monthly values sum to the period total;
- period total divided by the stated number of months equals the reported average;
- cash-flow identity holds: opening balance + inflows - outflows = closing balance, allowing only explicitly identified adjustments;
- transfers are included or excluded consistently on both sides;
- refunds or reimbursements are not described as funding, and funding is not described as a refund;
- recurring patterns and round amounts are checked transaction by transaction when they materially affect the result;
- surprising results receive a second pass over the underlying transactions.

Use user-provided facts as validation constraints, not as permanent account-specific rules. If the data conflicts with a stated invariant, show the exact conflicting transactions and dates instead of averaging the discrepancy away.

## Answer

Lead with the direct answer, currency, metric, and date range. Then show the shortest calculation that makes it auditable. Include a monthly table when the result is surprising, classifications are ambiguous, or the user asks for verification.

Clearly distinguish:

- **Verified:** directly supported by transaction data.
- **Classified:** supported by payee, notes, linkage, or recurring pattern.
- **Unknown:** insufficient evidence.

Do not introduce secondary concepts such as "the account became poorer" unless the user asked about balance change and the full cash-flow reconciliation supports that statement.
