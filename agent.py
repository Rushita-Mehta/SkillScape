import schedule
import time
import os
from recommendation_engine import load_data, calculate_skill_gaps

def update_recommendations():
    print("Agent: Checking for new data and updating training recommendations...")
    # In a real-world scenario, you might check a database or a data directory.
    if os.path.exists("employee_data.csv") and os.path.exists("role_skill_requirements.csv"):
        employees, role_requirements = load_data()
        recs = calculate_skill_gaps(employees, role_requirements)
        recs.to_csv("training_recommendations.csv", index=False)
        print("Agent: Recommendations updated successfully!")
    else:
        print("Agent: Required data files not found.")

if __name__ == "__main__":
    # Schedule the agent to run every 10 minutes (for demo purposes)
    schedule.every(10).minutes.do(update_recommendations)
    print("Agent scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)
