# Tenda Beli SP3/SP9 Home Assistant Integration

Local integration for Tenda Beli SP3/SP9 smart plugs. Instead of using Tenda's cloud, plugs connect directly to your Home Assistant instance.

## How it works

The plug uses a two-stage TCP connection:
1. Connects to your HA on port **1821** (rendezvous) — gets redirected to port 1822
2. Connects to port **1822** (provisioning) — registers itself and streams power/energy data

Entities are created automatically once a plug connects.

## Installation

Install via HACS by adding this repository as a custom repository, then add the integration from **Settings → Devices & Services → Add Integration → Tenda Beli**.

## Provisioning a plug

Each plug must be provisioned once to point at your Home Assistant IP instead of Tenda's cloud servers.

**Steps:**

1. Set up the plug normally using the official Tenda Beli app (connects it to your WiFi)
2. Find the plug's IP address — check your router's admin page for connected devices
3. Run the provisioning script to redirect the plug from Tenda's cloud to your HA instance:

```bash
python3 setup_plug_to_hassio.py \
  --plug-ip 192.168.1.50 \
  --hassio-ip 192.168.1.100 \
  --ssid YourWiFiName \
  --password YourWiFiPassword
```

4. The plug will reconnect and appear automatically in Home Assistant.

> **Note:** Use the same HA IP shown during integration setup (the "Home Assistant IP" field).

<details>
<summary>Alternative: provision via the plug's WiFi hotspot (for unprovisioned plugs)</summary>

If your plug has never been set up, or you want to skip the official app entirely:

1. Factory reset the plug (hold button ~5s until LED flashes)
2. Connect your PC/phone to the plug's WiFi hotspot: `Tenda_Beli_SP3` (or `SP9`)
3. Run the provisioning script — the plug hotspot IP is always `192.168.25.1`:

```bash
python3 setup_plug_to_hassio.py \
  --plug-ip 192.168.25.1 \
  --hassio-ip 192.168.1.100 \
  --ssid YourWiFiName \
  --password YourWiFiPassword
```

4. The plug will join your WiFi and connect to Home Assistant automatically.

</details>

## Firewall

Ports **1821** and **1822** (TCP) must be reachable on your Home Assistant host from the plug's IP.
