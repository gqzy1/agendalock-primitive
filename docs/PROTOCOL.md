# AgendaLock protocol

## Signed input and permissions

`open_agenda(tag,payload)` fixes exact JSON `{title,topics,members}`. There are 2–5 distinct case-insensitive topic names (1–80 characters) and 2–4 distinct nonzero wallet addresses. The title is 3–120 characters. The creator must be a member and becomes moderator. Tags use 3–32 lowercase letters, digits or hyphens, namespaced by the actual sender. An exact open replay is idempotent; conflicting input is rejected. Each creator may open at most 24 agendas.

Each named member supplies a statement of 20–2000 characters using their own transaction. A submitted statement cannot be replaced. Resubmitting identical text with the current revision is idempotent. `freeze` requires every roster member's statement and fixes the full signed ballot hash. The moderator cannot impersonate a member. There is no administrator bypass.

## Interpretation and consensus

The leader independently extracts one complete strict permutation of topic indices from each original member statement. Every validator repeats that extraction on the same original inputs, without seeing the leader's answer in its extraction prompt. All KNOWN/UNKNOWN decisions and ordinal indices must agree; a disagreement that does not change the chosen winner still rejects the proposal. Known quotation anchors must occur in the corresponding member's statement, never another member's text. Accepted anchors are deterministically fixed to the complete corresponding original statements. Every validator interprets that full source and must match all decision fields. Canonical JSON text crosses the nondeterministic boundary, avoiding container-type ambiguity.

Mention order is not preference. Ties, missing comparisons, unsupported conditions and ambiguity produce UNKNOWN. A different but clear opinion remains KNOWN. Schema/model errors, invalid quotes and independent disagreement abort before storage; they are not accepted uncertainty. No model chooses the consensus group order.

The accepted extraction uses native `gl.vm.run_nondet_unsafe`; Optimistic Democracy, votes, rotations, appeals and finality are network mechanisms. The contract does not replace them with scripted approvals.

## Exact Kemeny certificate

For every ordered pair `(a,b)`, support counts members placing a before b. A candidate order's objective is the number of member/pair disagreements: sum the reverse support for each pair in the candidate. Every permutation is enumerated lexicographically, up to `5! = 120` candidates. The proof retains each candidate and its score, the minimum, all minimum-scoring orders and the first lexicographic optimum. It also records opposing member indices for every chosen pair and directed majority triangles.

The complete candidate list proves global optimality within the declared roster and objective, not a heuristic. Pairwise support is derived only from accepted individual rankings. The protocol is unweighted; statement length and the moderator's identity add no vote weight. The tie-break is explicit topic-index order fixed at creation, not a hidden model preference.

## API and state

All views and mutating methods return JSON strings except opening, which returns the owner-qualified agenda ID. A missing view returns an empty string. Calls use positional arguments below.

| Method | Arguments | Caller / precondition |
| --- | --- | --- |
| `protocol` | none | Public |
| `get_agenda` | `agenda_id:string` | Public |
| `list_agendas` | `owner:string` | Public; created agendas only |
| `open_agenda` | `tag:string,payload:string` | Creator belongs to fixed roster |
| `submit` | `agenda_id:string,expected_revision:int,statement:string` | Named member; COLLECTING |
| `freeze` | `agenda_id:string,expected_revision:int` | Moderator; COLLECTING; all statements present |
| `rank` | `agenda_id:string,expected_revision:int` | Member; SEALED |
| `start` | `agenda_id:string,expected_revision:int,ranking_hash:string` | Moderator; READY; exact stored digest |
| `advance` | `agenda_id:string,expected_revision:int,topic:int` | Moderator; RUNNING; exact next topic |
| `cancel` | `agenda_id:string,expected_revision:int` | Any member; COLLECTING/SEALED/REVIEW/READY |

State flow is COLLECTING → SEALED → READY → RUNNING → CLOSED. An accepted uncertain ballot instead produces REVIEW. Pre-start states may become CANCELLED. CLOSED and CANCELLED are terminal. REVIEW cannot start or rerank; corrections create a new agenda. A running agenda has no before-start cancellation path.

Creation starts at revision 0. Each new statement, freeze, rank, start, advance or cancellation increments revision once. Every non-opening write checks the exact current integer revision. Boolean topic/revision values are not integers under protocol validation.

The ranking hash commits to protocol, agenda ID, frozen ballot hash, full accepted interpretations and the complete certificate. `start` recomputes the certificate before activating it. `advance` accepts only `chosen[cursor]`, appends it to completed and increments cursor; completed always equals a prefix of chosen. Final advancement closes the record. This is a persistent signed execution constraint, not a scheduler that can silently reorder work.

## Limitations

The electorate and topics are moderator declarations, not identity attestations. Public statements are public forever in transaction history. Consensus checks meaning against those statements, not whether the preferences are wise, true or sincere. Independent model interpretations cannot eliminate correlated errors. Minority disagreement and ties are reported, not erased. The exact objective does not promise strategy-proofness or universal satisfaction. State advancement records a signed acknowledgment only.
