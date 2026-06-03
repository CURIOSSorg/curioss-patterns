---
tags:
  - Demonstrating value as an Academic OSPO
  - Education & Skills
  - Open Source Development
  - Tools & Infrastructure
  - Working with Tech Transfer / External Partners
authors:
  - will-gearty
  - ramya-patchala
  - aryan-apte
  - ciara-flanagan
---
# Open Source AI Pilot

## Pattern Summary

Develop a pilot program to investigate the capabilities and use of locally run “open source” LLM for university applications.

## Problem / Challenge

Large Language Models (LLMs) have grown extremely quickly in the past couple of years. Universities (both faculty and administration) are keen to make use of these new tools.

However, there are a number of challenges:

- **Privacy:** In the case of platforms that incorporate further training in LLMs (e.g. ChatGPT), the LLM cannot be used for sensitive data, or documents with licenses that do not allow for dissemination without prior approval from the author(s).
- **Cost:** Where platforms protect confidential data (e.g. Co-Pilot), licenses may be too expensive for the entire university or for individual faculty to use in their research programs.
- **Reproducibility:** LLMs are stochastic by nature. This issue is exacerbated in enterprise models, which undergo frequent, undocumented updates. As a result,  their use as research tools raises concerns about reproducibility and result consistency.

## Context

A university or research institution with an interest in making use of AI.

## Forces

- Graphic Processing Units (GPUs) and large amounts of memory are required to run these models locally.

- A database of documents or information is required to augment the LLM.

- Resources are in place to fund students to work on development.

## Solution

Develop a pilot program to explore how to use AI tools in an open-source, academic environment.

Define and communicate the criteria for the project.

Overall, the pilot should be:

- Relatively low risk (to take account of LLM hallucinations).
- Useful to faculty and the wider university community.
- Able to run on local hardware.
- Designed for students to work and collaborate on.

### Tools and Infrastructure

A number of tools are available to support development.

Although [LLAMA](https://ollama.com/library/llama3.1) is not strictly open source, it can be run locally, and modified for various purposes.

Many open-source AI tools are available on [Hugging Face](https://huggingface.co/) (with and without LLMs).

Using retrieval-augmentation generation (RAG) will improve LLM accuracy.

## Resulting Context

Intended outcomes are:

- Faculty and students can make use of open source AI tools that benefit their research activities.
  
- The OSPO demonstrates its value in enhancing access to research and as an enabler of research efficiency.
  
- Developing AI solutions that address problems identified on campus fosters stronger relationships with faculty, researchers and students.

### Additional Learning from Syracuse University

We’ve hired two Masters of Science students to work on two pilot projects.

The first pilot is to build a chatbot that will answer questions about research being undertaken at our university. The objectives of the project are to improve access to university-based research; and to strengthen collaboration across campus.

An unexpected finding was the lack of a central database of publications written by faculty - an essential requirement for the chatbot. We’re currently building that database (which is a project in itself). These papers are being used to improve the training of a locally run instance of LLAMA and should enable the chatbot (in theory) to give more accurate answers.

Given the broader value of the database, we plan to make it publicly available when it’s completed.

The second project is a collaboration with an economics professor and her team to digitize old tariff documents. Replacing this manual task with an AI solution will reduce researchers’ workload and free up time for actual research.

We hope to have a working solution by the end of the spring semester 2025.

If the projects are successful, we will build similar tools that will be useful to the university community.

In taking on this project, we also discovered that the GPU hardware on campus is becoming outdated. We are currently working with other faculty that are interested in AI to submit a funding proposal.

## Known Instances

[Syracuse University Open Source Program Office](https://opensource.syracuse.edu/), Syracuse University

## References

## Contributors & Acknowledgement
