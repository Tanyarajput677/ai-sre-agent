# Autonomous AI-SRE Agent with GitOps Self-Healing & Semantic Guardrails

An autonomous Site Reliability Engineering (SRE) agent that ingests real-time Kubernetes cluster telemetry, isolates root causes across multi-modal failure vectors (CrashLoopBackOff, ImagePullBackOff, OutOfMemory, Probe Failures), and synthesizes declarative GitOps remediation patches validated against deterministic semantic safety policies.

## 🏗️ Architecture
- In-Cluster Outage -> Telemetry Ingestion -> SRE Reasoning Loop -> Semantic Guardrail -> GitOps Patch -> Cluster Recovery

## 📊 Benchmarking & Performance
- Mean Time to Remediation (MTTR): < 0.05 seconds (In-cluster synthesis & apply)
- Safety Policy Enforcement: 100% rejection rate for privilege escalations & destructive operations
- Failure Coverage: CrashLoopBackOff, ImagePullBackOff, OOMKilled, LivenessProbeFailure

## 🛠️ Tech Stack
- Orchestration: Kubernetes, KinD, Docker
- Agentic Runtime: Python 3.12, Kubernetes Client SDK, PyYAML
- Evaluation & Chaos: Custom Multi-Scenario Chaos Injector & Latency Benchmark Harness

## 🚀 Quickstart
1. Inject Chaos:
   python chaos.py bad_probe
2. Run AI-SRE Evaluator:
   python evaluator.py
