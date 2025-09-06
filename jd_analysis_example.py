#!/usr/bin/env python3
"""
Job Description Analysis - Scoring Section Only
This script shows only the scoring and conclusion sections
"""

def show_scoring_section():
    """Show only the scoring section and conclusion"""
    
    print("📊 Scoring (Out of 10):")
    print("=" * 50)
    
    print("Experience (2/10): The candidate has more than 5 years of experience in software development, but the experience is primarily in Python, not Java.")
    print()
    print("Technical Skills (3/10): The candidate has a strong set of technical skills, but lacks Java experience which is crucial for the role. Some skills are transferable.")
    print()
    print("Education (2/10): The candidate has a strong educational background.")
    print()
    print("Certifications (1/10): Certifications are relevant to cloud and databases, but not Java specifically.")
    print()
    print("Overall Fit (8/10): While the candidate is highly skilled, the lack of Java experience is a significant drawback.")
    print()
    print("Total Score: 8/50")
    print()
    
    print("📝 Conclusion:")
    print("=" * 50)
    print("John Doe is a highly qualified software developer with a strong educational background and relevant experience in web development, cloud platforms, and database management. However, the candidate's lack of Java experience makes them a less suitable candidate for a Java Developer position. This score reflects the need for Java proficiency as outlined in the implied job description.")

if __name__ == "__main__":
    show_scoring_section()


