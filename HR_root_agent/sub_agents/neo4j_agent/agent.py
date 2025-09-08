"""
Neo4j Agent for HR AI Assistant.

This agent provides graph database capabilities for the HR system using Neo4j.
"""

import os
from typing import Dict, List, Any, Optional, Union
import json
from neo4j import GraphDatabase

class Neo4jAgent:
    """Agent for managing Neo4j graph database operations."""
    
    def __init__(self, name: str = "Neo4j Graph Database Assistant"):
        self.name = name
        # Initialize connection params - these should be set from environment variables in production
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None
        
    def connect(self):
        """Establish connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            return True
        except Exception as e:
            print(f"Failed to connect to Neo4j: {e}")
            return False
            
    def close(self):
        """Close the Neo4j connection."""
        if self.driver:
            self.driver.close()
            
    def execute_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute a Cypher query and return the results."""
        if not self.driver:
            if not self.connect():
                return []
                
        try:
            with self.driver.session() as session:
                result = session.run(query, params or {})
                return [record.data() for record in result]
        except Exception as e:
            print(f"Query execution error: {e}")
            return []
            
    def create_employee_node(self, employee_data: Dict) -> Dict:
        """Create an employee node in the graph database."""
        query = """
        CREATE (e:Employee {
            id: $id,
            name: $name, 
            position: $position,
            department: $department,
            email: $email,
            hire_date: $hire_date
        })
        RETURN e
        """
        result = self.execute_query(query, employee_data)
        return result[0] if result else {}
        
    def create_relationship(self, from_id: str, to_id: str, relationship_type: str, properties: Dict = None) -> bool:
        """Create a relationship between two nodes."""
        query = f"""
        MATCH (a), (b)
        WHERE a.id = $from_id AND b.id = $to_id
        CREATE (a)-[r:{relationship_type} $properties]->(b)
        RETURN r
        """
        params = {
            "from_id": from_id,
            "to_id": to_id,
            "properties": properties or {}
        }
        result = self.execute_query(query, params)
        return bool(result)
        
    def get_organizational_hierarchy(self, department: Optional[str] = None) -> List[Dict]:
        """Retrieve the organizational hierarchy, optionally filtered by department."""
        query = """
        MATCH (e:Employee)-[r:REPORTS_TO]->(m:Employee)
        WHERE $department IS NULL OR e.department = $department
        RETURN e.name as employee, e.position as position, m.name as manager, e.department as department
        """
        return self.execute_query(query, {"department": department})
        
    def find_employee_connections(self, employee_id: str, depth: int = 2) -> List[Dict]:
        """Find connections to an employee up to a certain depth."""
        query = """
        MATCH path = (e:Employee {id: $employee_id})-[*1..$depth]-(connected)
        RETURN path
        """
        return self.execute_query(query, {"employee_id": employee_id, "depth": depth})
        
    def run_graph_analytics(self, analytics_type: str) -> Dict[str, Any]:
        """Run various graph analytics on the HR data."""
        results = {}
        
        if analytics_type == "centrality":
            # Find most central employees in the organization
            query = """
            CALL gds.betweenness.stream('employees')
            YIELD nodeId, score
            MATCH (n) WHERE id(n) = nodeId
            RETURN n.name AS employee, n.position AS position, score AS centrality
            ORDER BY centrality DESC
            LIMIT 10
            """
            results["centrality"] = self.execute_query(query)
            
        elif analytics_type == "communities":
            # Detect communities/groups in the organization
            query = """
            CALL gds.louvain.stream('employees')
            YIELD nodeId, communityId
            MATCH (n) WHERE id(n) = nodeId
            RETURN n.name AS employee, n.department AS department, communityId
            ORDER BY communityId, department
            """
            results["communities"] = self.execute_query(query)
            
        return results

# Create an instance of the Neo4j Agent
neo4j_agent = Neo4jAgent()
