#!/usr/bin/env node
/**
 * Ferrox Agent Toolkit CLI
 * 
 * Autonomous Dual-Layer Agile Scrum & DDD engineering architecture for AI agents.
 * 
 * Copyright (c) 2026 AI Autistic Intelligence. Licensed under MIT.
 */

const fs = require('fs');
const path = require('path');

const VERSION = '0.1.1';
const ROOT_DIR = path.resolve(__dirname, '..');

const HELP_TEXT = `
Ferrox Agent Toolkit CLI v${VERSION}
High-performance dual-layer AI agent architecture for modern polyglot engineering.

USAGE:
  ferrox-agent <command> [options]

COMMANDS:
  init [path]       Install / scaffold Ferrox agents and rules into a target workspace
  list              List all 10 specialized agents and 19 domain skills
  rules             Display the core Ferrox Master Operating Guide (AGENTS.md)
  verify            Verify toolkit integrity and directory layout
  version, -v       Show version
  help, -h          Show this help message

EXAMPLES:
  npx ferrox-agent init ./my-project
  npx ferrox-agent list
  npx ferrox-agent rules
`;

function copyRecursiveSync(src, dest) {
  const exists = fs.existsSync(src);
  const stats = exists && fs.statSync(src);
  const isDirectory = exists && stats.isDirectory();
  if (isDirectory) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach((childItemName) => {
      copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}

function handleInit(targetPath) {
  const target = path.resolve(process.cwd(), targetPath || '.');
  console.log(`\x1b[36mInitializing Ferrox Agent Toolkit in: ${target}\x1b[0m`);

  const agentsDir = path.join(target, '.agents');
  if (!fs.existsSync(agentsDir)) {
    fs.mkdirSync(agentsDir, { recursive: true });
  }

  // Copy rules and skills
  const rulesSrc = path.join(ROOT_DIR, 'rules');
  const skillsSrc = path.join(ROOT_DIR, 'skills');
  const agentsSrc = path.join(ROOT_DIR, 'agents');
  const agentsMdSrc = path.join(ROOT_DIR, 'AGENTS.md');

  if (fs.existsSync(rulesSrc)) {
    console.log('  -> Installing Layer 1 governance rules...');
    copyRecursiveSync(rulesSrc, path.join(agentsDir, 'rules'));
  }
  if (fs.existsSync(skillsSrc)) {
    console.log('  -> Installing 19 domain engineering skills...');
    copyRecursiveSync(skillsSrc, path.join(agentsDir, 'skills'));
  }
  if (fs.existsSync(agentsSrc)) {
    console.log('  -> Installing 10 specialized agent specs...');
    copyRecursiveSync(agentsSrc, path.join(agentsDir, 'agents'));
  }
  if (fs.existsSync(agentsMdSrc)) {
    const agentsMdDest = path.join(target, 'AGENTS.md');
    if (!fs.existsSync(agentsMdDest)) {
      console.log('  -> Installing AGENTS.md operating guide...');
      fs.copyFileSync(agentsMdSrc, agentsMdDest);
    }
  }

  console.log('\x1b[32m✔ Ferrox Agent Toolkit successfully initialized!\x1b[0m');
  console.log('Your AI coding agents now have access to pure DDD, 100% TDD, and WSTG Sentinel security.\n');
}

function handleList() {
  console.log('\x1b[35m=== Ferrox Agent Toolkit Roster ===\x1b[0m\n');
  
  const agentsPath = path.join(ROOT_DIR, 'agents');
  if (fs.existsSync(agentsPath)) {
    console.log('\x1b[33m[Specialized Agents (10)]:\x1b[0m');
    const files = fs.readdirSync(agentsPath).filter(f => f.endsWith('.md'));
    files.forEach(f => {
      console.log(`  • ${f.replace('.md', '')}`);
    });
    console.log('');
  }

  const skillsPath = path.join(ROOT_DIR, 'skills');
  if (fs.existsSync(skillsPath)) {
    console.log('\x1b[34m[Domain Skills (19)]:\x1b[0m');
    const skills = fs.readdirSync(skillsPath);
    skills.forEach(s => {
      console.log(`  • ${s}`);
    });
    console.log('');
  }
}

function handleRules() {
  const agentsMdPath = path.join(ROOT_DIR, 'AGENTS.md');
  if (fs.existsSync(agentsMdPath)) {
    console.log(fs.readFileSync(agentsMdPath, 'utf8'));
  } else {
    console.error('AGENTS.md not found in toolkit root.');
  }
}

function handleVerify() {
  console.log('\x1b[36mVerifying Ferrox Agent Toolkit integrity...\x1b[0m');
  const required = ['rules', 'skills', 'agents', 'AGENTS.md', 'plugin.json', 'openpack.json'];
  let allOk = true;

  for (const item of required) {
    const p = path.join(ROOT_DIR, item);
    if (fs.existsSync(p)) {
      console.log(`  \x1b[32m✔\x1b[0m ${item}`);
    } else {
      console.log(`  \x1b[31m✖ Missing:\x1b[0m ${item}`);
      allOk = false;
    }
  }

  if (allOk) {
    console.log('\x1b[32mAll core components verified.\x1b[0m');
  } else {
    process.exit(1);
  }
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';

  switch (command) {
    case 'init':
      handleInit(args[1]);
      break;
    case 'list':
      handleList();
      break;
    case 'rules':
      handleRules();
      break;
    case 'verify':
      handleVerify();
      break;
    case 'version':
    case '-v':
    case '--version':
      console.log(`ferrox-agent v${VERSION}`);
      break;
    case 'help':
    case '-h':
    case '--help':
    default:
      console.log(HELP_TEXT);
      break;
  }
}

main();
