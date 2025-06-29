# SkillScape Dashboard
SkillScape is an all-in-one Skill Analysis Dashboard that maps competencies to role benchmarks, uncovers skill gaps, and suggests tailored learning paths. It aligns talent development with business goals, driving performance improvements and engagement.

## 🚀 Live Demo
[SkillScape Dashboard](https://share.streamlit.io/Rushita-Mehta/SkillScape/main/dashboard.py)

## 🔍 Overview

SkillScape ingests your team’s (or your own) skill assessment data and:
1. **Maps competencies** to predefined role profiles  
2. **Identifies gaps** where skill levels fall short of benchmarks  
3. **Recommends curated learning paths**-from MOOCs to articles, to close those gaps  
4. **Generates customizable visual reports** for at-a-glance insight into skill distributions

## 🌟 Key Features

- **Role Benchmarking**: Compare actual vs. target proficiency across dozens of skills  
- **Gap Analysis**: Drill into which skills need the most attention  
- **Tailored Recommendations**: Auto-generated course lists and resources for each gap  
- **Interactive Charts**: Heatmaps, radar plots, and bar charts to explore data  
- **Progress Tracking**: Monitor improvements over time with saved snapshots  

## 🎯 Why It Matters

- **Align Learning to Strategy**: Focus training budgets on high-impact gaps  
- **Boost Engagement**: Empower individuals with clear, actionable development plans  
- **Drive Performance**: Bridge critical skill shortages before they slow your projects  
- **Data-Driven Decisions**: Turn raw assessment numbers into a prioritized roadmap 

## 🛠️ Usage
- Upload or point to your employee_data.csv (skill scores per person).
- Define or select a role_skill_requirements.csv (target benchmark per skill).
- Click “Analyze” to generate your gap heatmap and recommendation report.
- Export charts or download a PDF summary for stakeholders.
- Tip: You can swap in your own data files as long as they follow the same column schemas—see the sample CSVs in the repo.

## 🤝 Contributing
1. Fork the repo
2. Create a feature branch (git checkout -b feature/xyz)
3. Commit your changes (git commit -m "Add xyz")
4. Push and open a PR

## 📄 License
This project is released under the MIT License. See LICENSE for details.

## Local setup

```bash
git clone https://github.com/Rushita-Mehta/SkillScape.git
cd SkillScape
python -m venv .venv
.venv\Scripts\activate.bat   # or source .venv/bin/activate
pip install -r requirements.txt
streamlit run dashboard.py