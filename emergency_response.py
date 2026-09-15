from datetime import datetime


def get_emergency_response(disaster="FLOOD"):

    disaster = disaster.upper()

    if disaster == "LANDSLIDE":
        safety_guide = [
            "Move away from steep slopes and unstable ground.",
            "Avoid areas with cracks, falling rocks, or unusual ground movement.",
            "Do not cross roads blocked by mud, rocks, or debris.",
            "Move to a stable and elevated safe area.",
            "Keep your phone charged and follow official warnings.",
            "Do not return until authorities declare the area safe."
        ]
    else:
        safety_guide = [
            "Move immediately to higher and safer ground if flooding increases.",
            "Avoid flooded roads, bridges, and fast-moving water.",
            "Never walk or drive through moving flood water.",
            "Keep your phone charged and carry essential medicines.",
            "Keep important documents and emergency supplies ready.",
            "Follow evacuation instructions from local authorities."
        ]

    safe_places = [
        {
            "name": "Kathmandu Emergency Shelter",
            "type": "Emergency Shelter",
            "capacity": 150,
            "status": "OPEN",
            "latitude": 27.7172,
            "longitude": 85.3240
        },
        {
            "name": "Rasuwa Safe Zone",
            "type": "Safe Zone",
            "capacity": 200,
            "status": "OPEN",
            "latitude": 28.1667,
            "longitude": 85.3333
        },
        {
            "name": "Chitwan Emergency Shelter",
            "type": "Emergency Shelter",
            "capacity": 120,
            "status": "OPEN",
            "latitude": 27.5291,
            "longitude": 84.3542
        },
        {
            "name": "Pokhara Relief Center",
            "type": "Relief Center",
            "capacity": 100,
            "status": "OPEN",
            "latitude": 28.2096,
            "longitude": 83.9856
        }
    ]

    emergency_services = [
        {
            "name": "National Emergency",
            "type": "Emergency Response",
            "number": "112",
            "description": "For immediate emergency assistance.",
            "action": "CALL"
        },
        {
            "name": "Police / Law Enforcement",
            "type": "Police",
            "number": "100",
            "description": "For police and public safety assistance.",
            "action": "CALL"
        },
        {
            "name": "Fire & Rescue",
            "type": "Fire & Rescue",
            "number": "101",
            "description": "For fire, rescue and disaster response.",
            "action": "CALL"
        },
        {
            "name": "Ambulance / Medical Emergency",
            "type": "Medical Emergency",
            "number": "108",
            "description": "For ambulance and urgent medical assistance.",
            "action": "CALL"
        }
    ]

    return {
        "success": True,
        "disaster": disaster,
        "safety_guide": safety_guide,
        "safe_places": safe_places,
        "emergency_services": emergency_services,
        "sos_available": True,
        "timestamp": datetime.now().isoformat()
    }