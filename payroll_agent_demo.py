"""
Demo script for Payroll Agent functionality.
"""

import json
import datetime
from HR_root_agent.sub_agents.payroll_agent import PayrollAgent

def main():
    # Initialize the Payroll Agent
    agent = PayrollAgent()
    
    print("=== HR Payroll Agent Demo ===\n")
    
    # Set up demo data
    employees = [
        {
            "id": "EMP001",
            "name": "John Smith",
            "salary": 75000,
            "pay_type": "salary",
            "state": "CA",
            "allowances": 2,
            "deductions": {
                "401k": 0.05,
                "health_insurance": 120
            }
        },
        {
            "id": "EMP002",
            "name": "Jane Doe",
            "salary": 25,  # hourly rate
            "pay_type": "hourly",
            "hours_worked": 80,
            "overtime_hours": 5,
            "state": "NY",
            "allowances": 1,
            "deductions": {
                "401k": 0.03,
                "health_insurance": 90
            }
        },
        {
            "id": "EMP003",
            "name": "Robert Johnson",
            "salary": 120000,
            "pay_type": "salary",
            "state": "TX",
            "allowances": 3,
            "deductions": {
                "401k": 0.08,
                "health_insurance": 150,
                "dental_insurance": 30,
                "vision_insurance": 15,
                "fsa": 100
            }
        }
    ]
    
    # Set up pay period
    current_date = datetime.datetime.now()
    pay_period = {
        "start_date": (current_date - datetime.timedelta(days=14)).strftime("%Y-%m-%d"),
        "end_date": current_date.strftime("%Y-%m-%d"),
        "pay_date": (current_date + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
        "period_type": "biweekly"
    }
    
    print(f"Processing payroll for period: {pay_period['start_date']} to {pay_period['end_date']}")
    print(f"Pay date: {pay_period['pay_date']}")
    print(f"Number of employees: {len(employees)}")
    print("\n=== Processing Payroll ===\n")
    
    # Calculate payroll
    payroll_results = agent.calculate_payroll(employees, pay_period)
    
    # Display summary results
    print(f"Total Gross Pay: ${payroll_results['total_gross']:.2f}")
    print(f"Total Taxes: ${payroll_results['total_taxes']:.2f}")
    print(f"Total Deductions: ${payroll_results['total_deductions']:.2f}")
    print(f"Total Net Pay: ${payroll_results['total_net']:.2f}")
    
    # Generate a pay stub for each employee
    print("\n=== Employee Pay Stubs ===\n")
    
    for i, payment in enumerate(payroll_results["employee_payments"]):
        print(f"\nPay Stub for {payment['employee_name']} (ID: {payment['employee_id']})")
        print(f"Gross Pay: ${payment['gross_pay']:.2f}")
        print(f"Taxes: ${payment['total_taxes']:.2f}")
        
        # Print tax breakdown
        print("  Tax Breakdown:")
        for tax in payment["tax_breakdown"]:
            print(f"    {tax['name']}: ${tax['amount']:.2f}")
        
        # Print deductions
        print("  Deductions:")
        for deduction in payment["deductions_breakdown"]:
            pre_tax = "(Pre-tax)" if deduction["pre_tax"] else "(Post-tax)"
            print(f"    {deduction['name']} {pre_tax}: ${deduction['amount']:.2f}")
        
        print(f"Net Pay: ${payment['net_pay']:.2f}")
    
    # Generate payroll reports
    print("\n=== Payroll Reports ===\n")
    
    # Summary report
    summary_report = agent.generate_payroll_report(payroll_results, "summary")
    print("Summary Report:")
    print(f"Period: {summary_report['period']['start_date']} to {summary_report['period']['end_date']}")
    print(f"Employees: {summary_report['totals']['employees']}")
    print(f"Total Gross: {summary_report['totals']['gross']}")
    print(f"Total Net: {summary_report['totals']['net']}")
    
    # Tax report
    tax_report = agent.generate_payroll_report(payroll_results, "tax")
    print("\nTax Report:")
    print(f"Federal Income Tax: {tax_report['tax_liabilities']['federal_income_tax']}")
    print(f"State Income Tax: {tax_report['tax_liabilities']['state_income_tax']}")
    print(f"Social Security (Employee): {tax_report['tax_liabilities']['social_security']['employee']}")
    print(f"Social Security (Employer): {tax_report['tax_liabilities']['social_security']['employer']}")
    print(f"Medicare (Employee): {tax_report['tax_liabilities']['medicare']['employee']}")
    print(f"Medicare (Employer): {tax_report['tax_liabilities']['medicare']['employer']}")
    
    print("\n=== Payroll Agent Natural Language Queries ===\n")
    
    # Demonstrate natural language query handling
    queries = [
        "How do I calculate payroll?",
        "What tax rates do you use?",
        "Can you explain deductions?",
        "How do I generate pay stubs?",
        "What reports can you create?",
        "How do I schedule payroll?"
    ]
    
    for query in queries:
        print(f"Query: {query}")
        response = agent.ask(query)
        print(f"Response: {response}\n")
    
    print("=== Demo Complete ===")

if __name__ == "__main__":
    main()
