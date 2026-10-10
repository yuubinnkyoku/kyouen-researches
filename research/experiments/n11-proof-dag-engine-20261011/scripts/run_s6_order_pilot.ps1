param(
    [Parameter(Mandatory=$true)][string]$Solver,
    [string]$OutputRoot = "research/experiments/n11-proof-dag-engine-20261011/output/s6-order-pilot",
    [int]$SolverBudget = 100000,
    [int]$ProofLimit = 1000000,
    [string[]]$Orders = @("count-asc", "count-desc", "key"),
    [switch]$NativeProofCapture
)
$ErrorActionPreference = "Stop"
$python = (Get-Command python).Source
$rootLo = "10448351135500075008"
$rootHi = "1040"
foreach ($order in $Orders) {
    $out = Join-Path $OutputRoot $order
    if (Test-Path (Join-Path $out "proof-dag.json.gz")) {
        & $python "research/experiments/n11-proof-dag-engine-20261011/scripts/verify_saved.py" `
            (Join-Path $out "proof-dag.json.gz")
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        continue
    }
    $priorRun = Join-Path $out "run.json"
    if (Test-Path $priorRun) {
        $prior = Get-Content -Raw $priorRun | ConvertFrom-Json
        if ($prior.status -eq "solver_unknown_or_cutoff") {
            Write-Output "order=$order status=$($prior.status) nodes=$($prior.solver_result.nodes)"
            continue
        }
        throw "Existing non-certificate run needs review: $priorRun"
    }
    $captureArgs = @()
    if ($NativeProofCapture) { $captureArgs = @("--native-proof-capture") }
    & $python "research/experiments/n11-proof-dag-engine-20261011/scripts/certify.py" `
        --solver $Solver --n 11 --root-lo $rootLo --root-hi $rootHi `
        --solver-budget $SolverBudget --solver-order $order `
        --proof-limit $ProofLimit --proof-order $order --proof-sharing d4 `
        --out-dir $out @captureArgs
    if ($LASTEXITCODE -ne 0) {
        $runPath = Join-Path $out "run.json"
        if (Test-Path $runPath) {
            $record = Get-Content -Raw $runPath | ConvertFrom-Json
            if ($record.status -eq "solver_unknown_or_cutoff") {
                Write-Output "order=$order status=$($record.status) nodes=$($record.solver_result.nodes)"
                continue
            }
        }
        Write-Error "certification failed for order=$order (exit $LASTEXITCODE); inspect $out/run.json"
        exit $LASTEXITCODE
    }
    & $python "research/experiments/n11-proof-dag-engine-20261011/scripts/verify_saved.py" `
        (Join-Path $out "proof-dag.json.gz")
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
