# Contributing

Thanks for wanting to contribute! Open a PR or an issue for anything.

## When contributing

When you contribute to a pattern, add yourself as an author so you get credit
on the website and on the [Authors page](authors/index.md), which lists every
contributor alongside the patterns they've worked on.

There are two short steps:

1. **Add yourself to [`authors.yml`](https://github.com/CURIOSSorg/curioss-patterns/blob/main/authors.yml)** (at the root of this repo)
   if you're not already there. Pick a short slug — usually
   `firstname-lastname` — and fill in your name, ORCID (optional), and
   affiliation (optional). For example:

   ```yaml
   jane-doe:
     name: Jane Doe
     orcid: 0000-0001-2345-6789
     affiliation: Example University
   ```

2. **Add your slug to the pattern's `authors:` frontmatter** at the top of the
   pattern file. For example:

   ```yaml
   ---
   tags:
     - Community Building
   authors:
     - jane-doe
   ---
   ```

You do **not** need to edit the "Contributors & Acknowledgement" section at
the bottom of the pattern — the site generates that automatically from the
frontmatter.

## The RSS feed

The site publishes an RSS feed of new patterns at
[/feed_rss_created.xml](https://curioss.org/patterns/feed_rss_created.xml) so
readers can subscribe to updates. A couple of things to know as a contributor:

- **Your ORCID, if you provide one, appears publicly in each feed item** for
  every pattern you've co-authored — as a clickable link to your ORCID
  profile. This is the same ORCID that already shows up on the pattern page
  itself; the feed just makes it travel further.
- **The first paragraph of your pattern becomes the feed blurb.** Try to
  make that opening sentence stand on its own — it's what readers will see
  in their RSS reader before they click through.
- **My pattern isn't in the feed — why?** Three usual culprits:
  1. The file is not at the repo root (everything in `authors/` and the
     four meta files — `README.md`, `CONTRIBUTING.md`, `PATTERN-TEMPLATE.md`,
     and any new top-level non-pattern doc listed in the `match_path` of
     `.config/mkdocs.yml` — is excluded by design).
  2. The pattern has no git history yet (it must have been committed at
     least once; the feed uses the first commit as the publication date).
  3. The build is older than your latest commit — the feed is regenerated
     on every deploy.

## Local Development

If you want to test the MkDocs site locally:

1. **Install MkDocs Material** (requires Python):

   ```bash
   pip install -r .config/requirements.txt
   pip install mkdocs-material
   ```

2. **Run the development server:**

   ```bash
   cd .config
   mkdocs serve
   ```

3. **View the site:** Open your browser to <http://127.0.0.1:8000>

The development server will automatically reload when you make changes to any markdown files.
