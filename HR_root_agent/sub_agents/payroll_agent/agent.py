"""
Payroll Agent for HR AI Assistant.

This agent automates payroll processing, calculates salaries, manages taxes and deductions, 
and generates pay stubs.
"""

import os
import datetime
from typing import Dict, List, Any, Optional, Union
import json
import calendar
import math

class PayrollAgent:
    """Agent for automating payroll processing and management."""
    
    def __init__(self, name: str = "Payroll Assistant"):
        self.name = name
        self.tax_rates = self._load_tax_rates()
        self.deduction_types = self._load_deduction_types()
        self.payroll_history = {}
        
    def _load_tax_rates(self) -> Dict[str, Any]:
        """Load tax rate information for different income levels and regions."""
        return {
            "federal": [
                {"bracket": 10000, "rate": 0.10},
                {"bracket": 40000, "rate": 0.12},
                {"bracket": 85000, "rate": 0.22},
                {"bracket": 165000, "rate": 0.24},
                {"bracket": 210000, "rate": 0.32},
                {"bracket": 530000, "rate": 0.35},
                {"bracket": float('inf'), "rate": 0.37}
            ],
            "state": {
                "CA": [
                    {"bracket": 10000, "rate": 0.01},
                    {"bracket": 20000, "rate": 0.02},
                    {"bracket": 30000, "rate": 0.04},
                    {"bracket": 50000, "rate": 0.06},
                    {"bracket": 70000, "rate": 0.08},
                    {"bracket": 100000, "rate": 0.093},
                    {"bracket": float('inf'), "rate": 0.103}
                ],
                "NY": [
                    {"bracket": 12000, "rate": 0.04},
                    {"bracket": 25000, "rate": 0.045},
                    {"bracket": 50000, "rate": 0.0525},
                    {"bracket": 80000, "rate": 0.0585},
                    {"bracket": 200000, "rate": 0.0625},
                    {"bracket": float('inf'), "rate": 0.0685}
                ],
                "TX": [
                    {"bracket": float('inf'), "rate": 0.0}  # No state income tax
                ],
                "FL": [
                    {"bracket": float('inf'), "rate": 0.0}  # No state income tax
                ],
                # Add more states as needed
                "DEFAULT": [
                    {"bracket": 50000, "rate": 0.04},
                    {"bracket": 100000, "rate": 0.06},
                    {"bracket": float('inf'), "rate": 0.08}
                ]
            },
            "social_security": 0.062,  # 6.2% for Social Security
            "medicare": 0.0145,  # 1.45% for Medicare
            "futa": 0.006,  # 0.6% Federal Unemployment Tax
            "sui": {
                "CA": 0.034,
                "NY": 0.036,
                "TX": 0.027,
                "FL": 0.029,
                "DEFAULT": 0.03
            }
        }
    
    def _load_deduction_types(self) -> Dict[str, Dict[str, Any]]:
        """Load standard deduction types and their configurations."""
        return {
            "401k": {
                "type": "percentage",
                "default_rate": 0.05,
                "max_percentage": 0.15,
                "pre_tax": True,
                "description": "401(k) Retirement Plan"
            },
            "health_insurance": {
                "type": "fixed",
                "default_amount": 150.00,
                "pre_tax": True,
                "description": "Health Insurance Premium"
            },
            "dental_insurance": {
                "type": "fixed",
                "default_amount": 25.00,
                "pre_tax": True,
                "description": "Dental Insurance Premium"
            },
            "vision_insurance": {
                "type": "fixed",
                "default_amount": 15.00,
                "pre_tax": True,
                "description": "Vision Insurance Premium"
            },
            "fsa": {
                "type": "fixed",
                "default_amount": 100.00,
                "pre_tax": True,
                "description": "Flexible Spending Account"
            },
            "life_insurance": {
                "type": "fixed",
                "default_amount": 20.00,
                "pre_tax": False,
                "description": "Life Insurance Premium"
            },
            "charity": {
                "type": "percentage",
                "default_rate": 0.01,
                "max_percentage": 0.5,
                "pre_tax": False,
                "description": "Charitable Contribution"
            },
            "garnishment": {
                "type": "fixed",
                "default_amount": 0.00,
                "pre_tax": False,
                "description": "Wage Garnishment"
            }
        }
    
    def calculate_payroll(self, employees: List[Dict[str, Any]], 
                         pay_period: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate payroll for a list of employees for a specific pay period.
        
        Args:
            employees: List of employee information dictionaries including:
                - id: Employee ID
                - name: Employee name
                - salary: Annual salary or hourly rate
                - pay_type: "salary" or "hourly"
                - hours_worked: Hours worked in pay period (for hourly employees)
                - overtime_hours: Overtime hours worked (for hourly employees)
                - state: State code for tax calculation
                - deductions: Dictionary of deductions
                - allowances: Number of tax allowances
                
            pay_period: Dictionary with pay period information:
                - start_date: Start date of pay period
                - end_date: End date of pay period
                - pay_date: Date when payment is made
                - period_type: "weekly", "biweekly", "semimonthly", or "monthly"
                
        Returns:
            Dictionary containing the complete payroll calculations
        """
        payroll_results = {
            "pay_period": pay_period,
            "total_gross": 0.0,
            "total_net": 0.0,
            "total_taxes": 0.0,
            "total_deductions": 0.0,
            "employee_payments": []
        }
        
        for employee in employees:
            employee_result = self._calculate_employee_payroll(employee, pay_period)
            payroll_results["employee_payments"].append(employee_result)
            
            # Update totals
            payroll_results["total_gross"] += employee_result["gross_pay"]
            payroll_results["total_net"] += employee_result["net_pay"]
            payroll_results["total_taxes"] += employee_result["total_taxes"]
            payroll_results["total_deductions"] += employee_result["total_deductions"]
        
        # Add to payroll history
        period_key = f"{pay_period['start_date']}_{pay_period['end_date']}"
        self.payroll_history[period_key] = payroll_results
        
        return payroll_results
    
    def _calculate_employee_payroll(self, employee: Dict[str, Any], 
                                   pay_period: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate payroll for an individual employee."""
        # Calculate gross pay
        if employee.get("pay_type", "").lower() == "salary":
            # For salaried employees
            annual_salary = float(employee.get("salary", 0.0))
            
            # Determine divisor based on pay period type
            if pay_period["period_type"] == "weekly":
                divisor = 52
            elif pay_period["period_type"] == "biweekly":
                divisor = 26
            elif pay_period["period_type"] == "semimonthly":
                divisor = 24
            elif pay_period["period_type"] == "monthly":
                divisor = 12
            else:
                divisor = 26  # Default to biweekly
            
            gross_pay = annual_salary / divisor
            
        else:
            # For hourly employees
            hourly_rate = float(employee.get("salary", 0.0))  # Using salary field for hourly rate
            regular_hours = float(employee.get("hours_worked", 0.0))
            overtime_hours = float(employee.get("overtime_hours", 0.0))
            
            # Calculate regular and overtime pay
            regular_pay = hourly_rate * regular_hours
            overtime_pay = hourly_rate * 1.5 * overtime_hours
            
            gross_pay = regular_pay + overtime_pay
        
        # Calculate pre-tax deductions
        pre_tax_deductions = 0.0
        post_tax_deductions = 0.0
        deductions_breakdown = []
        
        for deduction_name, deduction_value in employee.get("deductions", {}).items():
            if deduction_name in self.deduction_types:
                deduction_info = self.deduction_types[deduction_name]
                
                # Calculate deduction amount
                if deduction_info["type"] == "percentage":
                    amount = gross_pay * float(deduction_value)
                else:
                    amount = float(deduction_value)
                
                # Add to appropriate deduction total
                if deduction_info.get("pre_tax", False):
                    pre_tax_deductions += amount
                else:
                    post_tax_deductions += amount
                
                # Add to breakdown
                deductions_breakdown.append({
                    "name": deduction_info.get("description", deduction_name),
                    "amount": amount,
                    "pre_tax": deduction_info.get("pre_tax", False)
                })
        
        # Calculate taxable income
        taxable_income = gross_pay - pre_tax_deductions
        
        # Calculate taxes
        state = employee.get("state", "DEFAULT")
        if state not in self.tax_rates["state"]:
            state = "DEFAULT"
        
        # Annualize taxable income for tax bracket calculation
        if pay_period["period_type"] == "weekly":
            annualized_income = taxable_income * 52
        elif pay_period["period_type"] == "biweekly":
            annualized_income = taxable_income * 26
        elif pay_period["period_type"] == "semimonthly":
            annualized_income = taxable_income * 24
        elif pay_period["period_type"] == "monthly":
            annualized_income = taxable_income * 12
        else:
            annualized_income = taxable_income * 26  # Default to biweekly
        
        # Calculate federal income tax
        federal_tax = self._calculate_progressive_tax(
            annualized_income, 
            self.tax_rates["federal"],
            employee.get("allowances", 0)
        )
        
        # Convert annual tax to pay period tax
        if pay_period["period_type"] == "weekly":
            federal_tax /= 52
        elif pay_period["period_type"] == "biweekly":
            federal_tax /= 26
        elif pay_period["period_type"] == "semimonthly":
            federal_tax /= 24
        elif pay_period["period_type"] == "monthly":
            federal_tax /= 12
        else:
            federal_tax /= 26  # Default to biweekly
        
        # Calculate state income tax
        state_tax = self._calculate_progressive_tax(
            annualized_income,
            self.tax_rates["state"][state],
            employee.get("allowances", 0)
        )
        
        # Convert annual state tax to pay period tax
        if pay_period["period_type"] == "weekly":
            state_tax /= 52
        elif pay_period["period_type"] == "biweekly":
            state_tax /= 26
        elif pay_period["period_type"] == "semimonthly":
            state_tax /= 24
        elif pay_period["period_type"] == "monthly":
            state_tax /= 12
        else:
            state_tax /= 26  # Default to biweekly
            
        # Calculate FICA taxes (Social Security and Medicare)
        social_security_tax = min(taxable_income * self.tax_rates["social_security"], 
                               (147000 / 26) * self.tax_rates["social_security"])  # 2024 SS wage cap
        medicare_tax = taxable_income * self.tax_rates["medicare"]
        
        # Additional Medicare tax for high earners (simplified)
        if annualized_income > 200000:
            additional_medicare = (annualized_income - 200000) * 0.009 / 26  # 0.9% additional
            medicare_tax += additional_medicare
        
        # Calculate total taxes
        total_taxes = federal_tax + state_tax + social_security_tax + medicare_tax
        
        # Calculate net pay
        net_pay = gross_pay - pre_tax_deductions - total_taxes - post_tax_deductions
        
        # Build tax breakdown
        tax_breakdown = [
            {"name": "Federal Income Tax", "amount": federal_tax},
            {"name": "State Income Tax", "amount": state_tax},
            {"name": "Social Security", "amount": social_security_tax},
            {"name": "Medicare", "amount": medicare_tax}
        ]
        
        # Create pay stub data
        pay_stub = {
            "employee_id": employee.get("id", ""),
            "employee_name": employee.get("name", ""),
            "pay_period": pay_period,
            "gross_pay": gross_pay,
            "pre_tax_deductions": pre_tax_deductions,
            "taxable_income": taxable_income,
            "total_taxes": total_taxes,
            "post_tax_deductions": post_tax_deductions,
            "net_pay": net_pay,
            "tax_breakdown": tax_breakdown,
            "deductions_breakdown": deductions_breakdown
        }
        
        # For hourly employees, include hours details
        if employee.get("pay_type", "").lower() != "salary":
            pay_stub["regular_hours"] = float(employee.get("hours_worked", 0.0))
            pay_stub["overtime_hours"] = float(employee.get("overtime_hours", 0.0))
            pay_stub["hourly_rate"] = float(employee.get("salary", 0.0))
            pay_stub["regular_pay"] = pay_stub["hourly_rate"] * pay_stub["regular_hours"]
            pay_stub["overtime_pay"] = pay_stub["hourly_rate"] * 1.5 * pay_stub["overtime_hours"]
        
        return pay_stub
    
    def _calculate_progressive_tax(self, income: float, 
                                  brackets: List[Dict[str, float]],
                                  allowances: int = 0) -> float:
        """Calculate tax using progressive tax brackets."""
        # Apply standard deduction based on allowances (simplified)
        standard_deduction = allowances * 4050  # Simplified allowance value
        taxable_income = max(0, income - standard_deduction)
        
        total_tax = 0.0
        previous_bracket = 0.0
        
        for bracket in brackets:
            bracket_limit = bracket["bracket"]
            rate = bracket["rate"]
            
            if taxable_income > previous_bracket:
                taxable_in_bracket = min(taxable_income, bracket_limit) - previous_bracket
                tax_in_bracket = taxable_in_bracket * rate
                total_tax += tax_in_bracket
                
            previous_bracket = bracket_limit
            
            if taxable_income <= bracket_limit:
                break
                
        return total_tax
    
    def generate_pay_stub(self, employee_payment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a detailed pay stub for an employee payment.
        
        Args:
            employee_payment: Dictionary with employee payment details
            
        Returns:
            Dictionary containing formatted pay stub information
        """
        # Format currency values
        formatted_stub = {
            "employee_id": employee_payment.get("employee_id", ""),
            "employee_name": employee_payment.get("employee_name", ""),
            "pay_period": {
                "start_date": employee_payment.get("pay_period", {}).get("start_date", ""),
                "end_date": employee_payment.get("pay_period", {}).get("end_date", ""),
                "pay_date": employee_payment.get("pay_period", {}).get("pay_date", "")
            },
            "gross_pay": f"${employee_payment.get('gross_pay', 0.0):.2f}",
            "net_pay": f"${employee_payment.get('net_pay', 0.0):.2f}",
            "taxes": [],
            "deductions": [],
            "ytd": {
                "gross": f"$0.00",  # In a real system, would calculate YTD values
                "net": f"$0.00",
                "federal_tax": f"$0.00",
                "state_tax": f"$0.00",
                "social_security": f"$0.00",
                "medicare": f"$0.00"
            }
        }
        
        # Format tax breakdown
        for tax in employee_payment.get("tax_breakdown", []):
            formatted_stub["taxes"].append({
                "name": tax.get("name", ""),
                "amount": f"${tax.get('amount', 0.0):.2f}"
            })
        
        # Format deductions breakdown
        for deduction in employee_payment.get("deductions_breakdown", []):
            formatted_stub["deductions"].append({
                "name": deduction.get("name", ""),
                "amount": f"${deduction.get('amount', 0.0):.2f}",
                "pre_tax": deduction.get("pre_tax", False)
            })
        
        # Add hourly details if applicable
        if "hourly_rate" in employee_payment:
            formatted_stub["hourly_details"] = {
                "hourly_rate": f"${employee_payment.get('hourly_rate', 0.0):.2f}",
                "regular_hours": f"{employee_payment.get('regular_hours', 0.0):.2f}",
                "overtime_hours": f"{employee_payment.get('overtime_hours', 0.0):.2f}",
                "regular_pay": f"${employee_payment.get('regular_pay', 0.0):.2f}",
                "overtime_pay": f"${employee_payment.get('overtime_pay', 0.0):.2f}"
            }
        else:
            formatted_stub["salary_details"] = {
                "annual_salary": f"${employee_payment.get('annual_salary', 0.0):.2f}"
            }
        
        return formatted_stub
    
    def calculate_employer_taxes(self, payroll_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate employer portion of taxes based on payroll data.
        
        Args:
            payroll_data: Dictionary with payroll calculation results
            
        Returns:
            Dictionary containing employer tax obligations
        """
        employer_taxes = {
            "social_security": 0.0,
            "medicare": 0.0,
            "futa": 0.0,
            "sui": 0.0,
            "total": 0.0
        }
        
        for payment in payroll_data.get("employee_payments", []):
            taxable_income = payment.get("taxable_income", 0.0)
            state = payment.get("employee_state", "DEFAULT")
            
            # Employer Social Security (matches employee contribution)
            social_security = min(taxable_income * self.tax_rates["social_security"], 
                               (147000 / 26) * self.tax_rates["social_security"])
            
            # Employer Medicare (matches employee contribution)
            medicare = taxable_income * self.tax_rates["medicare"]
            
            # Federal Unemployment Tax
            futa = min(taxable_income, 7000 / 26) * self.tax_rates["futa"]
            
            # State Unemployment Insurance
            sui_rate = self.tax_rates["sui"].get(state, self.tax_rates["sui"]["DEFAULT"])
            sui = min(taxable_income, 7000 / 26) * sui_rate
            
            # Add to totals
            employer_taxes["social_security"] += social_security
            employer_taxes["medicare"] += medicare
            employer_taxes["futa"] += futa
            employer_taxes["sui"] += sui
        
        # Calculate total
        employer_taxes["total"] = (
            employer_taxes["social_security"] +
            employer_taxes["medicare"] +
            employer_taxes["futa"] +
            employer_taxes["sui"]
        )
        
        return employer_taxes
    
    def run_scheduled_payroll(self, company_data: Dict[str, Any], 
                             schedule_date: str) -> Dict[str, Any]:
        """
        Run a scheduled payroll based on the company's pay schedule.
        
        Args:
            company_data: Dictionary with company and employee information
            schedule_date: The date to run the payroll for
            
        Returns:
            Dictionary containing the payroll results
        """
        # Parse the schedule date
        run_date = datetime.datetime.strptime(schedule_date, "%Y-%m-%d").date()
        
        # Determine pay period based on company's pay schedule
        pay_schedule = company_data.get("pay_schedule", "biweekly")
        
        if pay_schedule == "weekly":
            # Weekly payroll - every Friday
            days_to_friday = (4 - run_date.weekday()) % 7
            pay_date = run_date + datetime.timedelta(days=days_to_friday)
            
            # Period is previous Saturday to Friday
            end_date = pay_date
            start_date = end_date - datetime.timedelta(days=6)
            
            period_type = "weekly"
            
        elif pay_schedule == "biweekly":
            # Biweekly payroll - every other Friday
            # Determine if this is a pay week (simplified)
            # In a real system, would reference a calendar of pay dates
            is_pay_week = (run_date.isocalendar()[1] % 2) == 0
            
            if is_pay_week:
                days_to_friday = (4 - run_date.weekday()) % 7
                pay_date = run_date + datetime.timedelta(days=days_to_friday)
                
                # Period is previous two weeks
                end_date = pay_date
                start_date = end_date - datetime.timedelta(days=13)
                
                period_type = "biweekly"
            else:
                # Not a pay week
                return {
                    "status": "skipped",
                    "message": f"No payroll scheduled for {schedule_date} (not a pay week)"
                }
                
        elif pay_schedule == "semimonthly":
            # Semimonthly - 15th and last day of month
            day_of_month = run_date.day
            
            if day_of_month == 15 or day_of_month == run_date.replace(day=1).day + calendar.monthrange(run_date.year, run_date.month)[1] - 1:
                pay_date = run_date
                
                if day_of_month == 15:
                    # First half of month
                    start_date = run_date.replace(day=1)
                    end_date = run_date
                else:
                    # Second half of month
                    start_date = run_date.replace(day=16)
                    end_date = run_date
                
                period_type = "semimonthly"
            else:
                # Not a pay day
                return {
                    "status": "skipped",
                    "message": f"No payroll scheduled for {schedule_date} (not a pay date)"
                }
                
        elif pay_schedule == "monthly":
            # Monthly - last day of month
            is_last_day = run_date.day == calendar.monthrange(run_date.year, run_date.month)[1]
            
            if is_last_day:
                pay_date = run_date
                
                # Period is entire month
                start_date = run_date.replace(day=1)
                end_date = run_date
                
                period_type = "monthly"
            else:
                # Not a pay day
                return {
                    "status": "skipped",
                    "message": f"No payroll scheduled for {schedule_date} (not a pay date)"
                }
        else:
            # Invalid pay schedule
            return {
                "status": "error",
                "message": f"Invalid pay schedule: {pay_schedule}"
            }
        
        # Format dates as strings
        pay_period = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "pay_date": pay_date.strftime("%Y-%m-%d"),
            "period_type": period_type
        }
        
        # Run the payroll
        try:
            employees = company_data.get("employees", [])
            payroll_results = self.calculate_payroll(employees, pay_period)
            
            # Calculate employer taxes
            employer_taxes = self.calculate_employer_taxes(payroll_results)
            payroll_results["employer_taxes"] = employer_taxes
            
            return {
                "status": "success",
                "message": f"Payroll processed for period {pay_period['start_date']} to {pay_period['end_date']}",
                "payroll_data": payroll_results
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing payroll: {str(e)}"
            }
    
    def generate_payroll_report(self, payroll_data: Dict[str, Any], 
                               report_type: str = "summary") -> Dict[str, Any]:
        """
        Generate a payroll report based on payroll data.
        
        Args:
            payroll_data: Dictionary with payroll calculation results
            report_type: Type of report to generate ("summary", "detailed", "tax")
            
        Returns:
            Dictionary containing the formatted report data
        """
        if report_type == "summary":
            # Generate summary report
            report = {
                "period": {
                    "start_date": payroll_data.get("pay_period", {}).get("start_date", ""),
                    "end_date": payroll_data.get("pay_period", {}).get("end_date", ""),
                    "pay_date": payroll_data.get("pay_period", {}).get("pay_date", ""),
                    "type": payroll_data.get("pay_period", {}).get("period_type", "")
                },
                "totals": {
                    "employees": len(payroll_data.get("employee_payments", [])),
                    "gross": f"${payroll_data.get('total_gross', 0.0):.2f}",
                    "taxes": f"${payroll_data.get('total_taxes', 0.0):.2f}",
                    "deductions": f"${payroll_data.get('total_deductions', 0.0):.2f}",
                    "net": f"${payroll_data.get('total_net', 0.0):.2f}"
                },
                "employer_taxes": {
                    "social_security": f"${payroll_data.get('employer_taxes', {}).get('social_security', 0.0):.2f}",
                    "medicare": f"${payroll_data.get('employer_taxes', {}).get('medicare', 0.0):.2f}",
                    "futa": f"${payroll_data.get('employer_taxes', {}).get('futa', 0.0):.2f}",
                    "sui": f"${payroll_data.get('employer_taxes', {}).get('sui', 0.0):.2f}",
                    "total": f"${payroll_data.get('employer_taxes', {}).get('total', 0.0):.2f}"
                }
            }
            
        elif report_type == "detailed":
            # Generate detailed report with individual employee information
            employee_details = []
            
            for payment in payroll_data.get("employee_payments", []):
                employee_details.append({
                    "id": payment.get("employee_id", ""),
                    "name": payment.get("employee_name", ""),
                    "gross": f"${payment.get('gross_pay', 0.0):.2f}",
                    "taxes": f"${payment.get('total_taxes', 0.0):.2f}",
                    "deductions": f"${payment.get('pre_tax_deductions', 0.0) + payment.get('post_tax_deductions', 0.0):.2f}",
                    "net": f"${payment.get('net_pay', 0.0):.2f}"
                })
            
            report = {
                "period": {
                    "start_date": payroll_data.get("pay_period", {}).get("start_date", ""),
                    "end_date": payroll_data.get("pay_period", {}).get("end_date", ""),
                    "pay_date": payroll_data.get("pay_period", {}).get("pay_date", ""),
                    "type": payroll_data.get("pay_period", {}).get("period_type", "")
                },
                "totals": {
                    "employees": len(payroll_data.get("employee_payments", [])),
                    "gross": f"${payroll_data.get('total_gross', 0.0):.2f}",
                    "taxes": f"${payroll_data.get('total_taxes', 0.0):.2f}",
                    "deductions": f"${payroll_data.get('total_deductions', 0.0):.2f}",
                    "net": f"${payroll_data.get('total_net', 0.0):.2f}"
                },
                "employee_details": employee_details
            }
            
        elif report_type == "tax":
            # Generate tax report
            tax_details = {
                "federal_income_tax": 0.0,
                "state_income_tax": 0.0,
                "social_security_employee": 0.0,
                "social_security_employer": 0.0,
                "medicare_employee": 0.0,
                "medicare_employer": 0.0,
                "futa": 0.0,
                "sui": 0.0
            }
            
            # Calculate employee tax totals
            for payment in payroll_data.get("employee_payments", []):
                for tax in payment.get("tax_breakdown", []):
                    if tax.get("name") == "Federal Income Tax":
                        tax_details["federal_income_tax"] += tax.get("amount", 0.0)
                    elif tax.get("name") == "State Income Tax":
                        tax_details["state_income_tax"] += tax.get("amount", 0.0)
                    elif tax.get("name") == "Social Security":
                        tax_details["social_security_employee"] += tax.get("amount", 0.0)
                    elif tax.get("name") == "Medicare":
                        tax_details["medicare_employee"] += tax.get("amount", 0.0)
            
            # Add employer taxes
            tax_details["social_security_employer"] = payroll_data.get("employer_taxes", {}).get("social_security", 0.0)
            tax_details["medicare_employer"] = payroll_data.get("employer_taxes", {}).get("medicare", 0.0)
            tax_details["futa"] = payroll_data.get("employer_taxes", {}).get("futa", 0.0)
            tax_details["sui"] = payroll_data.get("employer_taxes", {}).get("sui", 0.0)
            
            # Format report
            report = {
                "period": {
                    "start_date": payroll_data.get("pay_period", {}).get("start_date", ""),
                    "end_date": payroll_data.get("pay_period", {}).get("end_date", ""),
                    "pay_date": payroll_data.get("pay_period", {}).get("pay_date", ""),
                    "type": payroll_data.get("pay_period", {}).get("period_type", "")
                },
                "tax_liabilities": {
                    "federal_income_tax": f"${tax_details['federal_income_tax']:.2f}",
                    "state_income_tax": f"${tax_details['state_income_tax']:.2f}",
                    "social_security": {
                        "employee": f"${tax_details['social_security_employee']:.2f}",
                        "employer": f"${tax_details['social_security_employer']:.2f}",
                        "total": f"${tax_details['social_security_employee'] + tax_details['social_security_employer']:.2f}"
                    },
                    "medicare": {
                        "employee": f"${tax_details['medicare_employee']:.2f}",
                        "employer": f"${tax_details['medicare_employer']:.2f}",
                        "total": f"${tax_details['medicare_employee'] + tax_details['medicare_employer']:.2f}"
                    },
                    "futa": f"${tax_details['futa']:.2f}",
                    "sui": f"${tax_details['sui']:.2f}",
                    "total_tax_liability": f"${sum(tax_details.values()):.2f}"
                }
            }
            
        else:
            # Invalid report type
            report = {
                "status": "error",
                "message": f"Invalid report type: {report_type}"
            }
        
        return report
    
    def get_payroll_history(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Retrieve payroll history for a given date range.
        
        Args:
            start_date: Start date for history retrieval (format: YYYY-MM-DD)
            end_date: End date for history retrieval (format: YYYY-MM-DD)
            
        Returns:
            Dictionary containing payroll history records
        """
        if not self.payroll_history:
            return {
                "status": "success",
                "message": "No payroll history found",
                "records": []
            }
        
        # If dates are provided, filter by date range
        filtered_history = {}
        
        if start_date or end_date:
            start = datetime.datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else datetime.date.min
            end = datetime.datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else datetime.date.max
            
            for period_key, payroll_data in self.payroll_history.items():
                period_start = datetime.datetime.strptime(
                    payroll_data.get("pay_period", {}).get("start_date", ""), 
                    "%Y-%m-%d"
                ).date()
                
                if start <= period_start <= end:
                    filtered_history[period_key] = payroll_data
        else:
            filtered_history = self.payroll_history
        
        # Format history records for response
        records = []
        
        for period_key, payroll_data in filtered_history.items():
            records.append({
                "period": {
                    "start_date": payroll_data.get("pay_period", {}).get("start_date", ""),
                    "end_date": payroll_data.get("pay_period", {}).get("end_date", ""),
                    "pay_date": payroll_data.get("pay_period", {}).get("pay_date", ""),
                    "type": payroll_data.get("pay_period", {}).get("period_type", "")
                },
                "totals": {
                    "employees": len(payroll_data.get("employee_payments", [])),
                    "gross": payroll_data.get("total_gross", 0.0),
                    "net": payroll_data.get("total_net", 0.0)
                }
            })
        
        return {
            "status": "success",
            "message": f"Retrieved {len(records)} payroll records",
            "records": records
        }
    
    def ask(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Process a natural language query about payroll.
        
        Args:
            query: The query text
            context: Additional context like company data
            
        Returns:
            Response to the query
        """
        query_lower = query.lower()
        
        if "calculate" in query_lower and "payroll" in query_lower:
            return "I can calculate payroll for your employees based on their salary or hourly rate, taxes, and deductions. Would you like me to run a payroll calculation?"
        
        elif "tax" in query_lower and ("rates" in query_lower or "brackets" in query_lower):
            return "I can provide information on current tax rates and brackets for different income levels and states. Federal income tax ranges from 10% to 37% depending on income level."
        
        elif "deduction" in query_lower:
            return "I can help set up various deductions such as 401(k), health insurance, dental insurance, FSA, and more. These can be fixed amounts or percentage-based deductions."
        
        elif "pay stub" in query_lower or "paystub" in query_lower:
            return "I can generate detailed pay stubs for your employees showing gross pay, taxes, deductions, and net pay. Would you like me to create a sample pay stub?"
        
        elif "report" in query_lower:
            return "I can generate various payroll reports including summary reports, detailed reports, and tax liability reports. What type of report would you like to see?"
        
        elif "schedule" in query_lower:
            return "I can help set up and run scheduled payrolls on a weekly, biweekly, semimonthly, or monthly basis. When would you like to schedule your next payroll run?"
        
        else:
            return "I can help with payroll processing, including calculating wages, taxes, and deductions, generating pay stubs, and creating payroll reports. What specific aspect of payroll would you like assistance with?"

# Example usage:
# agent = PayrollAgent()
# 
# employees = [
#     {
#         "id": "EMP001",
#         "name": "John Smith",
#         "salary": 75000,
#         "pay_type": "salary",
#         "state": "CA",
#         "allowances": 2,
#         "deductions": {
#             "401k": 0.05,
#             "health_insurance": 120
#         }
#     },
#     {
#         "id": "EMP002",
#         "name": "Jane Doe",
#         "salary": 25,  # hourly rate
#         "pay_type": "hourly",
#         "hours_worked": 80,
#         "overtime_hours": 5,
#         "state": "NY",
#         "allowances": 1,
#         "deductions": {
#             "401k": 0.03,
#             "health_insurance": 90
#         }
#     }
# ]
# 
# pay_period = {
#     "start_date": "2025-09-01",
#     "end_date": "2025-09-15",
#     "pay_date": "2025-09-20",
#     "period_type": "biweekly"
# }
# 
# payroll_results = agent.calculate_payroll(employees, pay_period)
# 
# # Generate a pay stub for the first employee
# pay_stub = agent.generate_pay_stub(payroll_results["employee_payments"][0])
# 
# # Generate a summary report
# report = agent.generate_payroll_report(payroll_results, "summary")
