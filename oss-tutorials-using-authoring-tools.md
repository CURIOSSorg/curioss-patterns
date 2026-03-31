---
tags:
  - Education & Skills
  - Tools & Infrastructure
---
# OSS Tutorials using Authoring Tools

## Pattern Theme / Category

* Education and Skills
* Tools and Infrastructure

## OSPO Problem / Challenge

There is limited knowledge across a university of how to create and use open source software (OSS) effectively; and how to follow best practices / standards.

## Context

A university creates substantial research outputs spanning various disciplines.

There is inconsistent awareness about the role of OSS standards in improving scientific quality and generating results that are reproducible and trustworthy.

Diverse teaching and learning approaches across departments make standardized training packages challenging.

The technology and departmental requirements for curriculum creation and dissemination also vary across the university.

Education/training content is frequently updated across the university.

## Forces

Funding bodies are mandating public access to funded research outputs and research software.

Training materials are needed to support academic cohorts to comply with these public funding mandates. 

Due to the diverse range of technologies and teaching approaches, training resources must be accessible and easily adapted.

## Solution

Create open educational resources ([OER](https://ospo.gwu.edu/open-educational-resources-oer)) in the form of self-directed tutorials based on tools tailored for OSS education.

* Utilize [Jupyter Books](https://github.com/jupyter-book/jupyter-book), combining Markdown and [Jupyter Notebooks](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html), to create tutorials that cater to various learning preferences.  
* Provide a [template repository](https://github.com/gw-ospo/jupyter-book-template) that can be used by anyone as a starting point for creating new tutorials.  
* A range of content can be offered to address various identified needs from introductions to OSS creation to tutorials showcasing OSS standards and practices (e.g. [OSS Licensing for Researchers and Educators](https://gw-ospo.github.io/oss-licensing/intro.html)).  
* Automate updates to tutorial content on websites (following commits to the repository) using [GitHub Actions](https://github.com/features/actions), [GitHub Pages](https://pages.github.com/) and Jupyter Book.  
* Tools such as [binder](https://mybinder.org/) and [Google Colab](https://colab.google/) can be used to allow users to interact with content in real time.  
* Jupyter Books can offer additional formats such as PDFs for offline access.

## Resulting Context

Other tools / platforms such as [Jupyter Book 2](https://blog.jupyterbook.org/posts/2024-11-15-jupyter-book-2-alpha) with [MyST Markdown](https://jupyterbook.org/en/stable/content/myst.html) and [Quarto](https://quarto.org/) may be incorporated to extend capabilities.  

Workflows can be developed for both tutorials *and* workshops that share content and provide experiential learning opportunities.

The methodology for designing OSS tutorials can serve as an example for promoting the use of OER across departments. 

### Additional Learning from the GW OSPO

An exciting benefit of these interactive and publicly available educational tutorial templates is that they are more dynamic. They enable a new type of continuous open science that more closely matches agile development. Because these resources are designed to enable reproducibility and accessibility, they:

* Foster trust in research.  
* Increase scientific quality.   
* Accelerate the pace of discovery and innovation.

## Known Instances

* [The GW Open Source Program Office](https://ospo.gwu.edu/), The George Washington University  
* [Georgia Tech Open Source Program Office](https://ospo.cc.gatech.edu/), Georgia Institute of Technology

## References

* The GW Open Source Program Office: [sample template repository](https://github.com/gw-ospo/jupyter-book-template)   
* [OSS Licensing for Researchers and Educators](https://gw-ospo.github.io/oss-licensing/intro.html) \- example of an open tutorial on OSS best practices  
* Repository: [version-control-workshop-2024 and supporting materials](https://github.com/gw-ospo/version-control-workshop-2024/tree/main)  
  [Version Control Basics](https://gw-ospo.github.io/version-control-workshop-2024/) \- Workshop and supporting materials  
* [Training modules for getting started with open source software development](https://github.com/gt-ospo/oss-training) \- examples of an open training notebooks on getting started with OSS   
* Set Your Money on FIRE: [sample template repository](https://github.com/david-lippert/fire)  
* [Set Your Money on FIRE tutorials](https://david-lippert.github.io/fire/intro.html)   
* [2024 URSSI Summer School resources](https://github.com/si2-urssi/summerschool-June2024)  

## Contributor(s) & Acknowledgment

Lorena Barba \- OSS Licensing Tutorial and Jupyter Book template support  
Clare Dillon \- added markdown to pattern repo  
Ciara Flanagan [https://orcid.org/0009-0005-3153-7673](https://orcid.org/0009-0005-3153-7673)  
David Lippert \- Design pattern and FIRE tutorial  
Michael Rossetti \- Jupyter Book Template

## Additional Notes / Related Inspiration


**Excerpt from the poem Love is an Emergent Process by Adrien Marie Brown**

i look to the sky  
taste the wind on my tongue  
and fling myself  
into the pattern  
when i forget—  
when i think the end is near  
i realize my insignificance  
as important as yours  
and begin  
to love  
again
