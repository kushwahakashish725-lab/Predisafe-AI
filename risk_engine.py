import json
import os
from datetime import datetime

def get_risk_level(score):

    if score < 25:
        return "LOW"

    elif score < 50:
        return "MODERATE"

    elif score < 75:
        return "HIGH"

    return "CRITICAL"

def analyze_trend(risk_history):

    if not risk_history:
        return {
            "trend": "STABLE",
            "change": 0,
            "message": "No previous risk data available."
        }

    if len(risk_history) == 1:
        return {
            "trend": "STABLE",
            "change": 0,
            "message": "Initial risk measurement recorded."
        }

    previous = risk_history[-2]
    current = risk_history[-1]

    change = current - previous

    if change >= 15:
        trend = "RAPIDLY_INCREASING"
        message = "Risk is increasing rapidly."

    elif change >= 5:
        trend = "INCREASING"
        message = "Risk is increasing."

    elif change <= -10:
        trend = "DECREASING"
        message = "Risk is decreasing."

    elif change <= -3:
        trend = "SLIGHTLY_DECREASING"
        message = "Risk is slightly decreasing."

    else:
        trend = "STABLE"
        message = "Risk is relatively stable."

    return {
        "trend": trend,
        "change": change,
        "message": message
    }

def determine_action(score, trend):

    # CRITICAL
    if score >= 75:

        return {
            "stage": "EMERGENCY",
            "alert": "CRITICAL FLOOD RISK",
            "action": "ACTIVATE EMERGENCY MODE",
            "priority": "URGENT"
        }

    if score >= 50 and trend in [
        "INCREASING",
        "RAPIDLY_INCREASING"
    ]:

        return {
            "stage": "EARLY_WARNING",
            "alert": "FLOOD RISK INCREASING",
            "action": "PREPARE FOR POSSIBLE EVACUATION",
            "priority": "HIGH"
        }
    if score >= 50:

        return {
            "stage": "WARNING",
            "alert": "HIGH FLOOD RISK",
            "action": "STAY ALERT AND MONITOR CONDITIONS",
            "priority": "HIGH"
        }
    if score >= 25:

        return {
            "stage": "MONITOR",
            "alert": "MODERATE FLOOD RISK",
            "action": "CONTINUE MONITORING",
            "priority": "MEDIUM"
        }

    return {
        "stage": "NORMAL",
        "alert": "LOW FLOOD RISK",
        "action": "NO IMMEDIATE ACTION REQUIRED",
        "priority": "LOW"
    }

def emergency_response(disaster="FLOOD"):

    if disaster == "FLOOD":

        return {
            "emergency_mode": True,

            "safety_steps": [
                "Move to higher ground.",
                "Avoid flooded roads and bridges.",
                "Do not walk or drive through moving water.",
                "Keep phone charged.",
                "Carry essential medicines and documents.",
                "Follow official evacuation instructions."
            ],

            "emergency_services": [
                "Local Emergency Services",
                "Police",
                "Fire & Rescue",
                "Disaster Management Authority"
            ],

            "safe_place_action":
                "Locate the nearest safe shelter or elevated area.",

            "sos_available": True
        }

    return {
        "emergency_mode": True,
        "safety_steps": [
            "Move to a safer location.",
            "Follow official emergency instructions."
        ],
        "emergency_services": [
            "Local Emergency Services"
        ],
        "safe_place_action":
            "Locate the nearest designated safe location.",
        "sos_available": True
    }

def analyze_risk(score, risk_history):

    level = get_risk_level(score)

    trend_data = analyze_trend(
        risk_history
    )

    action = determine_action(
        score,
        trend_data["trend"]
    )

    result = {
        "timestamp":
            datetime.now().isoformat(),

        "risk_score":
            score,

        "risk_level":
            level,

        "trend":
            trend_data["trend"],

        "risk_change":
            trend_data["change"],

        "trend_message":
            trend_data["message"],

        "stage":
            action["stage"],

        "alert":
            action["alert"],

        "action":
            action["action"],

        "priority":
            action["priority"]
    }
    if action["stage"] == "EMERGENCY":

        result["emergency"] = emergency_response()

    else:

        result["emergency"] = {
            "emergency_mode": False
        }

    return result

if __name__ == "__main__":

    print("\n====================================")
    print("       PREDISAFE AI")
    print("   RISK ESCALATION SIMULATION")
    print("====================================")

    risk_history = []

    simulated_scores = [
        35,
        48,
        61,
        78,
        91
    ]

    for score in simulated_scores:

        risk_history.append(score)

        result = analyze_risk(
            score,
            risk_history
        )

        print("\n------------------------------------")

        print(
            f"Risk Score : {result['risk_score']}/100"
        )

        print(
            f"Risk Level : {result['risk_level']}"
        )

        print(
            f"Trend      : {result['trend']}"
        )

        print(
            f"Stage      : {result['stage']}"
        )

        print(
            f"Alert      : {result['alert']}"
        )

        print(
            f"Action     : {result['action']}"
        )

        if result["emergency"]["emergency_mode"]:

            print("\n🚨 EMERGENCY MODE ACTIVATED")

            print("\nSafety Instructions:")

            for step in result["emergency"]["safety_steps"]:
                print(f"  • {step}")

    print("\n====================================")
    print("       SIMULATION COMPLETE")
    print("====================================")