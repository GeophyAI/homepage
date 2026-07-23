---
layout: page
permalink: /publications/
title: publications
description: My publications, grouped by year, type, or venue. Click a title to open the paper.
nav: true
nav_order: 2
---

<!-- _pages/publications.md -->

<!-- Bibsearch Feature -->

{% include bib_search.liquid %}

<div class="pub-sort btn-group btn-group-sm" role="group" aria-label="Sort publications">
  <button type="button" class="btn btn-outline-primary active" data-sort="year">By year</button>
  <button type="button" class="btn btn-outline-primary" data-sort="cat">By type</button>
  <button type="button" class="btn btn-outline-primary" data-sort="venue">By venue</button>
</div>

<div class="publications">

{% bibliography %}

</div>

<style>
  .pub-sort { margin: 0.5rem 0 1.5rem; flex-wrap: wrap; gap: 0; }
  .pub-sort .btn { text-transform: none; }

  /* Clean two-line entries: title on its own line, meta + links muted below */
  .publications ol.bibliography li { margin-bottom: 0.9rem; }
  .publications .row { margin-bottom: 0; }
  .publications .row > div[id] { flex: 1; max-width: none; } /* content fills full width */

  /* line 1 — title (primary: larger + bold + full contrast) */
  .publications ol.bibliography li .title {
    display: block;
    font-weight: 700;
    font-size: 1.15rem;
    line-height: 1.3;
    margin-bottom: 0.25rem;
  }
  .publications .title a { color: var(--global-text-color); font-weight: 700; }
  .publications .title a:hover { color: var(--global-theme-color); text-decoration: underline; }

  /* line 2 — authors · venue, year (secondary: small + muted gray) */
  .publications .author,
  .publications .periodical { display: inline; font-size: 0.85rem; line-height: 1.45; color: var(--global-text-color-light); }
  /* your own name: distinct but subordinate — no underline, medium weight, full contrast */
  .publications ol.bibliography li .author > em { font-style: normal; font-weight: 600; border-bottom: none; color: var(--global-text-color); }
  .publications .author::after { content: "  ·  "; }
  .publications .periodical + .periodical { display: none; } /* hide empty 2nd date div */

  /* links */
  .publications .links { display: inline; margin-left: 0.4rem; }
  .publications .links .btn {
    padding: 0 0.45em;
    font-size: 0.7rem;
    line-height: 1.7;
    margin-right: 0.15rem;
    color: var(--global-theme-color);
    border: 1px solid var(--global-divider-color);
    border-radius: 4px;
  }

  /* year headers */
  .publications h2.bibliography {
    font-size: 1.4rem;
    margin: 1.5rem 0 0.7rem;
    padding-bottom: 0.25rem;
    border-bottom: 1px solid var(--global-divider-color);
  }
</style>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".publications");
    if (!container) return;
    const lis = Array.from(container.querySelectorAll("ol.bibliography > li"));
    if (!lis.length) return;

    const venueNames = {
      "IEEE TGRS": "IEEE Transactions on Geoscience and Remote Sensing",
      "Geophysics": "Geophysics",
      "GP": "Geophysical Prospecting",
      "GJI": "Geophysical Journal International",
      "CJG": "Chinese Journal of Geophysics",
      "FES": "Frontiers in Earth Science",
      "JOUC": "Journal of Ocean University of China",
      "OGP": "Oil Geophysical Prospecting",
      "AG": "Applied Geophysics",
      "EAGE": "EAGE Conference & Exhibition",
      "SEG": "SEG / IMAGE Annual Meeting",
      "arXiv": "arXiv preprint",
    };
    const catOrder = ["Journal Articles", "Conference Proceedings", "Preprints"];

    const meta = lis.map(function (li) {
      const row = li.querySelector(".row");
      const d = (row && row.dataset) || {};
      return {
        li: li,
        year: parseInt(d.year, 10) || 0,
        cat: d.cat || "Journal Articles",
        abbr: d.abbr || "",
        venue: d.venue || d.abbr || "—",
      };
    });

    // Drop the original year-grouped markup; we rebuild for every mode.
    container.querySelectorAll("h2.bibliography, ol.bibliography").forEach(function (n) { n.remove(); });

    function buildGroups(mode) {
      const bins = {};
      const push = function (k, m) { (bins[k] = bins[k] || []).push(m); };
      if (mode === "year") {
        meta.forEach(function (m) { push(m.year, m); });
        return Object.keys(bins).sort(function (a, b) { return b - a; })
          .map(function (y) { return { label: y, items: bins[y] }; });
      }
      if (mode === "cat") {
        meta.forEach(function (m) { push(m.cat, m); });
        const ordered = catOrder.filter(function (c) { return bins[c]; })
          .map(function (c) { return { label: c, items: bins[c].slice().sort(byYearDesc) }; });
        Object.keys(bins).filter(function (c) { return catOrder.indexOf(c) === -1; })
          .forEach(function (c) { ordered.push({ label: c, items: bins[c].slice().sort(byYearDesc) }); });
        return ordered;
      }
      // venue: group by abbr, label with full venue name
      meta.forEach(function (m) { push(m.abbr || m.venue, m); });
      return Object.keys(bins)
        .sort(function (a, b) { return bins[b].length - bins[a].length || a.localeCompare(b); })
        .map(function (k) { return { label: venueNames[k] || k, items: bins[k].slice().sort(byYearDesc) }; });
    }
    function byYearDesc(a, b) { return b.year - a.year; }

    function render(mode) {
      container.innerHTML = "";
      buildGroups(mode).forEach(function (g) {
        const h2 = document.createElement("h2");
        h2.className = "bibliography";
        h2.textContent = g.label;
        const ol = document.createElement("ol");
        ol.className = "bibliography";
        g.items.forEach(function (m) { ol.appendChild(m.li); });
        container.appendChild(h2);
        container.appendChild(ol);
      });
      // If a search term is active, re-apply the filter to the new grouping.
      const sb = document.getElementById("bibsearch");
      if (sb && sb.value) sb.dispatchEvent(new Event("input"));
    }

    render("year");

    document.querySelectorAll(".pub-sort [data-sort]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".pub-sort [data-sort]").forEach(function (b) { b.classList.remove("active"); });
        btn.classList.add("active");
        render(btn.dataset.sort);
      });
    });

    // --- "Cite" buttons: copy a ready-to-paste formatted reference ---
    function field(txt, re) { const m = txt.match(re); return m ? m[1].trim() : ""; }
    function parseBib(txt) {
      const authorRaw = field(txt, /author\s*=\s*\{([\s\S]*?)\}/i);
      const authors = authorRaw.split(/\s+and\s+/).map(function (a) {
        const p = a.split(",");
        return p.length === 2 ? p[1].trim() + " " + p[0].trim() : a.trim();
      }).join(", ");
      const doi = field(txt, /doi\s*=\s*\{([^}]*)\}/i);
      const arxiv = field(txt, /arxiv\s*=\s*\{([^}]*)\}/i);
      const url = field(txt, /url\s*=\s*\{([^}]*)\}/i);
      return {
        authors: authors,
        title: field(txt, /title\s*=\s*\{+([^{}]*?)\}+\s*,/i),
        venue: field(txt, /journal\s*=\s*\{([^}]*)\}/i) || field(txt, /booktitle\s*=\s*\{([^}]*)\}/i),
        year: field(txt, /year\s*=\s*\{([^}]*)\}/i),
        link: doi ? "https://doi.org/" + doi : (arxiv ? "https://arxiv.org/abs/" + arxiv : url),
      };
    }
    function buildCitation(b) {
      let s = "";
      if (b.authors) s += b.authors + ". ";
      if (b.title) s += b.title + ". ";
      if (b.venue) s += b.venue + ", ";
      if (b.year) s += b.year + ". ";
      if (b.link) s += b.link;
      return s.trim();
    }
    async function copyText(text) {
      try { await navigator.clipboard.writeText(text); return true; }
      catch (e) {
        const ta = document.createElement("textarea");
        ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        let ok = false; try { ok = document.execCommand("copy"); } catch (e2) {}
        document.body.removeChild(ta); return ok;
      }
    }
    lis.forEach(function (li) {
      const links = li.querySelector(".links");
      const code = li.querySelector(".bibtex code");
      if (!links || !code) return;
      const citation = buildCitation(parseBib(code.textContent));
      if (!citation) return;
      const btn = document.createElement("a");
      btn.className = "cite btn btn-sm z-depth-0";
      btn.setAttribute("role", "button");
      btn.style.cursor = "pointer";
      btn.textContent = "Cite";
      btn.addEventListener("click", async function () {
        const ok = await copyText(citation);
        btn.textContent = ok ? "Copied!" : "Copy failed";
        setTimeout(function () { btn.textContent = "Cite"; }, 1500);
      });
      links.appendChild(btn);
    });
  });
</script>
