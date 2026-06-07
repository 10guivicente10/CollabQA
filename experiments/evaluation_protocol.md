# CollabQA Evaluation Protocol

## Goal

The goal of this evaluation is to compare three approaches to software quality activities in an authentication module:

1. Human alone
2. AI alone
3. Human + AI

The evaluation focuses on defect detection, test suggestion usefulness, false positives and decision traceability.

## Case Study

The case study is a small authentication module containing a controlled defect related to expired session validation.

The initial tests passed successfully, but they did not cover the expired session scenario. This created a false sense of quality, since the authentication module still accepted expired sessions.

## Evaluation Modes

### Human alone

The authentication code is reviewed manually without using CollabQA suggestions.

### AI alone

The AI review module generates suggestions automatically, without human validation.

### Human + AI

The AI generates suggestions, the human reviewer validates each suggestion, and the system records decisions in an audit log.

## Metrics

The following metrics are considered:

- Number of relevant problems found
- Number of false positives
- Number of useful tests suggested
- Number of human-validated decisions
- Audit log entries
- Final test result
- Final coverage

## Known Relevant Findings

The expected relevant findings in this case study are:

1. Expired sessions may still be accepted.
2. Admin permissions are automatically granted and should be reviewed or documented.
3. Session tokens are predictable.

## Threats to Validity

This evaluation is based on a small academic case study and a limited authentication module. The results should not be generalized to all software projects without further validation.

The human-alone evaluation may be affected by reviewer knowledge of the project, since the same team developed the case study.