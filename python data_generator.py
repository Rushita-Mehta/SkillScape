import pandas as pd
import numpy as np
import random

# Seed for reproducibility
np.random.seed(42)

# Define the number of synthetic employees
num_employees = 60

# Define roles and a new list for grade levels
roles = ["Software Engineer", "Data Analyst", "Product Manager", "HR Manager", "Marketing Specialist"]
grades = ["Junior", "Mid", "Senior"]

# Define a mapping of roles to required skills (each required proficiency is set to 5)
role_skill_requirements = {
    "Software Engineer": {"Python": 5, "Algorithms": 5, "System Design": 5},
    "Data Analyst": {"SQL": 5, "Statistics": 5, "Data Visualization": 5},
    "Product Manager": {"Market Analysis": 5, "Communication": 5, "Roadmapping": 5},
    "HR Manager": {"Recruitment": 5, "Employee Relations": 5, "Compliance": 5},
    "Marketing Specialist": {"SEO": 5, "Content Creation": 5, "Social Media": 5},
}

# Generate synthetic employee data for 60 employees
employees = []
for i in range(num_employees):
    name = f"Employee_{i+1}"  # Synthetic names like Employee_1, Employee_2, etc.
    role = random.choice(roles)
    grade = random.choice(grades)  # Assign a grade level randomly
    req_skills = role_skill_requirements[role]
    # Assign a random proficiency level between 1 and 5 for each required skill
    current_skills = {skill: np.random.randint(1, 6) for skill in req_skills}
    employees.append({
        "EmployeeID": i + 1,
        "Name": name,
        "Role": role,
        "Grade": grade,  # New column for grade
        **current_skills  # Unpack the current skills as separate columns
    })

# Save employee data to CSV
df_employees = pd.DataFrame(employees)
df_employees.to_csv("employee_data.csv", index=False)

# Also save the role-skill requirements for reference
role_data = []
for role, skills in role_skill_requirements.items():
    for skill, req in skills.items():
        role_data.append({
            "Role": role,
            "Skill": skill,
            "RequiredProficiency": req
        })
df_roles = pd.DataFrame(role_data)
df_roles.to_csv("role_skill_requirements.csv", index=False)

print("Synthetic data generated: 'employee_data.csv' with 60 employees (including grade) and 'role_skill_requirements.csv' with 15 rows.")
