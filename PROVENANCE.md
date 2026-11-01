# Provenance of this public release

This release was derived on 2026-11-01 from two private audit bundles. The bundles themselves are not published, because they contain third-party full texts, page captures, unlicensed upstream code and private correspondence metadata. Their SHA-256 values are recorded here so that the author can later show the exact originals to a reviewer.

| Private original | Bytes | SHA-256 |
|---|---|---|
| `Levin_Dietz_Sweet_Audit_2026-11-01(Codex).zip` | 119375087 | `4ab37fef36b7ce58db9840216afe2fe61d8fea6aaa47014b2219baa07bae0b26` |
| `levin-sorting-auditClaude.zip`, an earlier snapshot of the Claude bundle | 179866 | `18f8dead46193e540eec119dfece9e27e13efd0ea2a0f43c0973692b1b906d4d` |

## How the public copy was made

- `tools/build_public_release.py` (included) applied the removal rules.
- **codex-audit/.** Every kept file is byte-identical to the private original, and `verify_public_release.py` checks each one against the bundle's own `SHA256SUMS.txt`. Removed files are listed, with their original SHA-256 and the reason for removal, in `codex-audit/PUBLIC_RELEASE_REMOVED_FILES.json`. Because those files are absent, the bundle's own validator (`RUN_CHECKS.ps1`, `code/validate_package.py`) reports them missing in this copy. That is expected.
- **claude-audit/.** This is the final state of the Claude bundle at the end of the session. It is newer than the earlier snapshot hashed above, and adds the second-pass checks. Changes made for the public release are recorded in `CHANGELOG.md`. Removed files are listed in `claude-audit/PUBLIC_RELEASE_REMOVED_FILES.json`.
- **Prepared by AI.** `CROSS_AUDIT.md`, this repository's structure and the release tooling were prepared by Claude Opus 5.5 in Claude Cowork, at the request of Nathan Sweet.
