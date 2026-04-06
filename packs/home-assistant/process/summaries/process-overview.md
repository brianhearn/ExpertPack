---
title: "Summary — Process Pack Overview"
type: "summary"
tags: [process-overview, summaries]
pack: "home-assistant-process"
retrieval_strategy: "standard"
---

# Summary — Process Pack Overview

This summary covers the 7-phase smart home build process and key decision frameworks. For detailed guidance, follow the links to source files.

---

## The Seven-Phase Journey

Building a smart home with Home Assistant takes 3-6 months to do well. Each phase creates the foundation for the next.

| Phase | Goal | Time |
|-------|------|------|
| [1. Planning](../phases/01-planning.md) | Hardware, install method, network design | 1-3 days |
| [2. Initial Setup](../phases/02-initial-setup.md) | Flash HA, first integrations, companion app | 1 weekend |
| [3. Protocol Setup](../phases/03-protocol-setup.md) | Zigbee/Z-Wave coordinator, pair first devices | 1-2 weeks |
| [4. Automation Building](../phases/04-automation-building.md) | First automations, templates, testing | 2-4 weeks |
| [5. Dashboard Design](../phases/05-dashboard-design.md) | Lovelace dashboards, mobile optimization | 1-2 weeks |
| [6. Advanced Features](../phases/06-advanced-features.md) | Voice, energy monitoring, presence detection | 2-4 weeks |
| [7. Hardening](../phases/07-hardening.md) | Backups, security, remote access | 1 weekend + ongoing |

→ Source: [process overview](../overview.md)

---

## Key Decisions Before You Buy Hardware

Three decisions shape everything downstream. Make these first:

**1. Hardware:** Raspberry Pi 5 + USB SSD (~$120) or used Intel N100 mini-PC ($80-150). Avoid Pi 3, avoid SD card storage. A UPS is strongly recommended.

**2. Installation method:** HA OS for most users (full add-on support, Supervisor, built-in backups). HA Container only if you're a Docker power user who doesn't need add-ons. Never expose port 8123 to the internet.

**3. Protocol:** Lead with Zigbee (local, cheap, mature, massive device selection). Add ESPHome for DIY sensors. Use Z-Wave for locks and thick walls. Adopt Thread/Matter opportunistically.

→ Source: [decisions/protocol-selection.md](../decisions/protocol-selection.md) | [phases/01-planning.md](../phases/01-planning.md)

---

## Common Gotchas (Read Before Starting)

The mistakes that cost people the most time:

- **SD card:** Don't run HA on an SD card. They fail within 6-18 months. Use an SSD.
- **WiFi overload:** Don't buy 40 WiFi devices. Use Zigbee for sensors/plugs/bulbs; WiFi only for cameras.
- **USB 3.0 interference:** Use a USB 2.0 extension cable (20-30 cm) to move the Zigbee dongle away from USB 3.0 ports.
- **Motion lights mode:** Set `mode: restart` on motion-lighting automations. The default `single` mode ignores new motion events while the timer runs.
- **No backups:** Set up Google Drive Backup or Samba Backup on day one. You will need it.
- **YAML without validation:** Always run Settings → System → Check Configuration before restarting after YAML edits.
- **Port 8123 exposed:** Never port-forward 8123 to the internet. Use Nabu Casa, Tailscale, or Cloudflare Tunnel.
- **Naming:** Rename every entity when you add a device. `light.kitchen_ceiling` is useful; `light.0x00158d0003` is not.

→ Source: [gotchas/common-mistakes.md](../gotchas/common-mistakes.md)

---

## Proven Automation Patterns

These patterns work well across thousands of HA installations:

- **[Motion Lighting](../patterns/motion-lighting.md):** `mode: restart` + 5-minute off-delay. Triggers on motion sensor, turns on light, waits for clear, turns off after delay.
- **[Climate Control](../patterns/climate-control.md):** Presence-based HVAC — heat/cool only when home, use setback when away. Use generic thermostat with temperature sensor + switch.
- **[Security Monitoring](../patterns/security-monitoring.md):** Door/window contact sensors + cameras + Frigate object detection + push notifications. Keep cameras on dedicated VLAN.
- **[Notification Patterns](../patterns/notification-patterns.md):** HA Companion app push notifications with actionable buttons. Alert only for things that require action.

---

## What Makes a Smart Home Actually Work for Families

The technical system is only half the challenge. The other half is family acceptance:

- Automations should be invisible — lights that turn on/off without anyone pressing anything.
- Physical switches must always work regardless of HA state.
- Start small — prove one automation works reliably before expanding.
- Use presence-based automations (HVAC, security) as the highest ROI starting point.
- Don't require family members to open an app for daily tasks.

→ Source: [process/faq and gotchas](../gotchas/common-mistakes.md)
