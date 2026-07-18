param(
    [string]$ProjectDirectory = (Join-Path $PSScriptRoot "TraderFloor")
)

$ErrorActionPreference = "Stop"
$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$appDirectory = Join-Path $ProjectDirectory "app\TraderFloor"

if (-not (Test-Path -LiteralPath $appDirectory)) {
    throw "AgentCore project not found at $ProjectDirectory. Run 'agentcore create --name TraderFloor ...' first."
}

$targetPackage = Join-Path $appDirectory "trader"
if (Test-Path -LiteralPath $targetPackage) {
    Remove-Item -LiteralPath $targetPackage -Recurse -Force
}

Copy-Item -LiteralPath (Join-Path $repositoryRoot "src\trader") -Destination $targetPackage -Recurse
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "runtime.py") -Destination (Join-Path $appDirectory "main.py") -Force
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "pyproject.agentcore.toml") -Destination (Join-Path $appDirectory "pyproject.toml") -Force

Write-Host "Prepared AgentCore application at $appDirectory"
Write-Host "Run 'agentcore dev --logs' from $ProjectDirectory to test it."
