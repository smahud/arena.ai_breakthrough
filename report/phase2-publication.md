# Phase 2.8 — authorized publication and public verification

**Date:** 2026-11-07T04:57Z UTC, after the dated Phase-2 final report was locally committed. This report **supersedes only the previous publication blocker**, not the experimental/architectural findings or original raw logs.

## Before → authorized change → verified state

| Stage | Source/evidence | Classification |
|---|---|---|
| Earlier failure | [`publication-attempt.log`](../evidence/phase2/publication-attempt.log): no connector, no credential helper, no remote `origin`, `git push --dry-run` exit **128**; public HEAD `79412fd`. | VERIFIED *at the time*, preserved, not erased |
| User authorization | User supplied a PAT in this chat after reading blocker, requesting its use. No credential value retained in repo/artifacts/config/URL; the temporary helper contained only generic instructions. Conversation/tool input may retain the sensitive string: [security note](../evidence/phase2/publication-security-note.md). | VERIFIED authorization; do not claim the conversation is secret-free |
| Permission check | Authenticated GitHub `/user` HTTP **200**, login `smahud`; authenticated repo endpoint **200**, `private=false`, `default_branch=master`, `permissions.push=true`. Local worktree clean, remote `79412fd` ancestor of local `600f762` (6 commits ahead). | VERIFIED for this token/repository/time |
| Push | Direct HTTPS git push with short-lived askpass helper, **no force**, exit **0**, response `79412fd..600f762 HEAD -> master`. GitHub connector remained `unsupported`; no secret in remote URL or git config. | VERIFIED from tool result; sanitized outcome in [publication-success.log](../evidence/phase2/publication-success.log) |
| Independent public read | Anonymous `git ls-remote --symref` HEAD/master both `600f7620d569bf9f4986fdb87a4387ee50ea6400`; anonymous repository, closing commit and final-report content APIs all **200**. | VERIFIED, [raw publication-success.log](../evidence/phase2/publication-success.log) |

The five earlier research commits plus the closing report are now public: [audit `c0caa6e`](https://github.com/smahud/arena.ai_breakthrough/commit/c0caa6efbe8128d89abf066815340c8c02afe2bc), [preregistration `9430392`](https://github.com/smahud/arena.ai_breakthrough/commit/9430392dece0030abb264121e94a02d13681f7d6), [EXP-10 `cd5c029`](https://github.com/smahud/arena.ai_breakthrough/commit/cd5c029c68501a24d447b6ae6d55c4c74d9c5693), [EXP-11/security `b33d900`](https://github.com/smahud/arena.ai_breakthrough/commit/b33d900335b19532b6234e385e4f51d1839261e4), [synthesis `6508821`](https://github.com/smahud/arena.ai_breakthrough/commit/65088210a6fd686d39690f9b87817a00e0fe82be), [closing `600f762`](https://github.com/smahud/arena.ai_breakthrough/commit/600f7620d569bf9f4986fdb87a4387ee50ea6400). The current publication-correction commit will be verified separately after its own fast-forward push; do not invent its SHA in this document before it exists.

**Post-success correction validation:** six anonymous *individual commit* API requests
returned **200 and matching SHA**; main tests again **45/45**, disposable pipeline
**7/7**, 12 corrected docs had zero missing local links, and checked file text
contained zero PAT-value patterns (not a guarantee about all leak channels).
[`publication-correction-validation.log`](../evidence/phase2/publication-correction-validation.log)
preserves output before this publication-update commit.

**Remaining research limitation:** genuine **new-chat** continuity and compaction observations are PENDING, unrelated to delivery. The isolated fixture had **50/50** tests and **7/7** pipeline in its replay, before publication; no new source changes in this delivery stage. **Credential safety:** advise user to revoke/rotate the PAT after final push verification, since it was supplied through a chat/tool call. Never echo the value.
