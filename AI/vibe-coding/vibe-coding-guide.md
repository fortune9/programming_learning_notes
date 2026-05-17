---
title: Vibe Coding Guide
description: A guide for coding using AI
author: "Zhenguo Zhang"
date: 2026-05-17
---

## Background

[Vibe coding](https://en.wikipedia.org/wiki/Vibe_coding) has become increasingly popular since 2025 due to the
advancements in AI technology, particularly [AI agents](https://en.wikipedia.org/wiki/AI_agent). With this new
framework, it seems that anyone can code, even without any
programming knowledge.

## The Pain

As a bioinformatics scientist, I have been using vibe coding for a
while. However, I have found the following problems:

- It is easy to generate code that you don't want; for example, the
  code is not efficient, or it is wrong in edge cases.

- For simple tasks, AI is trapped into a loop of generating very
  complicated code. The code is not straightforward for the task.

- The code lacks clear strategic architectural design, which makes it hard to maintain and
  extend.

- As development goes on, the context for coding becomes lengthy and
  loses focus, which makes it hard for AI to generate code that is
  relevant to the current task.

## The Solution

To address these issues, I have developed a set of guidelines for vibe
coding based on my experience and reading:

- **Architecture first**: Before any coding, check whether a task is
  simple enough to be solved by a single function. If not, design the
  architecture first, make subtasks modular and clear, and then code
  each subtask.

- **Start small**: Implement each subtask with simple and
  straightforward code; don't add features not asked for.

- **Modularize the code**: Make code modular by putting code into functions and classes, which can help improve
  the readability and maintainability of the code.

- **Use references**: When coding, use references such as documentation, examples, and
  best practices to ensure that the code is efficient and follows
  industry standards. Ask for references if you can't find them.

- **Explain the code**: Add comments to explain the code, starting with high-level strategy and then details for implementation.

- **Test before moving on**: After each function, class, module, or
  subtask is implemented, test it before moving on to the next one.
  This can help catch any errors early and ensure that the code is
  working as expected.

- **Edit code**: Don't change adjacent code and comments when editing
  existing code; don't refactor things that aren't broken; remove
  unused imports, variables, and functions after the code is working; add
  comments to explain why the code is written in a certain way,
  especially when the code is not straightforward.

- **Keep the context clean**: As development goes on, the context for
  coding becomes lengthy and loses focus. To avoid this, keep the
  context clean by removing irrelevant information and focusing on the
  current task. Use [subagents](https://docs.anthropic.com/en/docs/agents-and-tools) to handle subtasks to avoid
  context contamination.

- **Ask if any uncertainty**: During planning and coding, if any
  uncertainty arises, ask for clarification immediately. This can help
  avoid generating code that is not relevant or efficient.


## Related Resources

- **[Skills for Real Engineers](https://github.com/mattpocock/skills)**: A collection of skills for real engineers, small but effective.
- **[Karpathy-Inspired Claude Code Guidelines](https://github.com/multica-ai/andrej-karpathy-skills)**: A set of
  high-level guidelines for writing code with AI, inspired by Andrej
  Karpathy's approach to coding.
- **[How to Vibe Coding](https://www.youtube.com/watch?v=ytT4-lGEf6A)**: A video showing how to use AI agents to develop a Super Mario Bros
  game.




