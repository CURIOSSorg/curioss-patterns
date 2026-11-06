---
tags:
 - Advocacy, Governance & Policy
 - Open Source Discovery
 - Working with Tech Transfer / External Partners
authors:
  - aoife-tierney
  - ciara-flanagan
  - clara-morella-teixidor
  - jacek-plucinski
  
---
# Open Source Software Disclosure Form

## Pattern Summary

Use a dedicated software disclosure form that asks researchers to list all third-party and open source software that their work depends on, together with licenses. This enables the Technology Transfer Office (TTO) to identify a basic software bill of materials (SBOM).

## Problem / Challenge

-   Open source is present in almost every research software project, yet it is often invisible to the TTO when researchers disclose a new invention or piece of software.
-   Many institutions only have a general invention disclosure form (IDF), which is often STEM-heavy and patent-focused. Software, and particularly the open source it depends      on, may not be fully referenced, or may not be named at all.
-   When third-party open source components and their licenses are not kown at the outset, Tech Transfer Offices (TTOs) can discover licensing conflicts late in the process -      after critical decisions about release, licensing and commercialization have already been made.
-   Institutions have little hard data on how much of their research output uses or produces open source, which makes it harder to plan support, monitor activity or make the       case for open source.

## Context

A university or research institution with a Technology Transfer Office (TTO), or similar innovation or commercialization team, that receives disclosures of research outputs from researchers.

An OSPO, open source champion or TTO staff member is in place who understands the context for open source disclosed within the institution's commercialization and translation pathways.

## Forces

-   Disclosure practice is not standard across TTOs.
-   Asking for a full list of dependencies and licenses asks more of researchers.
-   Researchers may not be familiar with SBOMs, or may not know the licenses of every component they use.
-   The TTO or OSPO may not own the institutional IP policy, which may sit at a higher level of governance. Updating a disclosure form may be more within their control than changing the policy itself.
-   TTO colleagues may not be fully aware of the importance or value proposition of open source see [Integrating OSS into Institutional Software Pathways](https://curioss.org/patterns/integrating-oss-into-institutional-software-pathways/).

## Solution

Use a dedicated software disclosure form, alongside the invention disclosure form, that captures the open source the software depends on.

The solution below outlines some core activities to consider.

### Review current disclosure processes

-   Identify which forms researchers currently use to disclose research outputs (e.g. invention disclosure, software disclosure, idea disclosure or IP notification forms) and who owns them.
-   Check whether these forms currently ask anything about software, third-party components or open source licenses.
-   Where possible, look at examples of disclosure forms from other institutions. Questions vary widely, from a simple description of what was developed through to full dependency lists and questions on the use of AI tools.


### Keep the software disclosure form lighter than the invention disclosure

-   Design the software disclosure form as a shorter companion to the invention disclosure form so researchers can complete both together.
-   Focus on what matters most for software: what was developed, who contributed, where the code is held and what it depends on.

### Ask for all third-party software and licenses

-   Ask researchers to list all third-party software, libraries and dependencies they have used, together with their licenses. In effect, this provides a basic SBOM.
-   Where researchers can generate an SBOM with a tool, accept it in place of a manually completed list.

### Draft focused open source questions


Keep the questions specific to open source. Examples include:

- Does the output contain or depend on any third-party or open source software? If so, list the components and their licenses (or attach an SBOM).
- Has any part of the code already been released publicly? If so, where (e.g. a public repository) and under which license?
- Is there a plan or obligation (e.g. from a funder or collaborator) to release the software as open source?
- Were AI tools or agents used to generate any part of the code?
- Who contributed to the code, including external collaborators or students?


### Use the disclosure to inform decisions

Use the information gathered to check license compatibility and to inform decisions about release and commercialization routes.

### Use the information for monitoring

Disclosed dependency lists and repository locations can help the institution to distinguish between internal development and code that has already been released publicly, and to build a better picture of open source activity across the institution.

### Review and update regularly

Revisit the questions periodically with TTO colleagues and researchers to ensure that the form keeps pace with new practices (e.g. the use of AI tools and agents in development) and new types of research outputs.

## Resulting Context

The TTO has visibility of open source components and licenses from the moment a research output is disclosed.

Licensing issues can be identified early, conversations about release and commercialization routes are better informed, and the institution builds up a clearer picture of how open source is used in its research.

## Additional Learning from Trinity College Dublin

Our TTO has a dedicated software disclosure form, which, as far as we know, is not standard practice across Tech Transfer offices.

Our software disclosure form is lighter than our invention disclosure form (IDF). We sometimes ask researchers to complete both, with the two forms going alongside each other.

The main advantage for open source is that we ask researchers to name all third-party software and dependencies they have used, including all of their licenses. In effect, our researchers provide a basic SBOM as part of their disclosure.

We plan to update our software disclosure form over time.

Our current IDF can be too STEM-heavy for researchers in arts, humanities and social sciences. We're planning to work with researchers to develop a 'softer' innovation disclosure form that would also capture outputs such as teaching materials, where appropriate.

We do not claim IP in artistic or scholarly works, and IP in teaching materials is something of a grey area. Where researchers want our support for these outputs (e.g. for consultancy or a spin-out), it must first be clear that we own the IP.

## Known Instances

Technology Transfer Office, Trinity College Dublin

## References

### Related Patterns

-   [Light-Touch Open Source Disclosure](https://curioss.org/patterns/light-touch-open-source-disclosure/)
-   [Integrating OSS into Institutional Software Pathways](https://curioss.org/patterns/integrating-oss-into-institutional-software-pathways/)

## Contributors & Acknowledgements



**A Note on AI Use:** This content was drafted with the help of AI. As a small organization,
AI tools help us turn rich conversations into written resources with
less effort---meaning we can offer more to the community. As always,
there were plenty of human eyes reviewing, editing and improving the
content before it was published. Thanks go to our community for the
insights. If you do spot any errors, please let us know so we can
correct them!
