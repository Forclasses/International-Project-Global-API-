#by Arif
def recommend_activity(temp_c, rain, wind):
    """
    Function: recommend_activity(temp_c, rain, wind)
    Does: Recommends activities based on different weather ranges.
    Returns: A list of suitable activities.
    """

    activities = []

    # 1. Temperature analysis

    if temp_c < 0:
        activities = [
            "Visit a museum",
            "Go ice skating",
            "Watch a movie"
        ]

    elif temp_c < 5:
        activities = [
            "Visit a cozy cafe",
            "Go shopping",
            "Take a short winter walk"
        ]

    elif temp_c < 10:
        activities = [
            "Explore the city",
            "Visit a botanical garden",
            "Go for a short walk"
        ]

    elif temp_c < 15:
        activities = [
            "Visit a zoo",
            "Go hiking",
            "Take nature photographs"
        ]

    elif temp_c < 20:
        activities = [
            "Go cycling",
            "Explore a nearby town",
            "Play outdoor sports"
        ]

    elif temp_c < 25:
        activities = [
            "Have a picnic",
            "Go hiking",
            "Visit a lake",
            "Go cycling"
        ]

    elif temp_c < 30:
        activities = [
            "Go swimming",
            "Visit a water park",
            "Play beach volleyball"
        ]

    elif temp_c < 35:
        activities = [
            "Relax near a lake",
            "Go swimming",
            "Take an evening walk"
        ]

    else:
        activities = [
            "Visit an indoor swimming pool",
            "Watch a movie",
            "Relax in an air-conditioned place"
        ]

    # 2. Rain probability analysis

    if rain >= 70:
        activities = [
            "Visit a museum",
            "Go bowling",
            "Watch a movie"
        ]

    elif rain >= 40:
        activities = [
            "Visit a cafe",
            "Go shopping",
            "Explore indoor attractions"
        ]

    elif rain >= 20:
        activities.append("Visit a covered market")

    # 3. Wind speed analysis

    if wind >= 40:
        activities = [
            "Visit a museum",
            "Go bowling",
            "Enjoy indoor entertainment"
        ]

    elif wind >= 30:
        activities = [
            activity for activity in activities
            if activity not in [
                "Go cycling",
                "Go hiking",
                "Have a picnic",
                "Play beach volleyball",
                "Relax near a lake"
            ]
        ]

    elif wind >= 15:
        activities = [
            activity for activity in activities
            if activity not in [
                "Play beach volleyball"
            ]
        ]

    # Remove duplicate activities
    activities = list(dict.fromkeys(activities))

    return activities


def recommend_clothing(temp_c, rain, wind):
    """
    Function: recommend_clothing(temp_c, rain, wind)
    Does: Recommends clothing based on weather conditions.
    Returns: A clothing recommendation as a string.
    """

    clothing = []

    # Temperature ranges

    if temp_c < 0:
        clothing.append(
            "Wear a thick winter jacket, gloves, scarf and warm shoes"
        )

    elif temp_c < 5:
        clothing.append(
            "Wear a winter jacket and a warm sweater"
        )

    elif temp_c < 10:
        clothing.append(
            "Wear a warm jacket and long trousers"
        )

    elif temp_c < 15:
        clothing.append(
            "Wear a jacket or hoodie"
        )

    elif temp_c < 20:
        clothing.append(
            "Wear comfortable clothes and a light jacket"
        )

    elif temp_c < 25:
        clothing.append(
            "Wear a t-shirt and comfortable trousers"
        )

    elif temp_c < 30:
        clothing.append(
            "Wear light summer clothing"
        )

    elif temp_c < 35:
        clothing.append(
            "Wear breathable clothing and shorts"
        )

    else:
        clothing.append(
            "Wear loose, lightweight and breathable clothing"
        )

    # Rain conditions

    if rain >= 70:
        clothing.append(
            "Take an umbrella and a waterproof jacket"
        )

    elif rain >= 40:
        clothing.append(
            "Consider taking an umbrella or raincoat"
        )

    elif rain >= 20:
        clothing.append(
            "A small umbrella may be useful"
        )

    # Wind conditions

    if wind >= 40:
        clothing.append(
            "Wear wind-resistant clothing"
        )

    elif wind >= 25:
        clothing.append(
            "Consider an additional layer against the wind"
        )

    # Additional advice

    if temp_c >= 25:
        clothing.append(
            "Use sunscreen and sunglasses"
        )

    return ". ".join(clothing) + "."
