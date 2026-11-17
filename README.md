# AgendaLock

**A shared agenda with a checkable disagreement budget.**

AgendaLock is a standalone GenLayer Intelligent Contract for small teams that need a fixed discussion order from independently signed priorities. Each member describes their strict preferences in ordinary language. Independent GenLayer validators agree on the complete individual rankings. Deterministic code checks every possible topic order, finds the exact Kemeny disagreement minimum and locks a reproducible agenda that cannot skip or repeat topics during execution.

It serves working groups, maintenance meetings and small review committees. A moderator cannot silently replace another member's priorities or assert that a convenient order is the collective optimum.

## Workflow

1. A moderator opens an agenda with 2–5 topics and 2–4 distinct member wallets, including themselves.
2. Every member signs their own immutable preference statement. The moderator can freeze only after all statements are present.
3. Any member requests `rank`. The leader and validators independently interpret every signed statement. They compare every complete ordinal decision; accepted anchors are fixed to the corresponding full signed statements. Missing comparisons, ties and ambiguous meaning produce REVIEW, not guessed preferences.
4. Exact enumeration computes every candidate's pairwise disagreement count, **all** optimal orders, pairwise support, opposing members and majority triangles. The canonical choice is the lexicographically first optimum by sealed topic index. The model does not choose it.
5. The moderator starts that exact ranking hash, then advances only the next canonical topic. Completion closes the agenda terminally. Before starting, any participant may cancel.

**Canonical Stable Studionet contract:** [`0xa9a4F60d1D046FCD7Df86C902751D4D4Ca84A3AB`](https://explorer-studio.genlayer.com/address/0xa9a4F60d1D046FCD7Df86C902751D4D4Ca84A3AB). [Real transactions and readbacks](EVIDENCE.md).

## Use

Stable Studionet only: chain **61999**, RPC `https://studio.genlayer.com/api`, SDK **genlayer-js@1.1.8**. Deploy [contracts/agendalock.py](contracts/agendalock.py), with its pinned runner and no constructor arguments. Full consensus is required. No funds, escrow, paid API credentials or frontend are needed.

```sh
npm ci
npm test
npm run verify
```

The verification command is read-only and checks source parity, every actual receipt, signed calldata, finalized state and an independent complete-ranking certificate calculation. [EVIDENCE.md](EVIDENCE.md) identifies the deployment and observed scenarios.

```js
await write('open_agenda', ['planning', JSON.stringify(input)]);
// Each named wallet submits its own statement with the current revision.
await write('submit', [id, currentRevision, statement]);
await write('freeze', [id, currentRevision]);
await write('rank', [id, currentRevision]);
// Read get_agenda at latest-final after successful FINALIZED execution.
await write('start', [id, record.revision, record.ranking_hash]);
await write('advance', [id, record.revision, nextTopicIndex]);
```

[Protocol and API](docs/PROTOCOL.md) · [Runnable calls](scripts/example.mjs) · [Statements](examples/statements.json) · [Tests](tests/test_agendalock.py) · [Operating scripts](docs/OPERATIONS.md).

## Why it needs GenLayer

The interpretation of “safety comes before logistics, with branding last” belongs to each signed member statement and must not depend on the moderator's private model. GenLayer provides the substantive independent interpretation boundary. After acceptance, deterministic exact optimization makes the disagreement objective and tie handling inspectable. The resulting persistent order also restricts later state transitions; it is more than an AI recommendation.

## Scope

This is an unweighted, small-roster strict-ranking protocol, not a public election, credential proof or Sybil-resistant poll. Wallets are named by the moderator; there is no claim of one wallet per person. Kemeny rankings can have multiple optima and Condorcet cycles; both are shown. The protocol does not claim every member is satisfied, that the tie-break is neutral to roster editing before sealing or that triadic cycles enumerate all longer cycles. Topic advancement is a signed agenda acknowledgment, not evidence that real discussion occurred. No private member information should be submitted to public chain state.
