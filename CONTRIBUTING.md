# Contributing

Thanks for wanting to contribute! Open a PR or an issue for anything.

## When contributing

When you contribute to a pattern, add yourself as an author so you get credit
on the website (and get your own author page listing every pattern you've
worked on).

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
