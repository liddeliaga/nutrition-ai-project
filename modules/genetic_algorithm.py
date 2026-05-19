def calculate_fitness(plan_totals, targets):
    """
    Calculates fitness score based on the difference between
    generated meal plan totals and user targets.

    Parameters:
        plan_totals (dict): Total calories and macros of generated plan.
        targets (dict): Target calories and macros.

    Returns:
        float: Fitness score.
    """

    calorie_error = abs(targets["calories"] - plan_totals["calories"])
    protein_error = abs(targets["protein"] - plan_totals["protein"])
    carbs_error = abs(targets["carbs"] - plan_totals["carbs"])
    fat_error = abs(targets["fat"] - plan_totals["fat"])

    fitness = (
        10000
        - calorie_error * 2
        - protein_error * 5
        - carbs_error * 2
        - fat_error * 3
    )

    return round(fitness, 2)


def run_genetic_algorithm(targets):
    """
    Placeholder genetic algorithm function.

    Later, this function will create a population of meal plans,
    apply selection, crossover and mutation, then return the best plan.

    Parameters:
        targets (dict): Target calories and macros.

    Returns:
        dict: Placeholder result.
    """

    return {
        "best_fitness": 960,
        "mutation_rate": 0.10,
        "population_size": 100,
        "generation_count": 50
    }