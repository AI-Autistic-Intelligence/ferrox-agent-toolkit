# Ferrox Agent Toolkit - PowerShell Installer for Windows
# Installs or links the toolkit into Antigravity IDE, global AI agents, and local workspace (.agents)

[CmdletBinding()]
param (
    [string]$Target = "all", # "all", "workspace", "antigravity"
    [string]$WorkspaceDir = "c:\Users\nn\Desktop\code",
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ToolkitRoot = (Resolve-Path (Join-Path $ScriptDir "..")).Path

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  🛡️  FERROX AGENT TOOLKIT INSTALLER (WINDOWS)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Source Toolkit Path: $ToolkitRoot" -ForegroundColor Gray
Write-Host "Installation Mode:   $Target" -ForegroundColor Gray

# ------------------------------------------------------------------------------
# 1. Install / Update Global Antigravity Plugin (~/.gemini/config/plugins)
# ------------------------------------------------------------------------------
if ($Target -eq "all" -or $Target -eq "antigravity") {
    $GlobalGeminiPluginDir = Join-Path $env:USERPROFILE ".gemini\config\plugins\ferrox-agent-toolkit"
    Write-Host "`n[1/2] Installing to Global Antigravity Plugin Directory..." -ForegroundColor Yellow
    Write-Host "Target: $GlobalGeminiPluginDir" -ForegroundColor Gray

    if (Test-Path $GlobalGeminiPluginDir) {
        Remove-Item -Path $GlobalGeminiPluginDir -Recurse -Force
    }

    New-Item -ItemType Directory -Path $GlobalGeminiPluginDir -Force | Out-Null

    Copy-Item -Path (Join-Path $ToolkitRoot "plugin.json") -Destination $GlobalGeminiPluginDir -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "agents.json") -Destination $GlobalGeminiPluginDir -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "openpack.json") -Destination $GlobalGeminiPluginDir -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "README.md") -Destination $GlobalGeminiPluginDir -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "HANDBOOK.md") -Destination $GlobalGeminiPluginDir -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "AGENTS.md") -Destination $GlobalGeminiPluginDir -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "LICENSE") -Destination $GlobalGeminiPluginDir -Force

    Copy-Item -Path (Join-Path $ToolkitRoot "rules") -Destination $GlobalGeminiPluginDir -Recurse -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "skills") -Destination $GlobalGeminiPluginDir -Recurse -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "agents") -Destination $GlobalGeminiPluginDir -Recurse -Force
    Copy-Item -Path (Join-Path $ToolkitRoot "scripts") -Destination $GlobalGeminiPluginDir -Recurse -Force

    Write-Host "  -> Global Antigravity Plugin successfully refreshed." -ForegroundColor Green
}

# ------------------------------------------------------------------------------
# 2. Install / Link to Workspace Root ($WorkspaceDir / .agents)
# ------------------------------------------------------------------------------
if ($Target -eq "all" -or $Target -eq "workspace") {
    Write-Host "`n[2/2] Installing to Workspace Directory..." -ForegroundColor Yellow
    Write-Host "Workspace Root: $WorkspaceDir" -ForegroundColor Gray

    if (-not (Test-Path $WorkspaceDir)) {
        New-Item -ItemType Directory -Path $WorkspaceDir -Force | Out-Null
    }

    $WorkspaceAgentsDir = Join-Path $WorkspaceDir ".agents"
    if (-not (Test-Path $WorkspaceAgentsDir)) {
        New-Item -ItemType Directory -Path $WorkspaceAgentsDir -Force | Out-Null
    }

    # Setup Junctions for live synchronization between ferrox-agent-toolkit and .agents
    $Junctions = @(
        @{ Name = "rules";  Source = (Join-Path $ToolkitRoot "rules") },
        @{ Name = "skills"; Source = (Join-Path $ToolkitRoot "skills") },
        @{ Name = "agents"; Source = (Join-Path $ToolkitRoot "agents") }
    )

    foreach ($j in $Junctions) {
        $DestPath = Join-Path $WorkspaceAgentsDir $j.Name
        if (Test-Path $DestPath) {
            # Remove existing directory/junction
            cmd /c "rmdir `"$DestPath`" 2>nul" | Out-Null
            if (Test-Path $DestPath) {
                Remove-Item -Path $DestPath -Recurse -Force -ErrorAction SilentlyContinue
            }
        }
        # Create NTFS Junction for instant live updates
        try {
            New-Item -ItemType Junction -Path $DestPath -Target $j.Source -Force | Out-Null
            Write-Host "  -> Linked .agents/$($j.Name) -> $($j.Source)" -ForegroundColor Green
        } catch {
            Copy-Item -Path $j.Source -Destination $DestPath -Recurse -Force
            Write-Host "  -> Copied .agents/$($j.Name)" -ForegroundColor Green
        }
    }

    # Copy root operating guide AGENTS.md to workspace root
    Copy-Item -Path (Join-Path $ToolkitRoot "AGENTS.md") -Destination (Join-Path $WorkspaceDir "AGENTS.md") -Force
    Write-Host "  -> Copied AGENTS.md to workspace root: $(Join-Path $WorkspaceDir 'AGENTS.md')" -ForegroundColor Green
}

Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "  ✅ FERROX AGENT TOOLKIT FULLY INSTALLED!" -ForegroundColor Green
Write-Host "  All repositories under $WorkspaceDir have direct access to:" -ForegroundColor Green
Write-Host "  - 19 Rules (.agents/rules/)" -ForegroundColor Green
Write-Host "  - 19 Skills (.agents/skills/)" -ForegroundColor Green
Write-Host "  - 10 Specialized Agents (.agents/agents/)" -ForegroundColor Green
Write-Host "  - Operating Guide ($WorkspaceDir\AGENTS.md)" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
