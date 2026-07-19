---
title: Maximize Your Claude Code Programming Productivity
---

Course URL: https://www.linkedin.com/learning/maximize-your-claude-code-programming-productivity 

## Skills

- Prevent agent to invoke a skill:
    + `disable-model-invocation: true`: the skill will show, but not
      be invoked by the agent.
    + `user-invocable: false`: hides the skill from user, but the
      agent can still invoke it.

## Project management

- changes from sequential to blended project management, where
  traditionally, it follows the sequence of product goal, design and
  engineering, but now they are blended together, check this page 
  https://claude.com/blog/product-management-on-the-ai-exponential

- Spec-driven development: a new approach to software development that
  emphasizes the use of specifications to guide the development process.
  It is a way to ensure that the software being developed meets the
  requirements of the stakeholders and is of high quality.

- SDD standards: there are different stands regarding SDD. Here are
  some examples:
  + Kiro spec doc: https://kiro.dev/docs/specs/
  + github spec-kit: https://github.com/github/spec-kit
  + Open spec: https://openspec.dev/


- One can create a project management skill based spec-driven
  development principle, so the skill can help user to create a spec
  for a project.


- Test-driven development: a software development approach that
  emphasizes writing tests before writing the actual code. It helps
  ensure that the code meets the requirements and behaves as expected.
  Test types: unit tests, integration tests, and smoke tests.


## MCP

- github mcp server: allows users to manage their own github
  repositories, such as creating new repositories, managing issues and
  pull requests, and collaborating with other developers. 

- Datadog MCP server: allows users to monitor and manage their applications and
  infrastructure, such as setting up alerts, viewing logs, and analyzing
  performance metrics.

- Linear MCP server: allows users to manage their projects and tasks,
  such as creating new tasks, assigning tasks to team members, and
  tracking progress.

- Notion MCP server: allows users to manage their notes and documents,
  such as creating new pages, organizing pages into databases, and
  collaborating with other users.

## Agents

- Agent view: run command `claude agents` to start the mode, which
  allows one to run multiple sessions of Claude, each focusing on one
  specific task.

- Subagents: one main agent can spawn multiple subagents, each focusing on a specific
  task. The main agent can communicate with the subagents and manage
  their tasks. Benefits of using subagents include:
  + preserve context: keep the main agent's context clean while make
    exploration and implementation in subagents.
  + Enforce constraints: limiting the tools used by each sub-agent
  + Reuse subagents: if a subagent is created for a specific task, it
    can be reused for similar tasks in the future by creating
    user-level subagents.
  + Specialized behavior: make subagents focus on specific domains
    with focused system prompts.
  + Control costs: routing tasks to subagents using cheaper models
    such as Haiku.

- Create subagents: in addition to use builtin subagents such as
  exploration, one can also create their own agents. To do so, prompt
  the main agent to create a subagent with a specific name and task.
  When it is created, it will be stored under `~/.claude/agents/` with
  a markdown file containing the subagent's name, description, tools,
  and model. One can find more info on subagents at https://code.claude.com/docs/en/sub-agents

  In google's Antigravity CLI, one can create subagents in the
  following folders by creating a file agent.md:

  • Workspace-specific agent: Place the definition in  {workspace}/.agents/agents/{agent_name}/agent.md                                                                                                         
  • Global agent (across all workspaces): Place it in  ~/.gemini/config/agents/{agent_name}/agent.md

  To some extent, subagents are similar to skills in terms of
  usage/functionality.

## Rutines

One can run a task by providing a prompt on a scheduled manner, which
can be achieved via Claude cloud, Claude desktop, or the /loop command
in the CLI.

Related to this, one can use /goal command to set a goal for the
agent, and the agent will try to achieve the goal by running tasks in
a loop until the goal is achieved. Make sure the goal is achievable
and measurable.

## Hooks

Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code’s lifecycle. Use this reference to look up event schemas, configuration options, JSON input/output formats, and advanced features like async hooks, HTTP hooks, and MCP tool hooks. If you’re setting up hooks for the first time, start with the guide instead.
Check details at https://code.claude.com/docs/en/Hooks

For example, one can create a hook which is activated whenever `rm`
command is executed.






