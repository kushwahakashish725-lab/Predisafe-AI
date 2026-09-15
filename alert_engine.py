from datetime import datetime

ALERT_LEVELS = {

    "NORMAL": {
        "priority": "LOW",
        "color": "GREEN"
    },

    "MONITOR": {
        "priority": "MEDIUM",
        "color": "YELLOW"
    },

    "EARLY_WARNING": {
        "priority": "HIGH",
        "color": "ORANGE"
    },

    "WARNING": {
        "priority": "HIGH",
        "color": "ORANGE"
    },

    "EMERGENCY": {
        "priority": "CRITICAL",
        "color": "RED"
    }

}

def get_alert_stage(score, trend):

    if score >= 75:
        return "EMERGENCY"

    if trend == "RAPIDLY_INCREASING":

        if score >= 50:
            return "EMERGENCY"

        return "EARLY_WARNING"

    if trend == "INCREASING":

        if score >= 50:
            return "EARLY_WARNING"

        if score >= 25:
            return "MONITOR"

    # Score based decisions
    if score >= 50:
        return "WARNING"

    if score >= 25:
        return "MONITOR"

    return "NORMAL"

def create_alert(score, trend, disaster):

    disaster = disaster.upper()

    stage = get_alert_stage(
        score,
        trend
    )

    alert_info = ALERT_LEVELS[stage]

    if stage == "NORMAL":

        title = f"{disaster} Risk Normal"

        message = (
            f"Current {disaster.lower()} risk indicators "
            "are within a relatively stable range."
        )

        action = (
            "Continue monitoring environmental conditions."
        )


    elif stage == "MONITOR":

        title = f"{disaster} Risk Monitoring"

        message = (
            f"Environmental conditions indicate "
            f"a developing {disaster.lower()} risk."
        )

        action = (
            "Stay informed and monitor the risk trend "
            "for further changes."
        )


    elif stage == "EARLY_WARNING":

        title = f"Early Warning: {disaster}"

        message = (
            f"{disaster.title()} risk is increasing. "
            "Prepare for possible protective action."
        )

        action = (
            "Prepare essential items, keep communication "
            "devices charged and monitor official alerts."
        )

    elif stage == "WARNING":

        title = f"Warning: {disaster}"

        message = (
            f"{disaster.title()} risk has reached a "
            "high level."
        )

        action = (
            "Avoid unnecessary travel and prepare to "
            "move to a safer location if advised."
        )

    else:

        title = f"🚨 EMERGENCY: {disaster}"

        message = (
            f"Critical {disaster.lower()} risk detected. "
            "Immediate precautionary action may be required."
        )

        action = (
            "Follow official emergency instructions, "
            "move to a safer location when advised and "
            "contact emergency services if necessary."
        )


    return {

        "stage": stage,

        "priority": alert_info["priority"],

        "color": alert_info["color"],

        "title": title,

        "message": message,

        "recommended_action": action,

        "score": score,

        "trend": trend,

        "disaster": disaster,

        "timestamp": datetime.now().isoformat()

    }

def get_emergency_actions(disaster):

    disaster = disaster.upper()


    common_actions = [

        "Keep your phone charged.",

        "Keep essential medicines and documents ready.",

        "Stay connected with family members.",

        "Follow instructions from official authorities.",

        "Do not take unnecessary risks to observe the disaster."

    ]


    if disaster == "FLOOD":

        disaster_actions = [

            "Move towards higher and safer ground when advised.",

            "Avoid flooded roads, bridges and low-lying areas.",

            "Never walk or drive through moving flood water.",

            "Stay away from electrical equipment in flooded areas."

        ]


    elif disaster == "LANDSLIDE":

        disaster_actions = [

            "Move away from steep and unstable slopes.",

            "Avoid areas showing cracks or unusual ground movement.",

            "Stay away from valleys and channels during severe rainfall.",

            "Do not approach an active landslide zone."

        ]


    else:

        disaster_actions = [

            "Move to a safer location when advised.",

            "Follow official disaster-management instructions."

        ]


    return disaster_actions + common_actions


def analyze_alert(score, trend, disaster):

    alert = create_alert(
        score,
        trend,
        disaster
    )

    emergency = (
        alert["stage"] == "EMERGENCY"
    )

    actions = get_emergency_actions(
        disaster
    )


    return {

        "alert": alert,

        "emergency": emergency,

        "actions": actions

    }


if __name__ == "__main__":

    test_cases = [

        (18, "STABLE"),

        (32, "INCREASING"),

        (55, "INCREASING"),

        (68, "RAPIDLY_INCREASING"),

        (91, "RAPIDLY_INCREASING")

    ]


    print("\n====================================")
    print("     PREDISAFE SMART ALERT ENGINE")
    print("====================================")


    for score, trend in test_cases:

        result = analyze_alert(
            score,
            trend,
            "FLOOD"
        )


        print("\n------------------------------------")

        print(
            "Score:",
            score
        )

        print(
            "Trend:",
            trend
        )

        print(
            "Stage:",
            result["alert"]["stage"]
        )

        print(
            "Priority:",
            result["alert"]["priority"]
        )

        print(
            "Title:",
            result["alert"]["title"]
        )

        print(
            "Message:",
            result["alert"]["message"]
        )

        print(
            "Action:",
            result["alert"]["recommended_action"]
        )

        print(
            "Emergency:",
            result["emergency"]
        )