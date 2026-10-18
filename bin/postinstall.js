#!/usr/bin/env node
/**
 * Ferrox Agent Toolkit - Automatic Self-Installation Hook
 * 
 * Automatically scaffolds `.agents/` and `AGENTS.md` into the consumer's
 * project workspace when installed via npm, yarn, or pnpm.
 */

const fs = require('fs');
const path = require('path');

function copyRecursiveSync(src, dest) {
  if (!fs.existsSync(src)) return;
  const stats = fs.statSync(src);
  if (stats.isDirectory()) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((child) => {
      copyRecursiveSync(path.join(src, child), path.join(dest, child));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

function runAutoInstall() {
  const pkgDir = path.resolve(__dirname, '..');
  
  // 1. Detect target project directory from npm/yarn/pnpm environment
  let targetDir = process.env.INIT_CWD;

  // 2. Fallback: if inside node_modules/<package>, target is the root containing node_modules
  if (!targetDir) {
    const parts = __dirname.split(path.sep);
    const nmIndex = parts.lastIndexOf('node_modules');
    if (nmIndex !== -1) {
      targetDir = parts.slice(0, nmIndex).join(path.sep);
    }
  }

  // 3. Safety check: avoid running on self when developing the toolkit
  if (!targetDir || path.resolve(targetDir) === pkgDir) {
    return;
  }

  // Check if target directory has a package.json, Cargo.toml, pyproject.toml, or .git
  const isProjectRoot = 
    fs.existsSync(path.join(targetDir, 'package.json')) ||
    fs.existsSync(path.join(targetDir, 'Cargo.toml')) ||
    fs.existsSync(path.join(targetDir, 'pyproject.toml')) ||
    fs.existsSync(path.join(targetDir, 'composer.json')) ||
    fs.existsSync(path.join(targetDir, '.git'));

  if (!isProjectRoot) {
    return;
  }

  console.log('\n\x1b[36m[ferrox-agent-toolkit]\x1b[0m Auto-installing AI agent architecture into project...');

  const agentsDir = path.join(targetDir, '.agents');
  if (!fs.existsSync(agentsDir)) {
    fs.mkdirSync(agentsDir, { recursive: true });
  }

  // Install Layer 1 Rules
  const rulesSrc = path.join(pkgDir, 'rules');
  if (fs.existsSync(rulesSrc)) {
    copyRecursiveSync(rulesSrc, path.join(agentsDir, 'rules'));
  }

  // Install 19 Domain Skills
  const skillsSrc = path.join(pkgDir, 'skills');
  if (fs.existsSync(skillsSrc)) {
    copyRecursiveSync(skillsSrc, path.join(agentsDir, 'skills'));
  }

  // Install 10 Specialized Agents
  const agentsSrc = path.join(pkgDir, 'agents');
  if (fs.existsSync(agentsSrc)) {
    copyRecursiveSync(agentsSrc, path.join(agentsDir, 'agents'));
  }

  // Install AGENTS.md operating guide if not already customized
  const agentsMdSrc = path.join(pkgDir, 'AGENTS.md');
  const agentsMdDest = path.join(targetDir, 'AGENTS.md');
  if (fs.existsSync(agentsMdSrc) && !fs.existsSync(agentsMdDest)) {
    fs.copyFileSync(agentsMdSrc, agentsMdDest);
  }

  console.log('\x1b[32m✔ [ferrox-agent-toolkit] Successfully provisioned .agents/ and AGENTS.md in your project!\x1b[0m');
  console.log('\x1b[35m  → 10 Specialized Agents (DDD, TDD 100%, WSTG Sentinel, DevOps, Polyglot)\x1b[0m');
  console.log('\x1b[35m  → 19 Engineering Skills & Layer 1 Agile Scrum Governance active.\x1b[0m\n');
}

try {
  runAutoInstall();
} catch (err) {
  // Silent fail on permission edge cases so npm install never breaks
  // Users can always run `npx ferrox-agent init` manually
}
