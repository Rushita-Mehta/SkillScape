import pandas as pd

def generate_consultative_insights(employees, recommendations):
    """
    Provides consultative insights for each combination of role and grade.
    Adjust cost-saving or other parameters as needed for your scenario.
    """
    insights = []
    training_effectiveness = 0.70
    cost_savings_per_gap_point_by_grade = {
        "Junior": 3000,
        "Mid": 5000,
        "Senior": 8000
    }
    competitor_productivity_improvement = 0.10  # 10%
    
    # Merge the recommendations with employee grade data.
    merged = recommendations.merge(
        employees[['EmployeeID', 'Grade', 'Role']], 
        on=['EmployeeID', 'Role'], 
        how='left'
    )
    
    # Group by Role and Grade.
    grouped = merged.groupby(['Role', 'Grade'])
    
    for (role, grade), group in grouped:
        avg_gap = group["Gap"].mean()
        expected_improvement = avg_gap * training_effectiveness
        num_employees = group["EmployeeID"].nunique()
        
        # Get the cost factor for the grade; default to 5000 if not found.
        cost_factor = cost_savings_per_gap_point_by_grade.get(grade, 5000)
        estimated_cost_savings = expected_improvement * cost_factor * num_employees
        
        insights.append({
            "Role": role,
            "Grade": grade,
            "AverageGap": round(avg_gap, 2),
            "ExpectedImprovement": round(expected_improvement, 2),
            "NumEmployees": num_employees,
            "EstimatedCostSavings": round(estimated_cost_savings, 2),
        })
    
    return pd.DataFrame(insights)
