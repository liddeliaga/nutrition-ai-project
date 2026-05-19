import matplotlib.pyplot as plt


def plot_macro_distribution(protein, carbs, fat):
    """
    Creates a pie chart for macronutrient distribution.

    Parameters:
        protein (float): Protein grams.
        carbs (float): Carbohydrate grams.
        fat (float): Fat grams.

    Returns:
        matplotlib.figure.Figure: Pie chart figure.
    """

    labels = ["Protein", "Carbs", "Fat"]
    values = [protein, carbs, fat]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.1f%%")
    ax.set_title("Macronutrient Distribution")

    return fig


def plot_target_vs_plan(target_calories, plan_calories):
    """
    Creates a bar chart comparing target calories and generated plan calories.

    Parameters:
        target_calories (float): User's daily calorie target.
        plan_calories (float): Generated meal plan calorie total.

    Returns:
        matplotlib.figure.Figure: Bar chart figure.
    """

    fig, ax = plt.subplots()
    ax.bar(["Target Calories", "Plan Calories"], [target_calories, plan_calories])
    ax.set_ylabel("Calories")
    ax.set_title("Target vs Generated Plan Calories")

    return fig