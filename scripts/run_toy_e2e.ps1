param(
    [string]$Distro = "Ubuntu",
    [string]$Harbor = "harbor",
    [string]$CodexAuthJson = "",
    [string[]]$Models = @("gpt-5.6-sol", "gpt-5.6-luna"),
    [string]$ReasoningEffort = "medium"
)

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uvCommand) {
    throw "uv is required on Windows."
}
if ($Models.Count -lt 1) {
    throw "Provide at least one model."
}

& $uvCommand.Source run --project $repoRoot python (Join-Path $repoRoot "scripts\prepare_toy_task.py")
if ($LASTEXITCODE -ne 0) { throw "Task preparation failed." }

$taskWindows = Join-Path $repoRoot ".runs\tasks\scan-ledger-batches"
$jobsWindows = Join-Path $repoRoot ".runs\jobs"
$dockerConfigWindows = Join-Path $repoRoot "examples\docker-public-config"
New-Item -ItemType Directory -Force -Path $jobsWindows | Out-Null

function ConvertTo-WslPath([string]$Path) {
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if ($fullPath -notmatch '^([A-Za-z]):\\(.*)$') {
        throw "Only a local Windows drive path can be converted: $fullPath"
    }
    $drive = $Matches[1].ToLowerInvariant()
    $tail = $Matches[2].Replace('\', '/')
    return "/mnt/$drive/$tail"
}

$taskWsl = ConvertTo-WslPath $taskWindows
$jobsWsl = ConvertTo-WslPath $jobsWindows
$dockerConfigWsl = ConvertTo-WslPath $dockerConfigWindows
$jobName = "scan-ledger-toy-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

$harborArguments = @(
    "run",
    "--path", $taskWsl,
    "--agent", "codex"
)
foreach ($model in $Models) {
    $harborArguments += @("--model", $model)
}
$harborArguments += @(
    "--agent-kwarg", "reasoning_effort=$ReasoningEffort",
    "--n-concurrent", "1",
    "--n-concurrent-agents", "1",
    "--max-retries", "0",
    "--job-name", $jobName,
    "--jobs-dir", $jobsWsl,
    "--yes"
)
if ($CodexAuthJson) {
    $harborArguments += @("--agent-env", "CODEX_AUTH_JSON_PATH=$CodexAuthJson")
}

& wsl.exe -d $Distro -- env "DOCKER_CONFIG=$dockerConfigWsl" $Harbor @harborArguments
if ($LASTEXITCODE -ne 0) { throw "Harbor run failed." }

$jobWindows = Join-Path $jobsWindows $jobName
$reportWindows = Join-Path $repoRoot ".runs\reports\$jobName"
& $uvCommand.Source run --project $repoRoot python (Join-Path $repoRoot "scripts\build_run_dashboard.py") `
    --job $jobWindows `
    --output $reportWindows
if ($LASTEXITCODE -ne 0) { throw "Dashboard generation failed." }

Write-Output "Dashboard: $(Join-Path $reportWindows 'index.html')"
