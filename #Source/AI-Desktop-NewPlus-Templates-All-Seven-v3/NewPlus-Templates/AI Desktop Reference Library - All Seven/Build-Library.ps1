# Windows PowerShell 5.1+; Python 3.9+; build this copied project only.
[CmdletBinding()] param()
$ErrorActionPreference='Stop'
$taskTarget = Join-Path $PSScriptRoot 'Build-Library.py'
$taskBuildArguments = @()
foreach ($taskName in @('python','python3','py')) {
  $taskCandidates = @(Get-Command $taskName -CommandType Application -ErrorAction SilentlyContinue)
  foreach ($taskPython in $taskCandidates) {
  $taskPrefix = @()
  if ($taskName -eq 'py') { $taskPrefix = @('-3') }
  $taskCompatible = $false
  try {
    & $taskPython.Source @taskPrefix -c "import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)" *> $null
    $taskCompatible = ($LASTEXITCODE -eq 0)
  } catch { $taskCompatible = $false }
  if (-not $taskCompatible) { continue }
  & $taskPython.Source @taskPrefix $taskTarget @taskBuildArguments
  if ($LASTEXITCODE -ne 0) { throw 'Guide build failed. Read the validation output.' }
  exit 0
  }
}
throw 'No compatible Python 3.9+ was found. The included HTML works without Python.'
