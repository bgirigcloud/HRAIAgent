"""
PGVector DB Agent for HR AI Assistant.

This agent provides vector database capabilities for the HR system using PostgreSQL with pgvector extension.
"""

import os
from typing import Dict, List, Any, Optional, Union
import json
import numpy as np
import psycopg2
from psycopg2.extras import execute_values

class PGVectorDBAgent:
    """Agent for managing vector database operations with PostgreSQL and pgvector."""
    
    def __init__(self, name: str = "Vector Database Assistant"):
        self.name = name
        # Initialize connection params - these should be set from environment variables in production
        self.host = os.getenv("PGVECTOR_HOST", "localhost")
        self.port = os.getenv("PGVECTOR_PORT", "5432")
        self.database = os.getenv("PGVECTOR_DB", "hr_vector_db")
        self.user = os.getenv("PGVECTOR_USER", "postgres")
        self.password = os.getenv("PGVECTOR_PASSWORD", "postgres")
        self.conn = None
        
    def connect(self):
        """Establish connection to PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return True
        except Exception as e:
            print(f"Failed to connect to PostgreSQL: {e}")
            return False
            
    def close(self):
        """Close the PostgreSQL connection."""
        if self.conn:
            self.conn.close()
            
    def initialize_database(self):
        """Initialize the database with required extensions and tables."""
        if not self.conn and not self.connect():
            return False
            
        try:
            with self.conn.cursor() as cursor:
                # Enable pgvector extension
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # Create resume embeddings table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS resume_embeddings (
                    id SERIAL PRIMARY KEY,
                    candidate_id VARCHAR(100) NOT NULL,
                    candidate_name VARCHAR(255) NOT NULL,
                    resume_text TEXT NOT NULL,
                    embedding vector(1536) NOT NULL,
                    metadata JSONB
                );
                """)
                
                # Create job description embeddings table
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS jd_embeddings (
                    id SERIAL PRIMARY KEY,
                    job_id VARCHAR(100) NOT NULL,
                    job_title VARCHAR(255) NOT NULL,
                    jd_text TEXT NOT NULL,
                    embedding vector(1536) NOT NULL,
                    metadata JSONB
                );
                """)
                
                # Create index for faster similarity search
                cursor.execute("CREATE INDEX IF NOT EXISTS resume_embedding_idx ON resume_embeddings USING ivfflat (embedding vector_l2_ops);")
                cursor.execute("CREATE INDEX IF NOT EXISTS jd_embedding_idx ON jd_embeddings USING ivfflat (embedding vector_l2_ops);")
                
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Database initialization error: {e}")
            self.conn.rollback()
            return False
    
    def store_resume_embedding(self, candidate_id: str, candidate_name: str, resume_text: str, 
                              embedding: List[float], metadata: Dict = None) -> bool:
        """Store a resume text and its embedding vector."""
        if not self.conn and not self.connect():
            return False
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                INSERT INTO resume_embeddings (candidate_id, candidate_name, resume_text, embedding, metadata)
                VALUES (%s, %s, %s, %s, %s)
                """, (candidate_id, candidate_name, resume_text, embedding, json.dumps(metadata or {})))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error storing resume embedding: {e}")
            self.conn.rollback()
            return False
            
    def store_jd_embedding(self, job_id: str, job_title: str, jd_text: str, 
                          embedding: List[float], metadata: Dict = None) -> bool:
        """Store a job description text and its embedding vector."""
        if not self.conn and not self.connect():
            return False
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                INSERT INTO jd_embeddings (job_id, job_title, jd_text, embedding, metadata)
                VALUES (%s, %s, %s, %s, %s)
                """, (job_id, job_title, jd_text, embedding, json.dumps(metadata or {})))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error storing JD embedding: {e}")
            self.conn.rollback()
            return False
    
    def find_similar_resumes(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """Find resumes similar to the query embedding."""
        if not self.conn and not self.connect():
            return []
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                SELECT candidate_id, candidate_name, resume_text, 
                       1 - (embedding <=> %s) AS similarity,
                       metadata
                FROM resume_embeddings
                ORDER BY embedding <=> %s
                LIMIT %s
                """, (query_embedding, query_embedding, limit))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        "candidate_id": row[0],
                        "candidate_name": row[1],
                        "resume_text": row[2],
                        "similarity": row[3],
                        "metadata": row[4]
                    })
                return results
        except Exception as e:
            print(f"Error finding similar resumes: {e}")
            return []
            
    def find_matching_jobs(self, resume_embedding: List[float], limit: int = 5) -> List[Dict]:
        """Find job descriptions that match a resume embedding."""
        if not self.conn and not self.connect():
            return []
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                SELECT job_id, job_title, jd_text, 
                       1 - (embedding <=> %s) AS similarity,
                       metadata
                FROM jd_embeddings
                ORDER BY embedding <=> %s
                LIMIT %s
                """, (resume_embedding, resume_embedding, limit))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        "job_id": row[0],
                        "job_title": row[1],
                        "jd_text": row[2],
                        "similarity": row[3],
                        "metadata": row[4]
                    })
                return results
        except Exception as e:
            print(f"Error finding matching jobs: {e}")
            return []
            
    def find_matching_candidates(self, jd_embedding: List[float], limit: int = 10) -> List[Dict]:
        """Find resumes that match a job description embedding."""
        if not self.conn and not self.connect():
            return []
            
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                SELECT candidate_id, candidate_name, resume_text, 
                       1 - (embedding <=> %s) AS similarity,
                       metadata
                FROM resume_embeddings
                ORDER BY embedding <=> %s
                LIMIT %s
                """, (jd_embedding, jd_embedding, limit))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        "candidate_id": row[0],
                        "candidate_name": row[1],
                        "resume_text": row[2],
                        "similarity": row[3],
                        "metadata": row[4]
                    })
                return results
        except Exception as e:
            print(f"Error finding matching candidates: {e}")
            return []

# Create an instance of the PGVector DB Agent
pgvector_db_agent = PGVectorDBAgent()
