# Results Analysis

The experimental comparison evaluated three modes: Human alone, AI alone, and Human + AI.

## Human alone

The human-alone mode identified one relevant problem: the expired session validation issue. This shows that manual review can detect important defects, especially when the reviewer understands the authentication logic.

However, this mode did not provide structured traceability. The decision was not automatically recorded in an audit log, and the review process depended entirely on the individual reviewer.

## AI alone

The AI-alone mode identified three relevant risks:

1. Expired sessions may still be accepted.
2. Admin permissions are automatically granted.
3. Session tokens are predictable.

This shows that AI assistance can increase the number of findings and suggest useful tests. However, the AI-alone mode did not include human validation, justification, or accountability. Therefore, the suggestions could not be treated as final decisions.

## Human + AI

The Human + AI mode achieved the best result. It identified the same three relevant risks as the AI-alone mode, but added human validation and traceability.

In this mode, two suggestions were accepted and one was partially accepted. Each decision included a human justification and was recorded in the audit log.

This result supports the central idea of the project: AI can improve software quality activities when used as a support tool, but the final decision should remain human and traceable.

## Main Result

The most important finding was related to expired session validation.

Initially, the test suite had 5 passing tests and gave a false sense of quality. After the AI-assisted review and human validation, a new test was suggested for expired sessions. This test failed in the original implementation, confirming the existence of the defect.

After correcting the validate_session function, all 6 tests passed and the final coverage reached 93%.

## Interpretation

The results suggest that Human–AI collaboration provides a better balance than using either humans or AI alone.

Human review contributes contextual judgement and responsibility.
AI contributes broader analysis and test suggestions.
The audit log contributes traceability and accountability.

Together, these elements support a more responsible software quality process.

## Limitations

This evaluation was performed on a small academic case study. The results should not be generalized to large industrial systems without further validation.

The AI module used in this prototype is deterministic and rule-based. In a future version, it could be connected to a real Large Language Model.

The human-alone mode may also be affected by reviewer familiarity with the project.