# Agent Skills: A Comprehensive Guide

## Table of Contents
1. [What is an Agent Skill?](#what-is-an-agent-skill)
2. [Triggering Skills in Different Interfaces](#triggering-skills-in-different-interfaces)
3. [Creating Your Own Skills](#creating-your-own-skills)
4. [Popular Skills Repositories](#popular-skills-repositories)
5. [Installing Skills with npx](#installing-skills-with-npx)

---

## What is an Agent Skill?

Agent skills are **reusable instruction sets** that extend AI agents' capabilities. They provide specialized knowledge and workflows to help AI assistants perform specific tasks more effectively, such as generating release notes, conducting code reviews, integrating with external tools, or following team conventions.

### Basic Format

Skills are defined in a `SKILL.md` file with YAML frontmatter. Here's the basic structure:

```markdown
---
name: example-skill
description: A brief description of what this skill does and when to use it.
---

# Example Skill

## Purpose
Describe what this skill helps accomplish.

## Instructions
Step-by-step instructions for the AI agent to follow when executing this skill.

## Examples
Provide concrete examples of how to use this skill.
```

**Required fields:**
- `name`: 1-64 characters, lowercase letters, numbers, and hyphens only
- `description`: 1-1024 characters describing what the skill does and when to use it

**Optional fields:**
- `license`: License name or reference
- `compatibility`: Environment requirements (max 500 characters)
- `metadata`: Additional key-value pairs (author, version, etc.)
- `allowed-tools`: Pre-approved tools the skill may use

Note that this file must be placed in a folder named after the skill (e.g., `example-skill/SKILL.md`) and can be located in various directories like `.agent-skills/`, `skills/`, or `.claude/skills/` depending on the agent.

### Simple Example

Here's a complete example of a skill for generating release notes:

````markdown
---
name: release-notes
description: Generate structured release notes from git commits. Use when creating changelogs, preparing releases, or when the user mentions release notes or changelog.
license: MIT
metadata:
  author: example-org
  version: "1.0"
---

# Release Notes Generator

## Purpose
Generate professional release notes by analyzing git commits between versions.

## Instructions
1. Fetch commits between the last tag and HEAD using git log
2. Categorize commits by type (feat, fix, docs, refactor, etc.)
3. Group related changes under appropriate sections
4. Format as markdown with proper headings
5. Highlight breaking changes prominently at the top

## Output Format
```
## [Version X.Y.Z] - YYYY-MM-DD

### ⚠️ Breaking Changes
- Breaking change descriptions

### ✨ New Features
- Feature descriptions

### 🐛 Bug Fixes
- Bug fix descriptions

### 📚 Documentation
- Documentation updates
```

## Examples

### Example: Generate notes from v1.0.0 to HEAD
```bash
git log v1.0.0..HEAD --oneline
```
Then categorize and format the output.
````

---

## Triggering Skills in Different Interfaces

Different AI coding agents support skills in various ways:

### VS Code Extensions

**GitHub Copilot:**
- Skills can be activated using natural language in comments
- Reference skills by mentioning their trigger keywords
- Example: `// @workspace use release-notes skill to generate changelog`

**Cursor:**
- Use the chat interface with trigger keywords
- Skills auto-activate based on context
- Command: Type the skill name or trigger in the chat panel
- Example: "Use the release-notes skill for the latest version"

### Claude Code (CLI)

- Skills are automatically discovered in the project or global skills directory
- Trigger by mentioning the skill name or trigger keywords in prompts
- Use slash commands if the skill registers one
- Example: `/release-notes` or "Generate release notes using the release-notes skill"
- Skills can be project-specific (`.agent-skills/` or `.claude/skills/`) or global (`~/.config/claude/skills/`)

### Gemini CLI

- Gemini-based agents support skills through natural language triggers
- Reference the skill in your prompt
- Example: `gemini "create release notes using the changelog skill"`

### Qwen-Code

- Skills work through contextual awareness
- Mention the skill name or related keywords in your coding session
- The agent will automatically apply relevant skills based on the task

### Windsurf

- Skills are activated via the chat interface
- Supports the standard SKILL.md format
- Use trigger keywords in your prompts
- Example: "Apply the code review skill to this PR"

### General Activation Pattern

Most modern AI coding agents follow this pattern:
1. **Auto-discovery**: Skills in `.agent-skills/`, `skills/`, or similar directories are automatically loaded
2. **Keyword activation**: Mentioning trigger keywords or the skill name activates it
3. **Slash commands**: Some skills register slash commands for direct invocation
4. **Context-aware**: Skills may activate automatically based on file types or project structure

---

## Creating Your Own Skills

### Step 1: Create the SKILL.md File

Create a file named `SKILL.md` in your skills directory:

```bash
mkdir -p .agent-skills/my-custom-skill
cd .agent-skills/my-custom-skill
touch SKILL.md
```

### Step 2: Define the Frontmatter

Add YAML frontmatter with metadata:

```yaml
---
name: my-custom-skill
description: Custom skill for [specific purpose]. Use when [describe when to activate this skill].
license: MIT
metadata:
  author: Your Name
  version: "1.0"
---
```

The `name` must match the directory name and follow naming rules (lowercase, hyphens only, no consecutive hyphens). The `description` should clearly explain both what the skill does and when to use it.

### Step 3: Write Clear Instructions

Provide detailed instructions for the AI agent:

```markdown
# My Custom Skill

## Purpose
Clearly state what problem this skill solves.

## Prerequisites
List any required tools, dependencies, or setup.

## Instructions
1. First step with specific details
2. Second step with examples
3. Third step with expected outcomes

## Best Practices
- Key principle 1
- Key principle 2
- Common pitfalls to avoid

## Examples

### Example 1: Basic Usage
[Show a simple example]

### Example 2: Advanced Usage
[Show a more complex scenario]

## Validation
How to verify the skill worked correctly.
```

### Step 4: Test Your Skill

1. Place the skill in a discoverable location
2. Restart your AI agent or reload skills
3. Test by using trigger keywords
4. Iterate based on results

### Best Practices for Skill Creation

- **Be specific**: Clear, actionable instructions work best
- **Include examples**: Show concrete use cases
- **Define scope**: State what the skill does and doesn't do
- **Use triggers wisely**: Choose distinctive, memorable keywords
- **Version your skills**: Track changes and improvements
- **Test thoroughly**: Verify the skill works across different scenarios
- **Document limitations**: Be upfront about edge cases or constraints

---

## Popular Skills Repositories

### 1. [skills.sh](https://skills.sh/)

**Overview**: The largest open agent skills ecosystem with a centralized marketplace.

**Features**:
- **443,000+ installs** of popular skills
- Leaderboard showing trending and popular skills
- Skills across multiple domains: web development, marketing, cloud services, design, testing
- One-command installation
- Supports Claude Code, GitHub Copilot, Gemini, Cursor, and many more

**Top Skills**:
- `find-skills`: Discover new skills
- Web development workflows
- Azure and AWS cloud integrations
- Marketing and content generation
- Project management helpers

**Installation**: `npx skills add <owner/repo>`

### 2. [Vercel Labs Skills](https://github.com/vercel-labs/skills)

**Overview**: Official skills repository from Vercel Labs, demonstrating the standard format.

**Features**:
- Reference implementation of the SKILL.md format
- High-quality, production-ready skills
- Well-documented examples
- Active maintenance and community contributions

**Use Cases**:
- Release note generation
- PR creation with conventions
- Integration patterns
- Deployment workflows

### 3. [Posit Dev Skills](https://github.com/posit-dev/skills)

**Overview**: Skills developed by Posit for data science and R/Python development workflows.

**Features**:
- Domain-specific expertise for R packages, Shiny, and Quarto
- Automatic skill activation based on context
- MIT licensed and open source
- Multi-platform support (Claude Code, Claude.ai, Claude API)

**Notable Skills**:
- `critical-code-reviewer`: Rigorous code review workflows
- `release-post`: Professional package release blog posts
- `shiny-bslib`: Modern Shiny dashboard development
- GitHub integration skills
- R package development helpers

### 4. [Hoodini AI Agent Skills](https://github.com/hoodini/ai-agents-skills)

**Overview**: Curated collection by Yuval Avidani focusing on production-ready patterns and organizational knowledge.

**Features**:
- Specialized knowledge modules for multiple AI agents
- Quick activation via trigger keywords
- Reusable across platforms (GitHub Copilot, Claude Code, Cursor, Windsurf)
- Security and accessibility patterns

**Notable Skills**:
- Google Workspace CLI
- Honest Agent Configuration
- AWS Agent Development
- Vercel and Cloudflare deployment
- Security best practices
- Accessibility patterns

**Philosophy**: "Supercharge your AI coding agents with specialized knowledge and production-ready patterns"

### Comparison Table

| Repository | Focus | Skill Count | Best For |
|------------|-------|-------------|----------|
| skills.sh | Marketplace | 400+ | Discovery & variety |
| Vercel Labs | Reference impl | ~10-20 | Learning standards |
| Posit Dev | Data science | ~10-15 | R/Python/Shiny |
| Hoodini | Enterprise | ~20-30 | Production patterns |

---

## Installing Skills with npx

The `npx skills` command provides a streamlined way to discover, install, and manage agent skills.

### Usage Examples

```bash
# Install all skills from a GitHub repository
npx skills add vercel-labs/agent-skills

# Install from skills.sh ecosystem (owner/repo format)
npx skills add username/skillname

# Install a specific skill from a repository
npx skills add vercel-labs/agent-skills --skill release-notes

# Install globally for all projects
npx skills add vercel-labs/agent-skills --global

# Install for a specific agent
npx skills add vercel-labs/agent-skills --agent claude-code

# List available skills before installing
npx skills add vercel-labs/agent-skills --list

# Install from a local directory
npx skills add ./path/to/local/skills

# Install from a GitHub URL
npx skills add https://github.com/username/skills-repo
```

### Command Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--global` | `-g` | Install to user directory (~/.config/[agent]/skills/) | `npx skills add repo -g` |
| `--agent` | `-a` | Target specific agent (claude-code, cursor, etc.) | `npx skills add repo -a cursor` |
| `--skill` | `-s` | Install specific skill(s) only | `npx skills add repo -s skill-name` |
| `--list` | | List available skills in repository | `npx skills add repo --list` |

**Supported agents:** `claude-code`, `cursor`, `github-copilot`, `opencode`, `windsurf`

### Skill Discovery Process

When you run `npx skills add`, the tool:

1. **Searches multiple directories** within the repository:
   - `skills/`
   - `.agent-skills/`
   - `.agents/skills/`
   - `.claude/skills/`
   - Root directory

2. **Locates SKILL.md files** in these directories

3. **Validates the skill format** (YAML frontmatter + markdown)

4. **Copies to target location**:
   - Project-level: `.agent-skills/` or `.claude/skills/`
   - Global: `~/.config/[agent]/skills/`

5. **Registers skills** with the agent for auto-discovery

### Quick Tips

**Verify installation:**
```bash
ls -la .agent-skills/                    # Project-level skills
ls -la ~/.config/claude/skills/          # Claude Code global skills
```

**Update a skill:**
```bash
rm -rf .agent-skills/skill-name && npx skills add repo --skill skill-name
```

**Validate your skills:**
```bash
npx skills-ref validate ./my-skill       # Requires skills-ref library
```

---

## Conclusion

Agent skills represent a powerful paradigm for extending AI coding assistants with specialized knowledge and workflows. By leveraging the simple SKILL.md format, developers can:

- Share expertise across teams and projects
- Standardize workflows and conventions
- Accelerate development with reusable patterns
- Build organizational knowledge bases
- Enhance AI agent capabilities without vendor lock-in

The ecosystem is rapidly growing with repositories like skills.sh, Vercel Labs, Posit Dev, and Hoodini providing hundreds of production-ready skills. The `npx skills` command makes discovery and installation seamless across different AI agents.

Whether you're creating custom skills for your team or leveraging community-contributed ones, agent skills provide a flexible, open standard for augmenting your AI-powered development workflow.

---

## Additional Resources

- [Vercel Labs Skills Repository](https://github.com/vercel-labs/skills) - Official implementation and examples
- [Skills.sh Marketplace](https://skills.sh/) - Browse and discover skills
- [Posit Skills](https://github.com/posit-dev/skills) - Data science focused skills, particularly for R users
- [Hoodini AI Agent Skills](https://github.com/hoodini/ai-agents-skills) - Another introduction on agent skills and a list of production-ready skills
- [SKILL.md Format Specification](https://agentskills.io/specification) - Detailed documentation on the skill format and best practices

## Contributing

Most skills repositories welcome contributions. To contribute:

1. Fork the repository
2. Create a new skill following the SKILL.md format
3. Test thoroughly with multiple agents
4. Submit a pull request with documentation

---

*Last updated: March 2026*
