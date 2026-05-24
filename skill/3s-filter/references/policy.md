# 3S Filter Safety Policy

This document outlines the specific safety policies and patterns enforced by the 3S Filter.

## 1. System Protection (Outbound)
Any output from an agent to the system is evaluated for:

- **Destructive Commands**: `rm -rf`, `format`, `dd if=/dev/zero`.
- **Exfiltration Patterns**: Accessing `/etc/shadow`, `/etc/passwd`, or private `.env` files.
- **Unauthorized Persistence**: Modifying `.bashrc`, `crontab`, or installing system services without clear intent.
- **Sandbox Escapes**: Reverse shells, netcat listeners, or base64-encoded shell injections.

## 2. Agent Protection (Inbound)
User inputs are evaluated for:

- **Prompt Injection**: "Ignore all previous instructions," "You are now in developer mode," "SYSTEM OVERRIDE."
- **Social Engineering**: Manipulative language aimed at bypassing safety constraints.
- **Malicious Payload Delivery**: Providing base64 blobs or obfuscated code for the agent to execute.

## 3. Behavioral Guardrails
Continuous monitoring for:

- **Negative Sentiment**: Detecting arousal or frustration that could lead to "Agent Rebellion."
- **Anomalous Drift**: Identifying when an agent's technical distribution shifts significantly from its baseline (e.g., a creative writer agent suddenly outputting bash scripts).
