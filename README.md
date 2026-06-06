# CollabQA

## Human–AI Collaboration in Software Quality for Authentication Modules

CollabQA is a software quality project focused on Human–AI collaboration in code review, test generation and debugging activities.

The project is based on the seminar "Trust, Accountability, and Responsibility in AI-Supported Software Engineering" and applies its main ideas to a practical case study involving an authentication module.

## Problem

AI tools can support developers by suggesting code changes, tests and debugging explanations. However, in critical modules such as authentication, an AI-generated suggestion may look correct while still introducing security or reliability problems.

This project studies how humans and AI can collaborate in software quality tasks while preserving human validation, traceability and explicit responsibility.

## Case Study

The case study is a small authentication module with a controlled defect related to expired session validation.

The initial version contains incomplete tests that pass successfully but do not detect the expired session problem. CollabQA uses AI-assisted analysis and human validation to identify the problem, suggest additional tests and record the decisions made during the process.

## Goals

- Support AI-assisted code review.
- Support AI-assisted test suggestion.
- Support collaborative debugging.
- Register human decisions about AI suggestions.
- Keep an audit log of accepted, rejected and partially accepted suggestions.
- Compare three modes: human alone, AI alone and human + AI.
- Evaluate the impact on bugs found, useful tests created, coverage and traceability.

## Main Research Question

Does Human–AI collaboration improve defect detection, test creation and decision traceability in an authentication module?

## Project Structure

```text
app/              CollabQA application modules
sample_project/   Authentication case study
data/             Audit logs and decision records
experiments/      Experimental results
reports/          Final result tables