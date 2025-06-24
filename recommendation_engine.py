import pandas as pd

def load_data():
    employees = pd.read_csv("employee_data.csv")
    role_requirements = pd.read_csv("role_skill_requirements.csv")
    return employees, role_requirements

def calculate_skill_gaps(employees, role_requirements):
    recommendations = []

    # Loop through each employee record
    for idx, row in employees.iterrows():
        role = row["Role"]
        emp_id = row["EmployeeID"]
        name = row["Name"]
        # Get required skills for this role
        req_skills = role_requirements[role_requirements["Role"] == role]
        for _, req in req_skills.iterrows():
            skill = req["Skill"]
            required_level = req["RequiredProficiency"]
            # Get current proficiency; if the column is missing, assume 0
            current_level = row.get(skill, 0)
            gap = required_level - current_level
            if gap > 0:
                # For demo purposes, map a skill gap to a generic training course.
                training_course = f"Advanced {skill} Training"
                recommendations.append({
                    "EmployeeID": emp_id,
                    "Name": name,
                    "Role": role,
                    "Skill": skill,
                    "CurrentProficiency": current_level,
                    "RequiredProficiency": required_level,
                    "Gap": gap,
                    "RecommendedTraining": training_course
                })
    return pd.DataFrame(recommendations)

if __name__ == "__main__":
    employees, role_requirements = load_data()
    recs = calculate_skill_gaps(employees, role_requirements)
    recs.to_csv("training_recommendations.csv", index=False)
    print("Training recommendations generated and saved to 'training_recommendations.csv'.")
