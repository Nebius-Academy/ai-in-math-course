# Week 2. Coding agents as tools for mathematical experimentation

## Practice, part 1. Exploring Cayley graph diameters with coding agents

In this task, you'll use a coding agent to find the law for the diameter of 𝑆_𝑛 w.r.t. the generators (1,2,…,𝑛) and (1,𝑛).

We suggest using **Claude Code** or **Codex**, though, we suppose, **Gemini CLI** or **Cursor** would likely also cope with it. 

The plan is::

* Generate data for 𝑛=3,…,12 (case 𝑛=12 might require C/C++/Rust; you can also try larger values of 𝑛 or just use the actual law below to get the correct numbers). A coding agent should be able to just write the code explicitly computing the diameter.
* Ask the agent to analyze the data and conjecture the law

The actual answer is:

* For odd 𝑛 ≥ 5:  (3𝑛^2−8𝑛+9)  / 4
* For even 𝑛 ≥ 6: (3𝑛^2−8𝑛+12)  / 4

Potential challenges for an AI agent:

* Clauses
* The formula doesn’t hold for 𝑛=3,4 (don't forget to supply 𝑛=3,4 data to the agent)

The agent should be able to eventually come up with the right formulas. What will be the “aha moment” when the agent will overcome these challenges?


## Practice, part 2 (optional). Exploring corner-case "super cool" sink configurations

TBD
