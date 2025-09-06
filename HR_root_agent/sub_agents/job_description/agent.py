# Load environment variables from .env file
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Verify API key is loaded
if not os.getenv('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

def research_role_skills_and_generate_jd(job_role: str, experience_years: int):
    """
    Research top skills for a specific job role and experience level using market data,
    then generate a comprehensive job description.
    
    Args:
        job_role (str): The job title/role (e.g., "Java Developer", "Data Scientist")
        experience_years (int): Years of experience required (e.g., 5, 3, 10)
    
    Returns:
        str: Comprehensive job description with market-researched skills and requirements
    """
    
    # Create experience level description
    if experience_years <= 2:
        level = "Junior"
        experience_desc = f"Entry to Mid-Level ({experience_years} years)"
    elif experience_years <= 5:
        level = "Mid-Level"
        experience_desc = f"Mid-Level ({experience_years} years)"
    elif experience_years <= 8:
        level = "Senior"
        experience_desc = f"Senior Level ({experience_years}+ years)"
    else:
        level = "Lead/Principal"
        experience_desc = f"Lead/Principal Level ({experience_years}+ years)"
    
    # This is where we'll use Gemini to research current market skills
    # For now, I'll implement comprehensive role-specific knowledge
    role_data = get_role_specific_data(job_role, experience_years, level)
    
    job_description = f"""### {level} {job_role}

We're looking for a highly skilled and experienced {level} {job_role} with a minimum of {experience_years} years of professional experience to join our team. The ideal candidate will be a leader in the full software development lifecycle, from concept and design to testing and deployment. You'll be responsible for building high-volume, low-latency, and high-performance applications, and will also provide guidance and mentorship to junior developers.

***

### Key Responsibilities ✍️

{role_data['responsibilities']}

***

### Required Skills & Qualifications 💻

{role_data['required_skills']}

***

### Preferred Qualifications ✅

{role_data['preferred_skills']}
"""
    
    return job_description

def get_role_specific_data(job_role: str, experience_years: int, level: str):
    """
    Get role-specific data for common tech roles.
    This would ideally use Gemini to research current market trends.
    """
    
    role_lower = job_role.lower()
    
    if "java" in role_lower and "developer" in role_lower:
        return get_java_developer_data(experience_years, level)
    elif "python" in role_lower and "developer" in role_lower:
        return get_python_developer_data(experience_years, level)
    elif "data scientist" in role_lower:
        return get_data_scientist_data(experience_years, level)
    elif "qa" in role_lower or "tester" in role_lower:
        return get_qa_tester_data(experience_years, level)
    else:
        # Generic developer template
        return get_generic_developer_data(job_role, experience_years, level)

def get_java_developer_data(experience_years: int, level: str):
    """Get Java developer specific data with current market skills"""
    
    responsibilities = """* **Design and Development:** Lead the design, development, and maintenance of robust, scalable, and secure Java-based applications and services.
* **Coding and Best Practices:** Write clean, efficient, well-documented, and testable code. Ensure all code meets high-quality standards and aligns with software development best practices.
* **Troubleshooting and Optimization:** Identify and resolve complex technical issues, and optimize application performance and scalability.
* **Collaboration:** Work closely with cross-functional teams, including product managers, architects, and QA engineers, to define, design, and ship new features.
* **Mentorship:** Provide technical guidance and mentorship to junior developers, and participate in code reviews to maintain code quality.
* **System Architecture:** Propose and implement changes to the existing Java infrastructure, and contribute to architectural reviews."""

    required_skills = f"""* **Experience:** At least {experience_years} years of hands-on experience in Java development.
* **Core Java:** Deep knowledge of Core Java, including Object-Oriented Programming (OOP) principles, data structures, algorithms, and multithreading.
* **Frameworks & Libraries:** Extensive experience with popular Java frameworks, such as **Spring Boot** and **Spring**, for building microservices and enterprise applications.
* **APIs and Web Services:** Proven ability to design and develop **RESTful APIs** and other web services.
* **Databases:** Proficiency with both relational (e.g., MySQL, PostgreSQL) and NoSQL (e.g., MongoDB) databases, including strong SQL skills.
* **Tools & Methodologies:** Expertise with build tools like **Maven** or **Gradle**, version control systems like **Git**, and a solid understanding of **Agile/Scrum** methodologies.
* **Testing:** Experience with testing frameworks like **JUnit** and **Mockito** for writing unit and integration tests.
* **Problem-Solving:** Strong analytical and problem-solving skills, with the ability to tackle complex technical challenges."""

    preferred_skills = """* Experience with **CI/CD** pipelines and tools (e.g., Jenkins, GitLab CI).
* Familiarity with cloud platforms (e.g., AWS, Azure, Google Cloud).
* Experience with containerization technologies like **Docker** and orchestration tools like **Kubernetes**.
* A Bachelor's or Master's degree in Computer Science, Software Engineering, or a related field."""

    return {
        'responsibilities': responsibilities,
        'required_skills': required_skills,
        'preferred_skills': preferred_skills
    }

def get_python_developer_data(experience_years: int, level: str):
    """Get Python developer specific data"""
    
    responsibilities = """* **Development:** Design, develop, and maintain scalable Python applications and services.
* **Code Quality:** Write clean, maintainable, and well-documented code following Python best practices.
* **API Development:** Build and maintain RESTful APIs and web services.
* **Database Integration:** Work with various databases and data storage solutions.
* **Testing:** Implement comprehensive testing strategies including unit, integration, and end-to-end tests.
* **Collaboration:** Work with cross-functional teams to deliver high-quality software solutions."""

    required_skills = f"""* **Experience:** Minimum {experience_years} years of professional Python development experience.
* **Python Expertise:** Strong knowledge of Python 3.x, including advanced features and standard library.
* **Frameworks:** Experience with web frameworks like **Django**, **Flask**, or **FastAPI**.
* **Databases:** Proficiency with SQL databases (PostgreSQL, MySQL) and ORM libraries (SQLAlchemy, Django ORM).
* **APIs:** Experience designing and consuming RESTful APIs and web services.
* **Version Control:** Proficiency with Git and collaborative development workflows.
* **Testing:** Experience with testing frameworks like **pytest**, **unittest**.
* **Problem Solving:** Strong analytical and debugging skills."""

    preferred_skills = """* Experience with cloud platforms (AWS, Azure, GCP).
* Knowledge of containerization (Docker, Kubernetes).
* Experience with data science libraries (NumPy, Pandas, Scikit-learn).
* Familiarity with CI/CD pipelines.
* Experience with message queues (Redis, RabbitMQ, Kafka)."""

    return {
        'responsibilities': responsibilities,
        'required_skills': required_skills,
        'preferred_skills': preferred_skills
    }

def get_data_scientist_data(experience_years: int, level: str):
    """Get Data Scientist specific data"""
    
    responsibilities = """* **Data Analysis:** Analyze large datasets to identify trends, patterns, and insights.
* **Model Development:** Build and deploy machine learning models for business applications.
* **Data Pipeline:** Design and maintain data pipelines and ETL processes.
* **Visualization:** Create compelling data visualizations and reports for stakeholders.
* **Research:** Stay current with latest developments in machine learning and data science.
* **Collaboration:** Work with business teams to understand requirements and translate them into analytical solutions."""

    required_skills = f"""* **Experience:** {experience_years}+ years of experience in data science or related field.
* **Programming:** Proficiency in **Python** and/or **R** for data analysis and modeling.
* **Machine Learning:** Strong knowledge of ML algorithms, statistical modeling, and data mining techniques.
* **Libraries:** Experience with data science libraries (**Pandas**, **NumPy**, **Scikit-learn**, **TensorFlow**, **PyTorch**).
* **Statistics:** Solid understanding of statistical concepts and hypothesis testing.
* **Data Visualization:** Proficiency with visualization tools (**Matplotlib**, **Seaborn**, **Plotly**, **Tableau**).
* **SQL:** Strong SQL skills for data extraction and manipulation.
* **Communication:** Ability to present complex findings to non-technical stakeholders."""

    preferred_skills = """* Experience with big data technologies (Spark, Hadoop).
* Cloud platform experience (AWS, Azure, GCP).
* Deep learning and neural networks experience.
* Experience with A/B testing and experimental design.
* Knowledge of MLOps and model deployment practices."""

    return {
        'responsibilities': responsibilities,
        'required_skills': required_skills,
        'preferred_skills': preferred_skills
    }

def get_qa_tester_data(experience_years: int, level: str):
    """Get QA Tester specific data"""
    
    responsibilities = """* **Test Planning:** Design and execute comprehensive test plans and test cases.
* **Manual Testing:** Perform functional, regression, integration, and user acceptance testing.
* **Bug Tracking:** Identify, document, and track software defects using bug tracking tools.
* **Automation:** Contribute to test automation efforts and maintain automated test suites.
* **Collaboration:** Work closely with development teams to ensure quality deliverables.
* **Documentation:** Create and maintain test documentation and procedures."""

    required_skills = f"""* **Experience:** {experience_years}+ years in software testing or quality assurance.
* **Testing Methodologies:** Strong understanding of testing methodologies and best practices.
* **Tools:** Experience with bug tracking tools (Jira, Azure DevOps) and test management tools.
* **API Testing:** Proficiency with API testing tools (Postman, SoapUI).
* **Automation:** Experience with test automation frameworks (Selenium, Cypress).
* **Databases:** Basic SQL knowledge for database testing.
* **Communication:** Strong analytical and communication skills."""

    preferred_skills = """* Programming knowledge (Python, Java, JavaScript) for test automation.
* Performance testing experience (JMeter, LoadRunner).
* Mobile testing experience (iOS/Android).
* CI/CD pipeline experience.
* Security testing knowledge."""

    return {
        'responsibilities': responsibilities,
        'required_skills': required_skills,
        'preferred_skills': preferred_skills
    }

def get_generic_developer_data(job_role: str, experience_years: int, level: str):
    """Get generic developer data for unspecified roles"""
    
    responsibilities = f"""* **Development:** Design, develop, and maintain software applications and systems.
* **Code Quality:** Write clean, maintainable, and well-documented code.
* **Problem Solving:** Identify and resolve technical issues and bugs.
* **Collaboration:** Work with cross-functional teams to deliver software solutions.
* **Best Practices:** Follow software development best practices and coding standards.
* **Continuous Learning:** Stay updated with latest technologies and industry trends."""

    required_skills = f"""* **Experience:** {experience_years}+ years of professional software development experience.
* **Programming:** Strong programming skills in relevant technologies.
* **Software Design:** Understanding of software design patterns and principles.
* **Version Control:** Proficiency with Git and collaborative development.
* **Testing:** Experience with testing frameworks and methodologies.
* **Problem Solving:** Strong analytical and debugging skills.
* **Communication:** Good communication and teamwork abilities."""

    preferred_skills = """* Experience with cloud platforms and services.
* Knowledge of CI/CD pipelines and DevOps practices.
* Familiarity with agile development methodologies.
* Experience with databases and data modeling.
* Understanding of security best practices."""

    return {
        'responsibilities': responsibilities,
        'required_skills': required_skills,
        'preferred_skills': preferred_skills
    }

job_description_agent = Agent(
    name="job_description_agent",
    model="gemini-2.0-flash",
    instruction="""You are an expert HR professional specializing in job description creation with deep knowledge of current market trends and technology skills.

When creating job descriptions, follow this exact format:

### [Level] [Role Title]

We're looking for a highly skilled and experienced [Level] [Role] with a minimum of [X] years of professional experience to join our team. The ideal candidate will be a leader in the full software development lifecycle, from concept and design to testing and deployment. You'll be responsible for building high-volume, low-latency, and high-performance applications, and will also provide guidance and mentorship to junior developers.

***

### Key Responsibilities ✍️

* **[Primary Area]:** [Detailed responsibility description]
* **[Secondary Area]:** [Detailed responsibility description]  
* **[Third Area]:** [Detailed responsibility description]
* **[Fourth Area]:** [Detailed responsibility description]
* **[Fifth Area]:** [Detailed responsibility description]
* **[Sixth Area]:** [Detailed responsibility description]

***

### Required Skills & Qualifications 💻

* **Experience:** [Experience requirement with years]
* **Core Technology:** [Core technology skills for the role]
* **Frameworks & Libraries:** [Relevant frameworks and libraries]
* **APIs and Services:** [API and service development skills]
* **Databases:** [Database technologies and skills]
* **Tools & Methodologies:** [Development tools and methodologies]
* **Testing:** [Testing frameworks and practices]
* **Problem-Solving:** [Problem-solving and analytical skills]

***

### Preferred Qualifications ✅

* [Preferred skill or experience]
* [Preferred skill or experience]
* [Preferred skill or experience]
* [Preferred skill or experience]

EXPERIENCE LEVEL GUIDELINES:
- 1-2 years: Junior level
- 3-5 years: Mid-Level  
- 6-8 years: Senior level
- 9+ years: Lead/Principal level

FOR JAVA DEVELOPERS specifically include: Spring Boot, Spring Framework, Maven/Gradle, JUnit, Mockito, REST APIs, microservices, SQL databases, Git, Agile/Scrum.

FOR PYTHON DEVELOPERS include: Django/Flask/FastAPI, SQLAlchemy, pytest, REST APIs, SQL/NoSQL databases, Git.

Always use the exact format above with emojis (✍️ 💻 ✅) and section dividers (***).""",
    description="An expert job description generator that creates comprehensive, market-competitive job descriptions with professional formatting",
    tools=[],
)