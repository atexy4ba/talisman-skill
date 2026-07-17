# Grill-me: brief definition for Talisman

Before any guide generation, run the grill-me skill to define the brief. Ask these
6 questions one at a time. The answers parameterize the entire workflow below.

## Question 1 — Document type

What kind of document are we producing?

| Option | Cover subtitle | DOC_KIND | TOC structure |
|--------|---------------|----------|---------------|
| Internal guide | "Internal Reference" | Technical Reference | Standard 7-chapter |
| Onboarding manual | "Onboarding Manual" | Onboarding | Getting-started heavy |
| Technical whitepaper | "Technical Whitepaper" | Whitepaper | Architecture + deep dives |
| API / integration guide | "API Reference" | API Reference | Endpoint-focused |
| Feature overview | "Feature Overview" | Feature Guide | Use-case driven |
| Contributor handbook | "Contributor Handbook" | Contributor Guide | Repository structure first |
| Brand / product guide | "Brand & Product Guide" | Product Guide | Market positioning first |

## Question 2 — Target audience

Who is this document for?

| Audience | Code density | Diagram vs text | Depth |
|----------|-------------|-----------------|-------|
| Developers | Heavy (real code) | 50/50 | Deep architecture |
| End-users | Light (config only) | 80/20 text | Workflow-focused |
| Managers | Conceptual only | 90/10 | High-level |
| OSS contributors | Full code + build | 40/60 | Contribution flow |
| C-suite / execs | None | 95/5 | Strategic value |

## Question 3 — Scope

Which part of the codebase does this cover?

| Scope | Research target | Chapters |
|-------|----------------|----------|
| Full codebase | Stratified sampling (all modules) | 5-7 |
| Single module | Module tree + models + views | 2-3 |
| Specific workflow | State machine + related models | 1-2 |
| Integration point | API + controllers + external refs | 2-3 |
| Architecture only | Core framework only | 3-5 |

## Question 4 — Depth

How comprehensive should the output be?

| Depth | Pages target | Chapters | Lines per chapter |
|-------|-------------|----------|-------------------|
| Overview (~10p) | 8-12 | 3-4 | ~100-150 |
| Standard (~25p) | 20-30 | 5-7 | ~200-300 |
| Comprehensive (~50p) | 40-55 | 7-10 | ~300-500 |

## Question 5 — Special focus

Any specific area to highlight?

| Focus | Extra chapter/section |
|-------|----------------------|
| Security | Full security chapter with audit patterns |
| Performance | Benchmarking + optimization patterns |
| APIs / integrations | External API patterns + example clients |
| Customization / extension | Extension patterns + override examples |
| Deployment / DevOps | Docker, CI/CD, production config |
| Testing | Test patterns, fixtures, CI setup |
| None (standard) | No extra chapter |

## Question 6 — Diagrams

Which diagram families are needed?

| Selection | Diagrams to produce |
|-----------|-------------------|
| All three (default) | Domain model + Flow + State machine |
| Domain model only | ER-style entity relationship |
| Flow + State machine | Pipeline + FSM |
| Architecture only | System architecture / deployment |
| None | No diagrams (text-only) |
