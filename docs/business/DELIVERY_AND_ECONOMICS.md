# Delivery, economics, and operations

Part of [BIZ-001](README.md). Policies below are proposed defaults for review, not established legal terms or spending authorization.

## Delivery checklist

1. Confirm the buyer, decision owner, affected users, scope, price, payment schedule, acceptance test, and support window in a [pilot brief](../../templates/business/PILOT_BRIEF.md).
2. Agree permitted data, tools, access, retention, deletion, and customer approval responsibilities before intake.
3. Record a baseline: task volume, time, errors/rework, current costs, measurement window, and competing changes.
4. Diagnose and compare with the simplest adequate alternative. Stop or rescope if the problem is outside competence or the solution is not worthwhile.
5. Implement in a safe test environment, with least-privilege access, backups where relevant, and a rollback plan. Production changes require explicit approval.
6. Test ordinary cases and failures. Include human review where needed; do not silently delegate consequential decisions to an experimental engine.
7. Deliver documentation, acceptance evidence, remaining limitations, and ownership of recurring tasks.
8. Collect feedback and outstanding payment, provide the agreed support, revoke unnecessary access, and execute agreed retention/deletion.

Log scope changes with price/time implications before implementing them. Separate defect correction within scope from newly requested features. Record incidents and remedial actions without publishing customer details.

## Economics: track two views

**Cash view:** money actually received minus cash actually paid. An unpaid invoice is not available compute funding. Cash flow can look positive because the founder worked unpaid or a bill has not arrived.

**Full-cost view:** attributable revenue minus delivery labor (including founder hours at an explicit rate), tools/API use, contractors, payment/platform fees, acquisition effort, and expected support/refund costs. Track fixed overhead separately to avoid double counting. This is an operating model, not a statutory accounting policy.

Record estimated versus actual amounts per engagement:

| Field | Why it matters |
|---|---|
| Agreed fee, invoiced amount, collected amount, dates | Separate booking, billing, and collection |
| Delivery, sales, admin, and support hours | Expose hidden founder labor and capacity constraints |
| Chosen labor rates and cash compensation | Distinguish economic cost from cash outflow |
| Direct tools, compute, contractors, fees | Understand job-level cost |
| Refunds, rework, maintenance commitment | Avoid treating unfinished obligations as profit |
| Acquisition cost allocation | Avoid apparently profitable jobs subsidized by unpaid selling |
| Contribution after attributable costs | Amount available for overhead and reinvestment |
| Fixed overhead, reserve, obligations | Determine whether the business itself is sustainable |

Simple planning arithmetic:

- Full-cost contribution per job = attributable revenue minus all attributable costs.
- Approximate break-even jobs = fixed period costs divided by positive contribution per similar job, rounded up.
- This estimate is invalid if scope varies materially, capacity is insufficient, or contribution is non-positive.
- Customer time saved is not automatically cash saved; distinguish measured time, avoided expense, redeployed capacity, and estimated value.

Prices must test customer willingness to pay and cover costs. No price, salary, margin target, or reserve amount is approved yet.

## Research and compute allocation

Choose a cash reserve and review period before distributing surplus. Allocate only collected cash remaining after due and reserved delivery, compensation, operating, refund, and applicable obligations. Record the proposed research amount, purpose, cap, and approver; the founder must approve actual expenditure.

For each compute increase, name the bottleneck and the result that would justify continuing. If customer access, data quality, evaluation, or implementation is limiting progress, more runs may not help. Do not automatically reinvest all cash or equate a revenue increase with research progress.

## Operational groundwork before the first paid engagement

- Confirm appropriate contracting/invoicing identity and payment arrangements.
- Resolve local registration, tax, contract, insurance, and outreach obligations with relevant qualified advice where needed; this repo does not determine compliance.
- Agree deliverable ownership, reusable background tools, third-party licenses, confidentiality, cancellation, liability, and support boundaries.
- Define access control, credential handling, incident contact, backup/recovery responsibilities, and retention/deletion.
- Name the delivery owner, capacity limit, and backup plan if the founder is unavailable.
- Use contractors or partners only after checking competence, permissions, confidentiality, cost, and customer commitments.
- Verify rights and permissions before publishing customer names, logos, testimonials, or case studies.

## Public/private boundary

This repository is public-facing. Commit strategy, blank forms, synthetic demonstrations, and approved non-identifying summaries only. Keep contact lists, transcripts, contracts, invoices, credentials, raw client data, and confidential commercial details in an approved private system outside the repository.

Private storage and its owner must be selected before intake. An ignored folder is not access control, and pseudonyms do not guarantee anonymity. Share only the minimum authorized data with models or external services. Check every diff for accidental disclosure; removing a file later does not remove it from Git history.
