---
name: sci-hub
description: Obtain full text for paywalled or bot-blocked papers and guidance documents, landing raw files in a scratchpad. Reach for it when a source is paywalled, captcha-walled, behind a 401/404, or listed in a "sources to obtain" or "could not fetch" table, and before declaring a source unreadable.
platforms: [linux, macos]
metadata:
  version: "1.0.0"
---

# sci-hub

Turn a "could not fetch" list into verified files on disk. The dominant failure mode here is not the paywall, it is giving up after one blocked request or, worse, reporting success without opening the file. A run is finished when **every attempted source ends in a verified file on disk or a written-down reason it cannot exist**.

**The sources land raw.** PDFs, HTML, DOCX, whatever the publisher serves: no Markdown conversion, no summarising. Name article files `lastnameYEAR.pdf` from the first author; keep downloaded bundles in their own subdirectory.

Sci-Hub serves previously uploaded copies from a library; it does not crack a paywall on demand. Papers older than a couple of years from major publishers are near-certain holdings. A paper younger than two years often is not in the library at all, and no mirror fixes that.

## The ladder

Work top to bottom. Stop at the first rung that yields the file.

1. **Open access check** (free, seconds): Unpaywall `https://api.unpaywall.org/v2/<DOI>?email=x@y.org`, Europe PMC `inEPMC`/`hasPDF` flags, PubMed `elink` to PMC. A PMC deposit beats everything: no walls at all.
2. **Supplementary material**: Europe PMC's bulk endpoint `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/supplementaryFiles` returns one zip of all supplementary files, and it serves plain curl when pmc.ncbi.nlm.nih.gov serves a CAPTCHA.
3. **Sci-Hub** for journal articles. Recipe below.
4. **Publisher site via real browser**, when the agent operates a browser anyway and a human with access can log in. Cloudflare-walled journals block curl with 403 but sometimes yield to a warmed browser session.

Say which rung produced each file. A source that survived every rung is recorded as "absent from the world", distinct from "paywalled".

## Sci-Hub recipe

Mirrors share a database but not protection: `sci-hub.box`, `sci-hub.ru`, `sci-hub.ee`, `sci-hub.mksa.top`. Availability and bot walls differ per mirror per day; the recipe handles each.

**Plain curl fails everywhere that matters.** The `.box` domain sits behind DDoS-Guard, whose clearance is a JavaScript challenge; cookie jars assembled by hand, checker-endpoint handshakes and even `--dump-dom` headless Chrome (whose user agent confesses "HeadlessChrome" and gets refused) all stall on the challenge page. Search-POST forms now trip bot checks too.

Use Playwright driving the system Chrome (`channel="chrome"`), never bundled Chromium:

1. Launch headless, set a real Chrome user agent string built from `google-chrome --version`.
2. Land on the homepage first and wait, letting the challenge solve itself. The page title becomes `Sci-Hub`.
3. Navigate to `https://sci-hub.box/<DOI>` and wait. Three landing pages exist: the article page (has an iframe whose src points at the storage PDF), a "not available through Sci-Hub" page, or a challenge again.
4. Extract the PDF URL from the embed iframe or a download link. Prefix `https:` onto `//host/...` forms. The storage host is frequently a **different domain** than the one queried (`.box` pages commonly point at `sci-hub.red`).
5. Download through the browser context's request client (`ctx.request.get`), not curl: it carries the solved session's cookies. Confirm the body starts `%PDF` before writing, then sanity-check with `file` and read the first page with `pdftotext` to confirm title and authors match the citation.

Fall through mirrors in the order they answer; each article is worth one attempt per mirror before the source is called absent. A "not available" verdict is trustworthy only after it comes from the article page itself, not from a blocked request.

## Guidance documents are not articles

A guideline (NHG, NVOG, ACOG, RCOG, USPSTF) is a website problem, not a paywall problem, and Sci-Hub carries none of them. Branch on the blocker:

- **401 or "security check" pages**: rerender the exact URL in Playwright with system Chrome; most are bot walls that a real browser passes silently. The `/print` URL variant of a guideline often bypasses the blocked page entirely.
- **404 on the known portal**: the document usually lives elsewhere as a direct PDF. Search for `site:nvog.nl wp-content`, publisher WordPress upload paths, and the federated `richtlijnendatabase.nl/<guideline>.html` pages, which serve every module as plain HTML that curls cleanly.
- **Whole-guideline PDF exports** behind a form with CSRF and required selections: skip the fight and archive each module page as HTML instead. More pieces, but curl-proof and better for later agent reading.
- **Wayback Machine capture**, when it is up: `web.archive.org` snapshots of a `/print` view often hold what the live site walls off. Check whether the archive itself answers before blaming the origin.

## Completion check

For each attempted source, one of:

- **File on disk** that passes `file` (real PDF/DOCX/HTML) and a first-page spot check against the citation.
- **Named blocker with evidence**: the article-absent page quote, the mirror list tried with timestamps, the search proving no open copy exists. "Paywalled" alone is not a finding; run the ladder before writing it.
