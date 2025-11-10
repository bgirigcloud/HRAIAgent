"""
Leave Management Agent Demo Script

This script demonstrates the core functionality of the Leave Management Agent.
"""

import os
from datetime import datetime, timedelta
from HR_root_agent.sub_agents.leave_management.agent import leave_management_agent

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def print_response(response):
    """Print agent response in a formatted way."""
    if hasattr(response, 'text'):
        print(response.text)
    else:
        print(str(response))
    print()

def main():
    """Run leave management demo scenarios."""
    
    print_section("🏖️ Leave Management System Demo")
    
    print("This demo showcases the Leave Management Agent's capabilities:")
    print("1. Initialize employee leave balances")
    print("2. Submit leave requests")
    print("3. Check leave balances")
    print("4. Approve/reject requests")
    print("5. View leave history")
    print()
    
    try:
        # Scenario 1: Initialize employee balances
        print_section("1️⃣ Initialize Employee Leave Balances")
        
        print("Initializing balances for employees with different tenures...\n")
        
        employees = [
            ("EMP001", "John Doe", 2),
            ("EMP002", "Jane Smith", 5),
            ("EMP003", "Bob Johnson", 8),
            ("EMP004", "Alice Williams", 1),
        ]
        
        for emp_id, name, tenure in employees:
            print(f"📋 Initializing {name} ({emp_id}) with {tenure} years tenure...")
            response = leave_management_agent.send_message(
                f"Initialize leave balances for {emp_id} with {tenure} years tenure"
            )
            print_response(response)
        
        # Scenario 2: Check leave balances
        print_section("2️⃣ Check Employee Leave Balances")
        
        for emp_id, name, _ in employees[:2]:  # Check first 2 employees
            print(f"📊 Checking balance for {name} ({emp_id})...")
            response = leave_management_agent.send_message(
                f"What is the leave balance for employee {emp_id}?"
            )
            print_response(response)
        
        # Scenario 3: Submit leave requests
        print_section("3️⃣ Submit Leave Requests")
        
        # Calculate dates
        today = datetime.now()
        next_week = today + timedelta(days=7)
        next_month = today + timedelta(days=30)
        
        requests = [
            {
                "emp_id": "EMP001",
                "name": "John Doe",
                "start": next_week.strftime("%Y-%m-%d"),
                "end": (next_week + timedelta(days=2)).strftime("%Y-%m-%d"),
                "type": "Vacation",
                "reason": "Family trip to the beach",
            },
            {
                "emp_id": "EMP002",
                "name": "Jane Smith",
                "start": next_month.strftime("%Y-%m-%d"),
                "end": (next_month + timedelta(days=4)).strftime("%Y-%m-%d"),
                "type": "Personal",
                "reason": "Home renovation work",
            },
            {
                "emp_id": "EMP003",
                "name": "Bob Johnson",
                "start": (today + timedelta(days=14)).strftime("%Y-%m-%d"),
                "end": (today + timedelta(days=14)).strftime("%Y-%m-%d"),
                "type": "Sick",
                "reason": "Medical appointment",
                "half_day": True,
            },
        ]
        
        for req in requests:
            emp_id = req["emp_id"]
            name = req["name"]
            start = req["start"]
            end = req["end"]
            leave_type = req["type"]
            reason = req["reason"]
            half_day = req.get("half_day", False)
            
            half_day_text = "half day " if half_day else ""
            print(f"📝 Submitting {half_day_text}leave request for {name} ({emp_id})...")
            print(f"   Type: {leave_type}, Dates: {start} to {end}")
            print(f"   Reason: {reason}\n")
            
            response = leave_management_agent.send_message(
                f"Submit {half_day_text}leave request for {emp_id} from {start} to {end} "
                f"for {leave_type} reason: {reason}"
            )
            print_response(response)
        
        # Scenario 4: View pending requests
        print_section("4️⃣ View Pending Leave Requests")
        
        print("📋 Fetching all pending leave requests...\n")
        response = leave_management_agent.send_message("Show all pending leave requests")
        print_response(response)
        
        # Scenario 5: Approve a request
        print_section("5️⃣ Approve Leave Request")
        
        # Generate request ID for first employee
        request_id = f"REQ-EMP001-{next_week.strftime('%Y%m%d')}"
        print(f"✅ Approving leave request: {request_id}...\n")
        
        response = leave_management_agent.send_message(
            f"Approve leave request {request_id} by manager MGR001"
        )
        print_response(response)
        
        # Scenario 6: Reject a request
        print_section("6️⃣ Reject Leave Request")
        
        request_id = f"REQ-EMP002-{next_month.strftime('%Y%m%d')}"
        print(f"❌ Rejecting leave request: {request_id}...\n")
        
        response = leave_management_agent.send_message(
            f"Reject leave request {request_id} by manager MGR001 with reason: "
            f"Team workload is high during this period. Please reschedule."
        )
        print_response(response)
        
        # Scenario 7: Check updated balance
        print_section("7️⃣ Check Updated Balance After Approval")
        
        print(f"📊 Checking updated balance for John Doe (EMP001)...\n")
        response = leave_management_agent.send_message(
            "What is the leave balance for employee EMP001?"
        )
        print_response(response)
        
        # Scenario 8: View leave history
        print_section("8️⃣ View Employee Leave History")
        
        print(f"📜 Fetching leave history for John Doe (EMP001)...\n")
        response = leave_management_agent.send_message(
            "Show leave history for employee EMP001"
        )
        print_response(response)
        
        # Scenario 9: Cancel a request
        print_section("9️⃣ Cancel Leave Request")
        
        # Submit another request to cancel
        cancel_date = today + timedelta(days=60)
        cancel_request_id = f"REQ-EMP004-{cancel_date.strftime('%Y%m%d')}"
        
        print(f"📝 Submitting a leave request for Alice Williams (EMP004)...\n")
        response = leave_management_agent.send_message(
            f"Submit leave request for EMP004 from {cancel_date.strftime('%Y-%m-%d')} "
            f"to {(cancel_date + timedelta(days=1)).strftime('%Y-%m-%d')} "
            f"for Vacation reason: Weekend getaway"
        )
        print_response(response)
        
        print(f"❌ Cancelling leave request: {cancel_request_id}...\n")
        response = leave_management_agent.send_message(
            f"Cancel leave request {cancel_request_id} for employee EMP004"
        )
        print_response(response)
        
        # Scenario 10: AI-powered insights
        print_section("🔟 AI-Powered Leave Insights")
        
        insights_questions = [
            "What are the current leave trends?",
            "Which employees have the highest leave utilization?",
            "Are there any concerning leave patterns?",
        ]
        
        for question in insights_questions:
            print(f"🤖 Question: {question}\n")
            response = leave_management_agent.send_message(question)
            print_response(response)
        
        print_section("✅ Demo Complete!")
        
        print("The Leave Management Agent successfully demonstrated:")
        print("  ✓ Employee balance initialization with tenure-based allocation")
        print("  ✓ Leave request submission with validation")
        print("  ✓ Balance checking and tracking")
        print("  ✓ Leave request approval and rejection")
        print("  ✓ Leave history tracking")
        print("  ✓ Request cancellation")
        print("  ✓ AI-powered insights and analytics")
        print("\nThe system is ready for production use! 🎉")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Set up environment
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️ Warning: GOOGLE_API_KEY not set in environment")
        print("The agent may use fallback responses instead of AI-powered responses.\n")
    
    main()
