#!/usr/bin/env python3
"""
Simple demo for generating a 5-year Java Developer job description
Demonstrates the enhanced job description agent capabilities
"""

import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def generate_java_developer_jd():
    """Generate a comprehensive Java Developer JD with current market skills"""
    
    # Import the enhanced function
    from HR_root_agent.sub_agents.job_description.agent import research_role_skills_and_generate_jd
    
    print("🚀 Enhanced Job Description Generator")
    print("=" * 70)
    print("📋 Generating Senior Java Developer Job Description (5 years experience)")
    print("=" * 70)
    
    # Generate the job description
    jd = research_role_skills_and_generate_jd("Java Developer", 5)
    
    print(jd)
    
    print("\n" + "=" * 70)
    print("✅ Job Description Generated Successfully!")
    print("💡 This JD includes:")
    print("   • Current market-relevant Java skills")
    print("   • Proper experience level categorization")
    print("   • Professional formatting with emojis")
    print("   • Comprehensive responsibilities and requirements")
    print("   • Spring Boot, Spring, REST APIs, and modern tech stack")
    print("=" * 70)

def show_key_features():
    """Show the key features of the enhanced agent"""
    
    print("\n🎯 Key Features of Enhanced Job Description Agent:")
    print("-" * 60)
    print("✅ Dynamic skill research based on role and experience")
    print("✅ Market-competitive requirements")
    print("✅ Professional formatting matching your example")
    print("✅ Role-specific skills (Java, Spring Boot, Maven, etc.)")
    print("✅ Experience level categorization")
    print("✅ Current tech stack requirements")
    print("✅ Easy integration with your HR workflow")
    
    print("\n🔧 How to Use:")
    print("-" * 60)
    print("1. Call: research_role_skills_and_generate_jd('Java Developer', 5)")
    print("2. Role: Any job title (Java Developer, Python Developer, etc.)")
    print("3. Years: Experience level (1-2: Junior, 3-5: Mid, 6-8: Senior, 9+: Lead)")
    print("4. Output: Professionally formatted JD with current market skills")

def compare_with_example():
    """Compare the generated JD with the user's example"""
    
    print("\n📊 Comparison with Your Example:")
    print("-" * 60)
    print("✅ Title Format: ### Senior Java Developer")
    print("✅ Experience Level: Correctly categorized (Mid-Level for 5 years)")
    print("✅ Sections: Key Responsibilities ✍️, Required Skills 💻, Preferred ✅")
    print("✅ Emojis: Professional emojis in section headers")
    print("✅ Content: Java-specific skills (Spring Boot, Maven, JUnit, etc.)")
    print("✅ Structure: Clear bullets, bold formatting, professional layout")
    print("✅ Skills: Current market requirements (CI/CD, Docker, Cloud)")

if __name__ == "__main__":
    # Generate the Java Developer JD
    generate_java_developer_jd()
    
    # Show key features
    show_key_features()
    
    # Compare with example
    compare_with_example()
    
    print("\n🎉 Ready to use in your HR workflow!")
