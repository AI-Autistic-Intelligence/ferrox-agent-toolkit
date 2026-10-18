# Ferrox Agent Toolkit - PowerShell Installer for Windows
# Installs or links the toolkit into Antigravity IDE and global AI agents

[CmdletBinding()]
param (
    [string]$Target = "antigravity",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ToolkitRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  🛡️  FERROX AGENT TOOLKIT INSTALLER (WINDOWS)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Source Toolkit Path: $ToolkitRoot" -ForegroundColor Gray

# Define Antigravity Plugin Target
$GlobalGeminiPluginDir = Join-Path $env:USERPROFILE ".gemini\config\plugins\ferrox-agent-toolkit"

Write-Host "Target Plugin Directory: $GlobalGeminiPluginDir" -ForegroundColor Yellow

if (Test-Path $GlobalGeminiPluginDir) {
    Write-Host "Existing installation found. Refreshing files..." -ForegroundColor Yellow
    Remove-Item -Path $GlobalGeminiPluginDir -Recurse -Force
}

New-Item -ItemType Directory -Path $GlobalGeminiPluginDir -Force | Out-Null

# Copy plugin files
Write-Host "Copying plugin files..." -ForegroundColor Gray
Copy-Item -Path (Join-Path $ToolkitRoot "plugin.json") -Destination $GlobalGeminiPluginDir -Force
Copy-Item -Path (Join-Path $ToolkitRoot "agents.json") -Destination $GlobalGeminiPluginDir -Force
Copy-Item -Path (Join-Path $ToolkitRoot "openpack.json") -Destination $GlobalGeminiPluginDir -Force
Copy-Item -Path (Join-Path $ToolkitRoot "README.md") -Destination $GlobalGeminiPluginDir -Force
Copy-Item -Path (Join-Path $ToolkitRoot "HANDBOOK.md") -Destination $GlobalGeminiPluginDir -Force
Copy-Item -Path (Join-Path $ToolkitRoot "AGENTS.md") -Destination $GlobalGeminiPluginDir -Force

Copy-Item -Path (Join-Path $ToolkitRoot "rules") -Destination $GlobalGeminiPluginDir -Recurse -Force
Copy-Item -Path (Join-Path $ToolkitRoot "skills") -Destination $GlobalGeminiPluginDir -Recurse -Force
Copy-Item -Path (Join-Path $ToolkitRoot "agents") -Destination $GlobalGeminiPluginDir -Recurse -Force
Copy-Item -Path (Join-Path $ToolkitRoot "scripts") -Destination $GlobalGeminiPluginDir -Recurse -Force

Write-Host "============================================================" -ForegroundColor Green
Write-Host "  ✅ FERROX AGENT TOOLKIT SUCCESSFULLY INSTALLED!" -ForegroundColor Green
Write-Host "  Location: $GlobalGeminiPluginDir" -ForegroundColor Green
Write-Host "  Antigravity IDE has immediate access to Ferrox rules & skills." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
