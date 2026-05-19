# AI Based Personalized Nutrition Planner

This project is developed for the Artificial Intelligence Methods course.

## Project Topic

Machine Learning and Genetic Algorithm based personalized nutrition planning system.

## Project Description

This system takes user information such as age, gender, height, weight, activity level and goal. Then it calculates the user's daily calorie and macronutrient targets.

After that, a machine learning model predicts possible weight change. Finally, a genetic algorithm creates a daily meal plan that is close to the user's calorie, protein, carbohydrate and fat targets.

The final system is presented with a Streamlit web interface.

## Main Features

- User information input
- BMR calculation
- TDEE calculation
- Daily target calorie calculation
- Macronutrient target calculation
- Machine learning based weight change prediction
- Genetic algorithm based meal plan optimization
- Result visualization with Streamlit

## Used Technologies

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Joblib
- Genetic Algorithm

## Project Structure

nutrition-ai-project/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── foods.csv
│   └── user_weight_data.csv
│
├── modules/
│   ├── calorie_calculator.py
│   ├── ml_model.py
│   ├── genetic_algorithm.py
│   ├── meal_planner.py
│   └── visualization.py
│
├── notebooks/
│   ├── data_analysis.ipynb
│   ├── ml_experiments.ipynb
│   └── ga_experiments.ipynb
│
├── models/
│   └── best_weight_model.pkl
│
├── outputs/
│   ├── model_results.csv
│   ├── optimization_results.csv
│   └── generated_meal_plan.csv
│
└── report/
    └── project_report.docx

## How to Run

Install dependencies:

pip install -r requirements.txt

Run the Streamlit application:

streamlit run app.py

## Current Version

The current version includes:

- Streamlit user interface
- User input form
- BMR calculation
- TDEE calculation
- Target calorie calculation
- Macronutrient calculation

Machine learning and genetic algorithm modules will be integrated in later stages.

## Team Responsibilities

| Member | Responsibility |
|---|---|
| Member 1 | Project structure, GitHub repository, Streamlit main app, integration, README |
| Member 2 | Food dataset, user weight dataset, data cleaning, data analysis |
| Member 3 | Machine learning model, model comparison, prediction module |
| Member 4 | Genetic algorithm, meal plan optimization, GA experiments |
| Member 5 | Visualization, report editing, demo video plan |

## Planned Workflow

1. Build the base Streamlit application.
2. Prepare and clean food and user datasets.
3. Train machine learning models for weight change prediction.
4. Implement genetic algorithm for meal plan optimization.
5. Integrate all modules into the Streamlit application.
6. Generate graphs and comparison tables.
7. Complete report and demo video.