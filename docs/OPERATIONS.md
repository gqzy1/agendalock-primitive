# Reproducible use and verification

Use Python 3.12+, Node.js 22+ and the locked `genlayer-js@1.1.8`. Install with `npm ci`; run local tests with `npm test`. Those tests use a scripted host/model and do not establish real network agreement. Optional SDK checks use `genvm-linter==0.11.0`: `genvm-lint check contracts/agendalock.py --json`. The pinned runner passed SDK validation and the recorded Stable Studionet schema compilation; a newer-runner advisory is informational.

## Read-only verification

`npm run verify` needs no signer and sends no transactions. It fetches every recorded receipt, verifies finality, positive successful execution, expected negative rejection, majority agreement, full consensus and actual signed method/arguments. It compares deployed bytes with the recorded source SHA256, reads final agendas at `latest-final` and runs an independent direct-inversion-count checker over all candidate orders and their commitments.

Public receipt files retain selected fields from real RPC responses, including leader execution/output and returned vote records. Full server configuration is omitted; raw response hashes are in the live journal. They are not synthetic receipts. If the hosted Studio is reset or unavailable, re-verification must report that condition honestly.

## Calls with independent members

```sh
node scripts/example.mjs protocol
node scripts/example.mjs get_agenda '["MODERATOR_ADDRESS:planning"]'
```

Read IDs from `evidence/live.json`. To open a new agenda, replace both placeholder wallets in `examples/agenda-template.json`. Members must use their own signers for `submit`. Invoke the example script with a method and JSON array of positional arguments. All mutating calls require private local `STUDIO_PRIVATE_KEY` and deliberate `ENABLE_CHAIN_WRITES=61999`; keep keys out of command arguments, commits and documents.

Read fresh revision after every FINALIZED successful call. Submit each member's original statement; the moderator freezes only after all are present. A member calls `rank`; inspect the complete accepted individual orders, all optimum rankings, tie-break and dissent before the moderator starts the stored ranking hash. Call `advance` only with the next topic from `proof.chosen`. A meeting's signed completion is not evidence of real-world discussion.

The caller journals the original hash in ignored `.local/` and resumes it after a timeout. A SUBMITTING marker without returned hash requires wallet/history reconciliation. Do not silently retry. A verified call is not resent. The caller verifies final execution; read business state explicitly after it.

## Deployment and acceptance

`npm run schema` is read-only compilation. `ENABLE_CHAIN_WRITES=61999 npm run live` creates dedicated restricted local test signers and deploys only if no deployment journal exists. Otherwise it resumes recorded hashes and skips successful stages. No frontend or paid service is involved; zero value is attached, and the run does not buy or transfer tokens. Do not delete journals to rerun successful transactions. Changed source after a recorded run fails closed.

The live acceptance uses separately generated member signers, validates their actual calldata and waits for FINALIZED plus successful execution on every positive step. Expected immutable-ballot, moderator, digest, next-topic and terminal-state rejections must finalize with the named error and unchanged state; those are recorded as failures, never counted as successful transactions. Native semantic extraction covers clear individual orders, missing strict order and a cyclic three-member profile with multiple Kemeny optima. FINALIZED status alone is insufficient: normal mode, full consensus and majority agreement are mandatory.

A fresh clone includes public evidence but never the original private signer keys. Use `npm run verify` in that clone. The live runner requires its original local actors to match the journal and refuses mismatched newly generated keys instead of issuing substitute signatures.
