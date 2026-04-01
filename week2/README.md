# Week 2. Coding agents as tools for mathematical experimentation

Papers of the week:
  * CayleyPy Growth: Efficient growth computations and hundreds of new conjectures on Cayley graphs. [Brief version](https://arxiv.org/abs/2509.19162) and [Long version](https://arxiv.org/abs/2502.18663)
  * [PrIncipal quiver Grassmannians: conjectures](https://arxiv.org/abs/2512.09731)

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

**Caution! This task is totally optional. Only approach it if you think you'll have fun with quivers. It shouldn't be too difficult from the technical point of view, but you'll have to get through some algebra**

Feel free to browse through the Linkedin articles about the quiver research:

[Part 1](https://www.linkedin.com/pulse/quiver-grassmannians-how-i-became-math-experimenter-stanislav-fedotov-ha6we/)

[Part 2](https://www.linkedin.com/pulse/ai-assisted-discovery-coding-agents-stanislav-fedotov-raone/)

The research paper: [arxiv link](http://arxiv.org/abs/2512.09731)

Let's consider a type A_n quiver 𝑄 and two dimension vectors: 𝑎 = dim⁡(𝑃⊕𝐼), 𝑑 = dim⁡(𝑃), where 𝑃 is a projective representation and 𝐼 is an injective representation. Let’s also construct a degeneration graph for the dimension vector 𝑎 and populate it with dimensions of irreducible components of the Grassmannians 𝐺𝑟(𝑀, 𝑑) for all 𝑎-dimensional representations 𝑀.

For such 𝑎 and 𝑑, the degeneration graph with likely have a prominent 𝑠𝑢𝑝𝑒𝑟 𝑐𝑜𝑜𝑙 subgraph, consisting of 𝑠𝑢𝑝𝑒𝑟 𝑐𝑜𝑜𝑙 vertices, whose Grassmannians are irreducible and of minimal dimension. The 𝑠𝑢𝑝𝑒𝑟 𝑐𝑜𝑜𝑙 𝑠𝑢𝑏𝑔𝑟𝑎𝑝ℎ will also have a single sink. 

Under “normal” conditions, the super cool sink is 𝑃⊕𝐼 itself, but in certain “insufficient” situations it will be a further degeneration of 𝑃⊕𝐼. Your task is to use **Claude Code** or **Codex** to determine:

* Which dimension vectors *a* and *d* are and “insufficient”,
* What will be the shape of the 𝑠𝑢𝑝𝑒𝑟 𝑐𝑜𝑜𝑙 𝑠𝑖𝑛𝑘 in these cases.

You'll have quite rich data here: https://drive.google.com/file/d/1WAA933tKt36X0I13NmmpLVKrHtlZkrHT/view?usp=sharing

Inside the `.zip` archive, you'll find six folders:

* `incompletes_a3` containing data about the A3 quiver: 0 -> 1 -> 2
* `incompletes_a3_sink` containing data about the A3_sink quiver: 0 -> 1 <- 2
* `incompletes_a4` containing data about the A4 quiver: 0 -> 1 -> 2 -> 3
* `incompletes_a4_sink` containing data about the A4_sink quiver: 0 -> 1 <- 2 <- 3
* `incompletes_a4_zigzag` containing data about the A4_zigzag quiver: 0 -> 1 <- 2 -> 3 <- 4
* `incompletes_a5_csink` containing data about the A5_csink quiver: 0 -> 1 -> 2 <- 3 <- 4

(The names of the particular quivers, such as "A4_zigzag" aren't official terminology.)

Inside each folder, you'll find a number of subfolders named like `3433_0321`, which means: 𝑎 = (3, 4, 3, 3), 𝑑 = (0, 3, 2, 1).

Inside each of these folders, you'll find...another subfolder, and inside of it:

* `parsed.csv` listing 𝑎-dimensional representations 𝑀 (`module` column contains them as bags of intervals such as `[1,1] + [0,2] + [0,3] + [0,3] + [3,3]`) and geometric invariants of 𝐺𝑟(𝑀, 𝑑) (you need the `irred_dims` column, which contains space-delimited dimensions of irreducible components; for example: `4 5 5`; a representation is irreducible if its `irred_dims` consist of a single number)
* `rank_poset/edges.csv` containing the edges of the degeneration graph as sources (`src` column) and targets	(`dst` column)

This information should be enough for you to determine 𝑠𝑢𝑝𝑒𝑟 𝑐𝑜𝑜𝑙 𝑠𝑖𝑛𝑘 for every configuration (𝑎, 𝑑) you can possibly find in the zip file.

**Recommendations**. 

* You can just dump the text above into the **Claude Code**'s prompt, and it should be able to start working.
* You'll totally need the `quiver` library: https://github.com/st-fedotov/quiver/tree/main, so make sure the agent installs it
* As the agent to create a **skill** for using it (just ask it nicely after installing this: https://github.com/anthropics/skills); this will make it more proficient in using the library
* The library **totally has** full functionality for creating projective and injective representations and for working with interval modules
* The actual rule isn't probabilistic: there are very clear "insufficiency" conditions, and the shape of the 𝑠𝑢𝑝𝑒𝑟 𝑐𝑜𝑜𝑙 𝑠𝑖𝑛𝑘 in these cases can be described quite clearly too. You can actually check it in the paper
* If in doubt, don't hesitate to ping Stan Fedotov

Good luck and have fun!
