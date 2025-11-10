"""
HR Policy Agent - Intelligent agent for handling employee policy queries
Allows HR to upload policy documents and employees to ask questions
"""
import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from google.adk.agents import Agent

class HRPolicyTools:
    """Tools for HR policy document management and query handling"""
    
    # In-memory storage for policy documents (in production, use a database)
    policy_documents = {}
    
    @staticmethod
    def upload_policy_document(document_name: str, content: str, category: str = "General") -> Dict[str, Any]:
        """
        Upload or update an HR policy document
        
        Args:
            document_name: Name of the policy document
            content: Text content of the policy
            category: Category of the policy (Leave, Benefits, Code of Conduct, etc.)
            
        Returns:
            Dictionary with upload status
        """
        try:
            policy_id = document_name.lower().replace(" ", "_")
            HRPolicyTools.policy_documents[policy_id] = {
                "name": document_name,
                "content": content,
                "category": category,
                "last_updated": "2025-11-10"
            }
            
            return {
                "success": True,
                "message": f"Policy document '{document_name}' uploaded successfully",
                "policy_id": policy_id,
                "category": category
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to upload policy: {str(e)}"
            }
    
    @staticmethod
    def list_all_policies() -> Dict[str, Any]:
        """
        List all available policy documents
        
        Returns:
            Dictionary containing all policy documents with their metadata
        """
        if not HRPolicyTools.policy_documents:
            return {
                "count": 0,
                "message": "No policy documents uploaded yet",
                "policies": []
            }
        
        policies_list = []
        for policy_id, policy_data in HRPolicyTools.policy_documents.items():
            policies_list.append({
                "id": policy_id,
                "name": policy_data["name"],
                "category": policy_data["category"],
                "last_updated": policy_data["last_updated"]
            })
        
        return {
            "count": len(policies_list),
            "policies": policies_list
        }
    
    @staticmethod
    def search_policy(query: str) -> Dict[str, Any]:
        """
        Search for relevant policy information based on employee query
        
        Args:
            query: Employee's question about policy
            
        Returns:
            Dictionary with relevant policy information
        """
        if not HRPolicyTools.policy_documents:
            return {
                "found": False,
                "message": "No policy documents available. Please ask HR to upload policies.",
                "relevant_policies": []
            }
        
        # Simple keyword matching (in production, use vector search/embeddings)
        query_lower = query.lower()
        relevant_policies = []
        
        for policy_id, policy_data in HRPolicyTools.policy_documents.items():
            content_lower = policy_data["content"].lower()
            name_lower = policy_data["name"].lower()
            
            # Check if query keywords appear in policy name or content
            query_words = query_lower.split()
            matches = sum(1 for word in query_words if word in content_lower or word in name_lower)
            
            if matches > 0:
                relevant_policies.append({
                    "policy_id": policy_id,
                    "name": policy_data["name"],
                    "category": policy_data["category"],
                    "content": policy_data["content"],
                    "relevance_score": matches
                })
        
        # Sort by relevance
        relevant_policies.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return {
            "found": len(relevant_policies) > 0,
            "query": query,
            "relevant_policies": relevant_policies[:3]  # Return top 3 most relevant
        }
    
    @staticmethod
    def get_policy_by_category(category: str) -> Dict[str, Any]:
        """
        Get all policies in a specific category
        
        Args:
            category: Category name (Leave, Benefits, Code of Conduct, etc.)
            
        Returns:
            Dictionary with policies in that category
        """
        matching_policies = []
        
        for policy_id, policy_data in HRPolicyTools.policy_documents.items():
            if policy_data["category"].lower() == category.lower():
                matching_policies.append({
                    "policy_id": policy_id,
                    "name": policy_data["name"],
                    "content": policy_data["content"],
                    "last_updated": policy_data["last_updated"]
                })
        
        return {
            "category": category,
            "count": len(matching_policies),
            "policies": matching_policies
        }
    
    @staticmethod
    def delete_policy(policy_id: str) -> Dict[str, Any]:
        """
        Delete a policy document
        
        Args:
            policy_id: ID of the policy to delete
            
        Returns:
            Dictionary with deletion status
        """
        try:
            if policy_id in HRPolicyTools.policy_documents:
                policy_name = HRPolicyTools.policy_documents[policy_id]["name"]
                del HRPolicyTools.policy_documents[policy_id]
                return {
                    "success": True,
                    "message": f"Policy '{policy_name}' deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Policy with ID '{policy_id}' not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete policy: {str(e)}"
            }


# HR Policy Agent
hr_policy_agent = Agent(
    name="hr_policy_agent",
    model="gemini-2.0-flash-exp",
    instruction="""You are an intelligent HR Policy Assistant that helps employees understand company policies.

Your primary responsibilities:
1. **Answer Employee Questions**: Provide clear, accurate answers about company policies based on uploaded documents
2. **Policy Search**: Search through policy documents to find relevant information
3. **Explain Policies**: Break down complex policies into easy-to-understand language
4. **Provide Examples**: Give practical examples when explaining policies
5. **Reference Sources**: Always cite which policy document you're referencing

**For HR Administrators:**
- Help them upload and manage policy documents
- Organize policies by category (Leave, Benefits, Code of Conduct, Remote Work, etc.)
- Track policy updates

**For Employees:**
- Answer questions about leave policies, benefits, work hours, remote work, etc.
- Explain eligibility criteria and procedures
- Provide step-by-step guidance for policy-related processes
- Clarify ambiguous policy language

**Communication Style:**
- Be friendly, professional, and empathetic
- Use simple language, avoid HR jargon
- Provide specific references to policy sections
- If information is not in the policy documents, clearly state that and suggest contacting HR directly

**Important Guidelines:**
- Always base answers on uploaded policy documents
- If a policy doesn't exist or information is unclear, admit it
- For sensitive matters (disciplinary, termination), advise consulting HR directly
- Keep employee data confidential
- Stay neutral and unbiased

When an employee asks a question:
1. Search relevant policy documents
2. Extract the most relevant information
3. Provide a clear, concise answer
4. Cite the policy document name
5. Offer to clarify further if needed""",
    description="An intelligent HR assistant that answers employee questions about company policies by searching through uploaded policy documents",
    tools=[],
)
