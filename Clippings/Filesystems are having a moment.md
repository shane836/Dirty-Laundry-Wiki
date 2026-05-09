---
title: "Filesystems are having a moment"
source: "https://madalitso.me/notes/why-everyone-is-talking-about-filesystems/"
author:
published: 2026-02-22
created: 2026-05-09
description: "a digital garden by daniel phiri"
tags:
  - "clippings"
---
🌱 - A collection of sprouting thoughts.

![](https://madalitso.me/images/file.png)

I used to work at a vector database company. My entire job was helping people understand why they needed a database purpose-built for AI; embeddings, semantic search, the whole thing. So it's a little funny that I'm writing this. But here I am, watching everyone in the AI ecosystem suddenly rediscover the humble filesystem, and I think they might be onto something bigger than most people realize.

Not bigger than databases. Different from databases. I need to say that upfront because I already know someone is going to read this and think I'm saying "files good, databases bad." I'm not. Stay with me.

#### Everyone is talking about files

If you've been paying any attention to the AI agent space over the last few months, you've noticed something strange. [LlamaIndex](https://www.llamaindex.ai/blog/files-are-all-you-need) published "Files Are All You Need." [LangChain](https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/) wrote about how agents can use filesystems for context engineering. [Oracle](https://blogs.oracle.com/developers/comparing-file-systems-and-databases-for-effective-ai-agent-memory-management), *yes Oracle (who is cooking btw)*, put out a piece comparing filesystems and databases for agent memory. [Dan Abramov](https://overreacted.io/a-social-filesystem/) wrote about a social filesystem built on the AT Protocol. [Archil](https://archil.com/post/why-file-systems-are-here-to-stay) is building cloud volumes specifically because agents want POSIX file systems.

Jerry Liu from LlamaIndex put it bluntly: instead of one agent with hundreds of tools, we're moving toward a world where the agent has access to a filesystem and maybe 5-10 tools. That's it. Filesystem, code interpreter, web access. And that's as general, if not more general than an agent with 100+ MCP tools.

[Karpathy](https://karpathy.bearblog.dev/year-in-review-2025/) made the adjacent observation that stuck with me. He pointed out that Claude Code works because it runs on your computer, with your environment, your data, your context. It's not a website you go to — it's a little *spirit* that lives on your machine. OpenAI got this wrong, he argued, by focusing on cloud deployments in containers orchestrated from ChatGPT instead of simply running on localhost.

And here's the thing that makes all of this matter commercially: coding agents make up the majority of actual AI use cases right now. Anthropic is reportedly approaching profitability, and a huge chunk of that is driven by Claude Code, a CLI tool. Not a chatbot. A tool that reads and writes files on your filesystem.

![](https://madalitso.me/images/window.png)

#### Context windows aren't memory

Here's where I think most of the discourse misses the deeper point.

Memory; in the human, psychological sense is fundamental to how we function. We don't re-read our entire life story every time we make a decision. We have long-term storage, selective recall, the ability to forget things that don't matter and surface things that do. Context windows in LLMs are none of that. They're more like a whiteboard that someone keeps erasing.

If you've used Claude Code for any real project, you know the dread of watching that "context left until auto-compact" notification creep closer. Your entire conversation, all the context the agent has built up about your codebase, your preferences, your decisions about to be compressed or lost.

Filesystems solve this in the most boring, obvious way possible. Write things down. Put them in files. Read them back when you need them. Claude's `CLAUDE.md` file gives the agent persistent context about your project. Cursor stores past chat history as searchable files. People are writing `aboutme.md` files that act as portable identity descriptors any agent can read i.e. your preferences, your skills, your working style, all in a file that moves between applications without anyone needing to coordinate an API.

Except! It might not be quite that simple.

A [recent paper from ETH Zürich](https://arxiv.org/abs/2602.11988) evaluated whether these repository-level context files actually help coding agents complete tasks. The finding was counterintuitive: across multiple agents and models, context files tended to *reduce* task success rates while increasing inference cost by over 20%. Agents given context files explored more broadly, ran more tests, traversed more files — but all that thoroughness delayed them from actually reaching the code that needed fixing. The files acted like a checklist that agents took too seriously.

This sounds like it undermines the whole premise. But I think it actually sharpens it. The paper's conclusion wasn't "don't use context files." It was that **unnecessary requirements make tasks harder, and context files should describe only minimal requirements.** The problem isn't the filesystem as a persistence layer. The problem is people treating `CLAUDE.md` like a 2,000-word onboarding document instead of a concise set of constraints. Which brings us to the question of standards.

![](https://madalitso.me/images/web.png)

#### The file format is the API (but which file?)

Right now we have `CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`, `.cursorrules`, and probably five more by the time you read this. Everyone agrees that agents need persistent filesystem-based context. Nobody agrees on what the file should be called or what should go in it. I see efforts to consolidate, this is good.

Dan Abramov's piece on a [social filesystem](https://overreacted.io/a-social-filesystem/) crystallized something important here. He describes how the AT Protocol treats user data as files in a personal repository; structured, owned by the user, readable by any app that speaks the format. The critical design choice is that different apps don't need to agree on what a "post" is. They just need to namespace their formats (using domain names, like Java packages) so they don't collide. Apps are reactive to files. Every app's database becomes derived data i.e. a cached materialized view of everybody's folders.

The same tension exists in the agent context file space. We don't need `CLAUDE.md` and `AGENTS.md` and `copilot-instructions.md` to converge into one file. We need them to coexist without collision. And to be fair, some convergence is happening. Anthropic released [Agent Skills](https://agentskills.io/) as an open standard, a `SKILL.md` format that Microsoft, OpenAI, Atlassian, GitHub, and Cursor have all adopted. A skill you write for Claude Code works in Codex, works in Copilot. The file format *is* the API.

[NanoClaw](https://github.com/qwibitai/nanoclaw), a lightweight personal AI assistant framework, takes this to its logical conclusion. Instead of building an ever-expanding feature set, it uses a "skills over features" model. Want Telegram support? There's no Telegram module. There's a `/add-telegram` skill, essentially a markdown file that teaches Claude Code how to rewrite your installation to add the integration. Skills are just files. They're portable, auditable, and composable. No MCP server required. No plugin marketplace to browse. Just a folder with a `SKILL.md` in it.

This is interoperability without coordination. And I want to be specific about what I mean by that, because it's a strong claim. In tech, getting two competing products to work together usually requires either a formal standard that takes years to ratify, or a dominant platform that forces compatibility. Files sidestep both. If two apps can read markdown, they can share context. If they both understand the SKILL.md format, they can share capabilities. Nobody had to sign a partnership agreement. Nobody had to attend a standards body meeting. The file format does the coordinating.

#### The bottleneck shifted

There's a useful analogy from infrastructure. Traditional data architectures were designed around the assumption that storage was the bottleneck. The CPU waited for data from memory or disk, and computation was essentially reactive to whatever storage made available. But as processing power outpaced storage I/O, the [paradigm shifted](https://www.moonfire.com/stories/the-lakehouse-era/). The industry moved toward [decoupling storage and compute](https://www.pracdata.io/p/zero-disk-architecture-the-future?hide_intro_popup=true), letting each scale independently, which is how we ended up with architectures like S3 plus ephemeral compute clusters. The bottleneck moved, and everything reorganized around the new constraint.

Something similar is happening with AI agents. The bottleneck isn't model capability or compute. It's context. Models are smart enough. They're just forgetful. And filesystems, for all their simplicity, are an incredibly effective way to manage persistent context at the exact point where the agent runs — on the developer's machine, in their environment, with their data already there.

#### You're using a graph and you don't know it

Now, I'd be a *frawd* if I didn't acknowledge the tension here. [Someone on Twitter](https://x.com/nayshins/status/2009366290692231328) joked that "all of you saying you don't need a graph for agents while using the filesystem are just in denial about using a graph." And... they're not wrong. A filesystem *is* a tree structure. Directories, subdirectories, files i.e. a directed acyclic graph. When your agent runs `ls`, `grep`, reads a file, follows a reference to another file, it's traversing a graph.

Richmond in Oracle's piece made the sharpest distinction I've seen: **filesystems are winning as an interface, databases are winning as a substrate.** The moment you want concurrent access, semantic search at scale, deduplication, recency weighting — you end up building your own indexes. Which is, let's be honest, basically a database.

Having worked at Weaviate, I can tell you that this isn't an either/or situation. The file interface is powerful because it's universal and LLMs already understand it. The database substrate is powerful because it provides the guarantees you need when things get real. The interesting future isn't files *versus* databases. It's files as the interface humans and agents interact with, backed by whatever substrate makes sense for the use case.

![](https://madalitso.me/images/finger.png)

#### This is really about personal computing

Here's my actual take on all of this, the thing I think people are dancing around but not saying directly.

Filesystems can redefine what personal computing means in the age of AI.

Not in the "everything runs locally" sense (but maybe?). In the sense that your data, your context, your preferences, your skills, your memory — lives in a format you own, that any agent can read, that isn't locked inside a specific application. Your `aboutme.md` works with your flavour of OpenClaw/NanoClaw today and whatever comes tomorrow. Your skills files are portable. Your project context persists across tools.

This is what personal computing was supposed to be before everything moved into walled-garden SaaS apps and proprietary databases. Files are the original open protocol. And now that AI agents are becoming the primary interface to computing, files are becoming the interoperability layer that makes it possible to switch tools, compose workflows, and maintain continuity across applications, all without anyone's permission.

I'll admit this is a bit idealistic. The history of open formats is littered with standards that won on paper and lost in practice. Companies have strong incentives to make their context files just different enough that switching costs remain high. The fact that we already have `CLAUDE.md` and `AGENTS.md` and `.cursorrules` coexisting rather than one universal format, is evidence that fragmentation is the default, not the exception. And the ETH Zürich paper is a reminder that even when the format exists, writing good context files is harder than it sounds. Most people will write bad ones, and bad context files are apparently worse than none at all.

But I keep coming back to something Dan Abramov wrote: our memories, our thoughts, our designs *should* outlive the software we used to create them. That's not a technical argument. It's a values argument. And it's one that the filesystem, for all its age and simplicity, is uniquely positioned to serve. Not because it's the best technology. But because it's the one technology that already belongs to you.