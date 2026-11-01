param([switch]$Recompute, [string]$AuditPython = '')
$ErrorActionPreference = 'Stop'
$auditRoot = $PSScriptRoot
if (-not $AuditPython) { $AuditPython = Join-Path $auditRoot '.venv\Scripts\python.exe' }
if (-not (Test-Path -LiteralPath $AuditPython)) { throw 'Create a Python 3.12 environment and pass its executable with -AuditPython. See README.md.' }
if ($Recompute) {
    $auditChecks = @('check_math_and_replay.py','check_source_semantics.py','check_actual_source.py','check_robustness.py','check_fish.py','check_morphometrics_calibration.py','check_wings.py','check_nanopub_crypto.py','check_crypto_negative_control.py','check_rsa_independently.py')
    foreach ($auditCheck in $auditChecks) {
        & $AuditPython -X utf8 (Join-Path $auditRoot ('code\' + $auditCheck))
        if ($LASTEXITCODE -ne 0) { throw ('Check failed: ' + $auditCheck) }
    }
    Write-Output 'Recomputation finished. Runtime fields changed; keep the original archive and regenerate the manifest only for a separately labeled new audit version.'
} else {
    & $AuditPython -X utf8 (Join-Path $auditRoot 'code\validate_package.py')
    if ($LASTEXITCODE -ne 0) { throw 'Package validation failed. Read results/package_validation.json.' }
}
