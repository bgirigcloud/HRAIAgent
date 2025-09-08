"""
RAG Agent for HR AI Assistant.

This agent provides Retrieval Augmented Generation capabilities for the HR system.
"""

import os
from typing import Dict, List, Any, Optional, Union
import json
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGAgent:
    """Agent for managing Retrieval Augmented Generation operations."""
    
    def __init__(self, name: str = "RAG Knowledge Assistant"):
        self.name = name
        # Initialize the embedding model
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Failed to load embedding model: {e}")
            self.model = None
        
        # Reference to PGVector DB agent for storing and retrieving embeddings
        self.vector_db_agent = None
        
    def set_vector_db_agent(self, agent):
        """Set the vector database agent for this RAG agent to use."""
        self.vector_db_agent = agent
            
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text."""
        if not self.model:
            print("Error: Embedding model not initialized")
            return []
            
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
            
    def index_document(self, doc_type: str, doc_id: str, doc_title: str, 
                      doc_text: str, metadata: Dict = None) -> bool:
        """Index a document in the vector database."""
        if not self.vector_db_agent:
            print("Error: Vector DB agent not set")
            return False
            
        embedding = self.generate_embedding(doc_text)
        if not embedding:
            return False
            
        if doc_type.lower() == "resume":
            return self.vector_db_agent.store_resume_embedding(
                doc_id, doc_title, doc_text, embedding, metadata
            )
        elif doc_type.lower() == "jd" or doc_type.lower() == "job_description":
            return self.vector_db_agent.store_jd_embedding(
                doc_id, doc_title, doc_text, embedding, metadata
            )
        else:
            print(f"Unsupported document type: {doc_type}")
            return False
            
    def retrieve_similar_documents(self, query: str, doc_type: str, limit: int = 5) -> List[Dict]:
        """Retrieve documents similar to the query."""
        if not self.vector_db_agent:
            print("Error: Vector DB agent not set")
            return []
            
        query_embedding = self.generate_embedding(query)
        if not query_embedding:
            return []
            
        if doc_type.lower() == "resume":
            return self.vector_db_agent.find_similar_resumes(query_embedding, limit)
        elif doc_type.lower() == "jd" or doc_type.lower() == "job_description":
            return self.vector_db_agent.find_matching_jobs(query_embedding, limit)
        else:
            print(f"Unsupported document type: {doc_type}")
            return []
            
    def match_resume_to_jobs(self, resume_text: str, limit: int = 5) -> List[Dict]:
        """Match a resume to available job descriptions."""
        if not self.vector_db_agent:
            print("Error: Vector DB agent not set")
            return []
            
        resume_embedding = self.generate_embedding(resume_text)
        if not resume_embedding:
            return []
            
        return self.vector_db_agent.find_matching_jobs(resume_embedding, limit)
            
    def match_job_to_candidates(self, job_description: str, limit: int = 10) -> List[Dict]:
        """Match a job description to available candidate resumes."""
        if not self.vector_db_agent:
            print("Error: Vector DB agent not set")
            return []
            
        jd_embedding = self.generate_embedding(job_description)
        if not jd_embedding:
            return []
            
        return self.vector_db_agent.find_matching_candidates(jd_embedding, limit)
    
    def augment_prompt(self, query: str, context_type: str = "both", limit: int = 3) -> str:
        """Augment a prompt with retrieved context."""
        augmented_prompt = f"Query: {query}\n\nRelevant Context:\n"
        
        # Retrieve similar documents
        if context_type.lower() in ["both", "resume"]:
            resumes = self.retrieve_similar_documents(query, "resume", limit)
            if resumes:
                augmented_prompt += "\nResume Context:\n"
                for i, resume in enumerate(resumes):
                    augmented_prompt += f"{i+1}. Candidate: {resume['candidate_name']}\n"
                    augmented_prompt += f"   Similarity: {resume['similarity']:.2f}\n"
                    # Extract a snippet for context
                    snippet = resume['resume_text'][:500] + "..." if len(resume['resume_text']) > 500 else resume['resume_text']
                    augmented_prompt += f"   Snippet: {snippet}\n\n"
        
        if context_type.lower() in ["both", "jd"]:
            jobs = self.retrieve_similar_documents(query, "jd", limit)
            if jobs:
                augmented_prompt += "\nJob Description Context:\n"
                for i, job in enumerate(jobs):
                    augmented_prompt += f"{i+1}. Job: {job['job_title']}\n"
                    augmented_prompt += f"   Similarity: {job['similarity']:.2f}\n"
                    # Extract a snippet for context
                    snippet = job['jd_text'][:500] + "..." if len(job['jd_text']) > 500 else job['jd_text']
                    augmented_prompt += f"   Snippet: {snippet}\n\n"
        
        augmented_prompt += f"\nBased on the above context, please answer the following query: {query}"
        return augmented_prompt

# Create an instance of the RAG Agent
rag_agent = RAGAgent()
