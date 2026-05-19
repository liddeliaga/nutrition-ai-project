def predict_weight_change(user_data):
    """
    Placeholder ML prediction function.

    Later, this function will load a trained machine learning model
    and predict weekly weight change based on user data.

    Parameters:
        user_data (dict): User information and nutrition targets.

    Returns:
        float: Predicted weekly weight change in kg.
    """

    goal = user_data.get("goal", "maintain_weight")

    if goal == "lose_weight":
        return -0.4

    if goal == "gain_weight":
        return 0.3

    return 0.0