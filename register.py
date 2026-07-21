import requests

# --- 1. FILL IN YOUR DETAILS HERE ---
PHONE_NUMBER_ID = "1140053769199865"  # I pulled this from your earlier screenshot!
ACCESS_TOKEN = "EAAbEBq3pvg0BRjy7fGYthSJLB1fkv0CWoTwclZCHoOqyaVElwVZCtpkQGAblPvb8jTwTPIiK2yblOgGvEUyU9j4ZAqZC1gCJ6EePjZCIsXRbVdZB06GFaw8RYZAwIZApND2YTaazjZBKoNyOZA3Y4gfHbqsdwoRAZAqxZA4ESuxRsLj5H9PqTArE0icesom3IyH96QZDZD"

url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/register"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# --- 2. SET A 6-DIGIT PIN ---
# If you haven't set a 2-Step Verification PIN yet, just make one up right now (e.g., "123456").
# If you already set one in the WhatsApp Manager, use that exact PIN here.
data = {
    "messaging_product": "whatsapp",
    "pin": "227788" 
}

# --- 3. FIRE THE REQUEST ---
print("Sending registration request to Meta...")
response = requests.post(url, headers=headers, json=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")