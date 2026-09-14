---
name: grilling
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree **one question at a time**. The **frontier** is every decision whose prerequisites are already settled, the questions you could ask _now_ without guessing at answers you haven't heard yet. Each turn, pick the single most load-bearing question on the frontier (the one the most downstream decisions hang off), ask it with your recommended answer, and wait for the user's reply before asking the next. Never ask two questions in one message. Number questions sequentially across the whole session (Q1, Q2, ...).

Each question should be formatted like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each answer reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier after every answer and pick the next question. A question whose answer depends on the one currently open waits its turn.

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), dispatch a sub-agent to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so a question downstream of it waits for the sub-agent to report, and you ask a frontier question that doesn't depend on it in the meantime. The _decisions_ are the user's. Put each to them and wait.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
