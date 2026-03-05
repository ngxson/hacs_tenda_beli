#!/usr/bin/env python3
"""
Redirect a Tenda Beli plug from Tenda's cloud to your Home Assistant instance.

Usage:
  1. Set up the plug normally via the official Tenda Beli app
  2. Find the plug's IP address in your router's admin page
  3. Run this script:

  python3 setup_plug_to_hassio.py --plug-ip 192.168.1.50 --hassio-ip 192.168.1.100 --ssid MyWiFi --password MyPassword
"""

import argparse
import json
import urllib.request
import urllib.error


def provision(plug_ip, hassio_ip, ssid, password):
    url = f"http://{plug_ip}:5000/guideDone"
    payload = {
        "account": "1",
        "key": password,
        "location": "Australia/Sydney",
        "server": hassio_ip,
        "ssid": ssid,
        "timezone": 600,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    print(f"Sending provisioning request to {url} ...")
    print(f"  SSID:      {ssid}")
    print(f"  Server:    {hassio_ip}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            print(f"Plug responded: {body}")
            print("Done. The plug will now join your WiFi and connect to Home Assistant.")
    except urllib.error.URLError as e:
        print(f"Error: {e}")
        print("Make sure you are connected to the plug's WiFi hotspot and the plug IP is correct.")


def main():
    parser = argparse.ArgumentParser(description="Provision a Tenda Beli plug to connect to Home Assistant")
    parser.add_argument("--plug-ip",   required=True,          help="IP address of the plug on your local network")
    parser.add_argument("--hassio-ip", required=True,          help="IP of your Home Assistant instance")
    parser.add_argument("--ssid",      required=True,          help="WiFi network SSID")
    parser.add_argument("--password",  required=True,          help="WiFi network password")
    args = parser.parse_args()

    provision(args.plug_ip, args.hassio_ip, args.ssid, args.password)


if __name__ == "__main__":
    main()
