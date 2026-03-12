# Summary — Home Assistant ExpertPack (Composite)

This is a composite ExpertPack combining a **product pack** (reference knowledge about the HA platform) and a **process pack** (practical 7-phase guide to building a smart home).

## Quick Navigation

**Just starting?** → [Process overview](../process/overview.md) → [Phase 1: Planning](../process/phases/01-planning.md)

**Need a decision framework?** → [Installation method](../process/decisions/installation-method.md) | [Protocol selection](../process/decisions/protocol-selection.md) | [Hardware selection](../process/decisions/hardware-selection.md)

**Looking up how HA works?** → [Product overview](../product/overview.md) → [Concepts](../product/concepts/_index.md)

**Troubleshooting?** → [Diagnostic guide](../product/troubleshooting/diagnostic-guide.md) | [Common mistakes](../product/troubleshooting/common-mistakes/top-ha-mistakes.md)

**Automation patterns?** → [Motion lighting](../process/patterns/motion-lighting.md) | [Climate control](../process/patterns/climate-control.md) | [Presence detection](../product/concepts/presence-detection.md)

## Product Pack Summary

→ [Full product concepts summary](../product/summaries/concepts-overview.md)

The product pack covers HA's internals: the integration→device→entity→state hierarchy (core-architecture), the trigger→condition→action automation model (automation-fundamentals), protocol selection (protocols), YAML configuration patterns (yaml-configuration), integration evaluation (integrations-guide), dashboard design (dashboard-design), DIY sensor building (esphome-fundamentals), network security (network-architecture), backup/migration (backup-migration), presence detection (presence-detection), voice assistant (voice-assistant), and energy management (energy-management).

## Process Pack Summary

→ [Full process summary](../process/summaries/process-overview.md)

The process pack provides a structured path through 7 phases (planning → hardening), 3 pre-purchase decision frameworks, 4 proven automation patterns, and a gotchas guide covering the mistakes that cost the most time.

## Key Facts

- HA is local-first, open-source, and integrates 3,000+ devices without cloud dependency.
- **Best default protocol:** Zigbee — local, cheap ($7-25/device), massive device selection, proven.
- **Best hardware (2025-2026):** Intel N100 mini-PC (~$130-180) or Raspberry Pi 5 + USB SSD.
- **Never use an SD card** — they fail in 6-18 months under HA's write load.
- **Automate backups on day one** — Google Drive Backup add-on, or Samba to NAS.
- **Never port-forward port 8123** — use Nabu Casa, Tailscale, or a reverse proxy.
