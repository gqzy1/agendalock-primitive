# AgendaLock — on-chain evidence

- Network: Stable Studionet, chain **61999**, RPC `https://studio.genlayer.com/api`.
- Contract: [`0xa9a4F60d1D046FCD7Df86C902751D4D4Ca84A3AB`](https://explorer-studio.genlayer.com/address/0xa9a4F60d1D046FCD7Df86C902751D4D4Ca84A3AB).
- Deployment transaction: [`0x5a56e6c901b0647c4f9f7fb5f78b0e70fb70c72584376a7c39ded40bd02ccaf1`](https://explorer-studio.genlayer.com/tx/0x5a56e6c901b0647c4f9f7fb5f78b0e70fb70c72584376a7c39ded40bd02ccaf1).
- Source SHA256: `2d789587f4080e50619008d20f3ba0f6c96d337d00d1e9d01c18215a15f0fd43`.
- Exact SDK: `genlayer-js@1.1.8`. Deployed source matches repository bytes.
- Canonical run: **33 FINALIZED transactions: 26 SUCCESS and 7 expected contract rejections.**
- Fresh independent receipt/source/calldata/readback verification: passed, `2026-11-17T18:48:55.397Z`.

Negative cases are finalized failed executions with the exact expected error and unchanged state. They are never counted as SUCCESS. ACCEPTED and a successful leader alone were insufficient. Every positive result also required majority agreement, NORMAL execution mode, full consensus and a matching finalized business-state readback.

## Actual transaction index

| Step | Transaction | Expected result | Observed execution |
| --- | --- | --- | --- |
| deploy | [`0x5a56e6c901…`](https://explorer-studio.genlayer.com/tx/0x5a56e6c901b0647c4f9f7fb5f78b0e70fb70c72584376a7c39ded40bd02ccaf1) | SUCCESS | FINALIZED / SUCCESS |
| open-main | [`0x272eeb1e1f…`](https://explorer-studio.genlayer.com/tx/0x272eeb1e1f66881b4b8176ee115924eeafa1c3c8a136415b3395e2cac4d9775a) | SUCCESS | FINALIZED / SUCCESS |
| open-unclear | [`0xe71f4e217e…`](https://explorer-studio.genlayer.com/tx/0xe71f4e217eadb335f04ae28ff7b25f656813dfe57aa50a5397ea2ed4a2259b78) | SUCCESS | FINALIZED / SUCCESS |
| open-cycle | [`0x9d1c2b354e…`](https://explorer-studio.genlayer.com/tx/0x9d1c2b354edc1321c019170e06a3904431bcd54e5c307c7b5cd1b3908d801589) | SUCCESS | FINALIZED / SUCCESS |
| submit-owner | [`0xcef97b59b4…`](https://explorer-studio.genlayer.com/tx/0xcef97b59b447a86ddc6209c897ce84663894a5dd948f57cffb7c202768b42659) | SUCCESS | FINALIZED / SUCCESS |
| cycle-0 | [`0xa7683a7f95…`](https://explorer-studio.genlayer.com/tx/0xa7683a7f9550836063587c705c064e4dbafb5bcca092f45b8fcaf9d33349379e) | SUCCESS | FINALIZED / SUCCESS |
| unclear-owner | [`0xcfbe0c9ad5…`](https://explorer-studio.genlayer.com/tx/0xcfbe0c9ad515fdb127a3fa329b9b8ef4e96be7eb6c9b4e13d381d56a9c4fbbf1) | SUCCESS | FINALIZED / SUCCESS |
| submit-member | [`0xe7a16a1df2…`](https://explorer-studio.genlayer.com/tx/0xe7a16a1df251a2c36266904c7e60062410534eec42a8742d9cb6f4c2a4b7a313) | SUCCESS | FINALIZED / SUCCESS |
| cycle-1 | [`0xd7c76f8c71…`](https://explorer-studio.genlayer.com/tx/0xd7c76f8c717e72c6f3cc5d042fa2993eb17ae170879278519dbe00736555cbd2) | SUCCESS | FINALIZED / SUCCESS |
| unclear-member | [`0xb6775175c9…`](https://explorer-studio.genlayer.com/tx/0xb6775175c9f5877b7a85ad8c832acf890c796d3e739d34da915967a19e364bb8) | SUCCESS | FINALIZED / SUCCESS |
| cannot-rewrite-ballot | [`0x7bb4bd7fef…`](https://explorer-studio.genlayer.com/tx/0x7bb4bd7fef5acf14289a0e36fd845dacfd96b416f9102f855a84c56ac827bcea) | BALLOT_IMMUTABLE | FINALIZED / ERROR |
| cycle-2 | [`0x22a8635056…`](https://explorer-studio.genlayer.com/tx/0x22a86350567b6425481ab3ffbf444fd1fc57430c6e3fccdcb69fe2b0ac6ea8e5) | SUCCESS | FINALIZED / SUCCESS |
| freeze-unclear | [`0x1f40d78d47…`](https://explorer-studio.genlayer.com/tx/0x1f40d78d47e93413cc467925c2583aa79965a4e0eaac7613324c3f4199d09535) | SUCCESS | FINALIZED / SUCCESS |
| nonmoderator-freeze | [`0xb249c92310…`](https://explorer-studio.genlayer.com/tx/0xb249c923106f40183ff36856632626a7ed37895846565b3e98ae8e2ee645a921) | MODERATOR_ONLY | FINALIZED / ERROR |
| freeze-cycle | [`0x934d1c2ef2…`](https://explorer-studio.genlayer.com/tx/0x934d1c2ef289fa64d46ad38c6f8f7a3756afb8aa2f951cfc26c39ddd93a397a1) | SUCCESS | FINALIZED / SUCCESS |
| rank-unclear | [`0xf6265f26c0…`](https://explorer-studio.genlayer.com/tx/0xf6265f26c0a169ce51165279d7367c314ef76760f8346dc206adc00b6b992d32) | SUCCESS | FINALIZED / SUCCESS |
| freeze-main | [`0xe55b7fed60…`](https://explorer-studio.genlayer.com/tx/0xe55b7fed60aea34a90b97b9300e0c7a8839318ecfa443fd3bfadd6837e2bdb65) | SUCCESS | FINALIZED / SUCCESS |
| rank-cycle | [`0x18ad7d7e80…`](https://explorer-studio.genlayer.com/tx/0x18ad7d7e8032342d205e602ce1b461383c7e47db59f8b2692111bf74351cb941) | SUCCESS | FINALIZED / SUCCESS |
| review-cannot-start | [`0x64c9bb1054…`](https://explorer-studio.genlayer.com/tx/0x64c9bb1054ecbbc8e8ebc54276e1d1ee4fe6f134701e56a8f7a3eba60f3d598d) | NOT_READY | FINALIZED / ERROR |
| rank-main | [`0x1e978e77c6…`](https://explorer-studio.genlayer.com/tx/0x1e978e77c6b95d770d338ef2ecf7300caaf374c2c57006d118857042fa44f0e5) | SUCCESS | FINALIZED / SUCCESS |
| start-cycle | [`0x412ad43c50…`](https://explorer-studio.genlayer.com/tx/0x412ad43c5012935ccdc738cf1033fccc2c2599af5a3925e6d5ec764504850779) | SUCCESS | FINALIZED / SUCCESS |
| member-cancel | [`0xaf4e975f3f…`](https://explorer-studio.genlayer.com/tx/0xaf4e975f3fa9c3b4b044197024224ce3d1415a69b2575a37931b2a0a30437076) | SUCCESS | FINALIZED / SUCCESS |
| nonmoderator-start | [`0x3bf1467026…`](https://explorer-studio.genlayer.com/tx/0x3bf1467026de9d037d167d5584de4d58938d09762d1c6b31bfd90591f4753050) | MODERATOR_ONLY | FINALIZED / ERROR |
| cycle-complete-0 | [`0xf594b62e3e…`](https://explorer-studio.genlayer.com/tx/0xf594b62e3ebcf796bbb2051b2c156b10e5bc7022295f53491d8a77a8714bca7f) | SUCCESS | FINALIZED / SUCCESS |
| wrong-ranking-hash | [`0xbf4256a9b7…`](https://explorer-studio.genlayer.com/tx/0xbf4256a9b7c08aa629fe80879674f107a9b939dbd27a4c256fa731e14a103772) | RANKING_MISMATCH | FINALIZED / ERROR |
| cycle-complete-1 | [`0xe6e87f148d…`](https://explorer-studio.genlayer.com/tx/0xe6e87f148d5814f252e66e3dfcc957b310b3f3fd31453024dbe9bab75a95d07b) | SUCCESS | FINALIZED / SUCCESS |
| start-main | [`0xb15f9a0be7…`](https://explorer-studio.genlayer.com/tx/0xb15f9a0be7aa4c632a15b638278f7f884fb431d44f4fbee0eb18b3471512ee9f) | SUCCESS | FINALIZED / SUCCESS |
| cycle-complete-2 | [`0x4e34b5fcfc…`](https://explorer-studio.genlayer.com/tx/0x4e34b5fcfc89a8d11f2db1cfdbc236bf7e0c483edf02e82751708da4f02fd00d) | SUCCESS | FINALIZED / SUCCESS |
| cannot-skip-topic | [`0x8817d2ae28…`](https://explorer-studio.genlayer.com/tx/0x8817d2ae287b32ca8fe88f27541a10252ae37b8fd8059386c213ecca822be48f) | WRONG_NEXT_TOPIC | FINALIZED / ERROR |
| complete-safety | [`0xe51b195e5f…`](https://explorer-studio.genlayer.com/tx/0xe51b195e5f093ca2aa3e0a26c6cb953e2c92d1b594a6a87da529967da04c7a95) | SUCCESS | FINALIZED / SUCCESS |
| complete-logistics | [`0xbc98c064a2…`](https://explorer-studio.genlayer.com/tx/0xbc98c064a2bb98effd4b5655aca39b7e9294f5cfa1aeda5efeb2af2b55353803) | SUCCESS | FINALIZED / SUCCESS |
| complete-branding | [`0x83f4a01f17…`](https://explorer-studio.genlayer.com/tx/0x83f4a01f1755c91ec804456324251780620af990d1398259473dad3ee3324e6b) | SUCCESS | FINALIZED / SUCCESS |
| cannot-repeat-closed | [`0xd6027d5d79…`](https://explorer-studio.genlayer.com/tx/0xd6027d5d794fe7cae870d892a61fe10169933ec5453d12e5aedfedcc5b9d6d52) | NOT_RUNNING | FINALIZED / ERROR |

## Final state readback

All final records were read again using **latest-final** and independently verified.

- `0x19832461b4432508905361fec63f74f746c4a685:planning`: **CLOSED**, completed `[2, 0, 1]`, revision 8.
- Main ranking: `[2, 0, 1]`, minimum disagreement `0`.
- Cyclic profile: **CLOSED**, minimum disagreement `4`, all optima `[[0, 1, 2], [1, 2, 0], [2, 0, 1]]`, chosen `[0, 1, 2]`.
- Unranked/tied statement: accepted REVIEW, then member cancellation to **CANCELLED**.

## Evidence files

- `deployment.json`: canonical network, address, transaction and source hash.
- `evidence/live.json`: actual signed intents, hashes, selected real receipts, before/after readbacks and final states.
- `evidence/receipts/`: selected actual RPC fields, including returned votes and leader outputs. Server configuration is omitted.
- `evidence/verification.json`: fresh independent source, receipt, calldata, finality and readback checks.
- `evidence/verified-records.json`: independently fetched final records.
- `evidence/solver-parity.json`: AST identity of unchanged solver functions and their previously tested source.
- `scripts/verify_record.py`: offline proof verifier independent of contract imports.

## Historical source compatibility evidence

Historical attempts are excluded from the canonical acceptance totals. They are not presented as successful native execution. The initial immutable source assumed its extra JSON audit returned a string; its semantic validation failed closed. `evidence/history/revision-1/` retains its exact deployed source and observed receipts. Revision 2 handled JSON objects and completed known-input main workflows, but uncertain cases did not reach majority agreement. `evidence/history/revision-2/` preserves those actual successes and failures.

The canonical validator independently reinterprets the complete original inputs and compares every business decision. Anchors are deterministically fixed to the complete original source text. Canonical JSON text crosses the native boundary. No additional language-audit call is used.

## Local verification and limits

11 current parser/state/validator groups passed in `evidence/current-contract-tests.txt`. Unchanged mathematical oracle results remain in `evidence/base-solver-tests.txt`, with solver AST identity verified separately; those successful oracle tests were not repeated.
The independent inversion-count oracle covers all 216 three-member/three-topic profiles and 100 four-member/five-topic profiles. Current tests cover signed-member isolation, immutable ballots, incomplete rosters, uncertainty, hashes, revisions, next-topic enforcement and terminal states.

GenVM lint and SDK validation passed. A newer-runner advisory is informational; the pinned source passed real Stable Studionet schema compilation and the native transactions above. Inputs are synthetic public declarations; transactions, validators and stored states are real. These checks do not prove immunity to all prompt manipulation, network outages or correlated errors. No real-world event, identity or service fulfillment is asserted. No cash purchase, asset custody or external command execution is involved.
