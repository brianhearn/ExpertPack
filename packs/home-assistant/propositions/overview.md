# Propositions — Home Assistant Pack Overview

Atomic factual statements extracted from the top-level overview files.

---

### overview.md (composite pack)

- This Home Assistant ExpertPack is a composite pack containing two sub-packs: a product pack (platform reference) and a process pack (smart home building journey).
- The product pack answers questions about what Home Assistant is and how it works internally.
- The process pack provides a 7-phase guided journey for building a smart home with HA, from hardware selection to a fully hardened system.
- The product pack covers: concepts (architecture, protocols, automation, YAML, ESPHome, dashboards, integrations, presence detection, voice assistant, energy management, networking, backup), troubleshooting, FAQ, and a glossary.
- The process pack covers: 7 phases, 3 key decision frameworks, 4 proven automation patterns, and common gotchas.

### product/overview.md

- Home Assistant is an open-source home automation platform built by the Open Home Foundation and backed commercially by Nabu Casa.
- HA runs locally on hardware (Raspberry Pi, mini-PC, NAS, or VM) and serves as the central hub for all smart devices regardless of brand or protocol.
- HA integrates over 3,000 devices and services through its integration library.
- HA's core philosophy is local-first, open, and privacy-respecting — unlike Google Home, Amazon Alexa, or Apple HomeKit which are cloud-dependent.
- HA provides: protocol-agnostic integration (Zigbee, Z-Wave, Matter, WiFi, Bluetooth), a trigger/condition/action automation engine, Lovelace dashboards, ESPHome support, local voice assistant (Assist), energy monitoring, and remote access options.
- This pack targets Home Assistant 2026.3+.

### process/overview.md

- Building a smart home with HA done poorly becomes a maintenance burden — unreliable automations, fragmented protocols, a system that confuses rather than helps.
- HA users do not need to be programmers — they need patience, willingness to read documentation, and comfort with a text editor.
- A basic HA install with 10-20 devices takes 1-2 weekends; a solid protocol setup with first automations takes 2-4 weeks; full home coverage takes 1-3 months.
- The seven phases are: Planning, Initial Setup, Protocol Setup, Automation Building, Dashboard Design, Advanced Features, Hardening.
