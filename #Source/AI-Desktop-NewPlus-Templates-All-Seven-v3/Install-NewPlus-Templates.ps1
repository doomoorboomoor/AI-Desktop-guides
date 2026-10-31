# Windows PowerShell 5.1+; installs direct New+ template entries, not the enclosing folder.
[CmdletBinding(SupportsShouldProcess=$true)]
param(
  [string]$TemplatesPath = (Join-Path $env:LOCALAPPDATA 'Microsoft\PowerToys\NewPlus\Templates'),
  [switch]$Overwrite,
  [switch]$IncludeDated
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-TemplateSHA256 {
  param([string]$TaskFilePath)
  $taskHasher = [System.Security.Cryptography.SHA256]::Create()
  $taskStream = [System.IO.File]::OpenRead($TaskFilePath)
  try { return ([System.BitConverter]::ToString($taskHasher.ComputeHash($taskStream))).Replace('-', '') }
  finally { $taskStream.Dispose(); $taskHasher.Dispose() }
}

$src = Join-Path $PSScriptRoot 'NewPlus-Templates'
$dated = Join-Path $PSScriptRoot 'Optional-Dated-Templates'
if (-not (Test-Path -LiteralPath $src -PathType Container)) {throw 'Extract the entire ZIP first. NewPlus-Templates/ was not found.'}
if ([string]::IsNullOrWhiteSpace($TemplatesPath)) { throw 'TemplatesPath cannot be empty.' }
$dest = [System.IO.Path]::GetFullPath($TemplatesPath)
if ($dest.TrimEnd('\') -eq ([System.IO.Path]::GetFullPath($src)).TrimEnd('\')) { throw 'Destination cannot be package source.' }
$items = @(Get-ChildItem -LiteralPath $src -Force)
if ($IncludeDated) {
  if (-not (Test-Path -LiteralPath $dated -PathType Container)) { throw 'Optional dated templates missing.' }
  $items += @(Get-ChildItem -LiteralPath $dated -Force)
}
if (-not (Test-Path -LiteralPath $dest)) {
  if ($PSCmdlet.ShouldProcess($dest, 'Create New+ templates directory')) {
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
  }
}
$installed=0; $skipped=0
foreach ($item in $items) {
  $out = Join-Path $dest $item.Name
  if ((Test-Path -LiteralPath $out) -and (-not $Overwrite)) {
    Write-Host ('SKIP existing: ' + $item.Name) -ForegroundColor Yellow
    $skipped++; continue
  }
  if (-not $PSCmdlet.ShouldProcess($out, 'Install/replace PowerToys New+ template')) {continue}
  if (Test-Path -LiteralPath $out) {
    $backupBase = Join-Path $env:LOCALAPPDATA ('Microsoft\PowerToys\NewPlus\TemplateBackups\' + [Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $backupBase -Force | Out-Null
    Copy-Item -LiteralPath $out -Destination (Join-Path $backupBase $item.Name) -Recurse -Force
    Write-Host ('BACKUP: ' + $item.Name + ' -> ' + $backupBase) -ForegroundColor Cyan
    Remove-Item -LiteralPath $out -Force -Recurse
  }
  Copy-Item -LiteralPath $item.FullName -Destination $out -Recurse -Force
  $files = if ($item.PSIsContainer) {@(Get-ChildItem -LiteralPath $item.FullName -File -Recurse -Force)} else {@($item)}
  foreach ($file in $files) {
    $rel = if ($item.PSIsContainer) {$file.FullName.Substring($item.FullName.Length).TrimStart('\','/')} else {''}
    $target = if ($item.PSIsContainer) {Join-Path $out $rel} else {$out}
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {throw ('Verification failed: missing ' + $target)}
    if ((Get-TemplateSHA256 -TaskFilePath $file.FullName) -ne (Get-TemplateSHA256 -TaskFilePath $target)) {
      throw ('Verification failed: SHA-256 mismatch ' + $target)
    }
  }
  if ($item.PSIsContainer) {
    foreach ($name in @('#Old','#Temp')) {
      if (-not (Test-Path -LiteralPath (Join-Path $out $name) -PathType Container)) {
        throw ('Verification failed: missing ' + $name + ' in ' + $item.Name)
      }
    }
  }
  Write-Host ('OK installed: ' + $item.Name) -ForegroundColor Green
  $installed++
}
Write-Host ("`nNew+ templates path: " + $dest)
Write-Host ('Installed: ' + $installed + '; skipped: ' + $skipped)
Write-Host 'In PowerToys Settings, enable New+. Right-click inside a folder > New+.'
if ($IncludeDated) { Write-Host 'Enable New+ > Replace variables in template filename for the dated template.' }
