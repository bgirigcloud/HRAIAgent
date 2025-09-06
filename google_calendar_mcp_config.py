"""
Google Calendar MCP Configuration
Handles Google Calendar API authentication and MCP server setup.
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarMCPConfig:
    """Configuration class for Google Calendar MCP integration."""
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """
        Initialize the Google Calendar MCP configuration.
        
        Args:
            credentials_file: Path to the OAuth2 credentials JSON file
            token_file: Path to store the access token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.service = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar API.
        
        Returns:
            True if authentication successful, False otherwise
        """
        # Load existing token if available
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"Credentials file '{self.credentials_file}' not found.")
                    print("Please download OAuth2 credentials from Google Cloud Console.")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())
        
        # Build the service
        self.service = build('calendar', 'v3', credentials=self.creds)
        return True
    
    def get_service(self):
        """Get the Google Calendar service object."""
        if not self.service:
            if not self.authenticate():
                raise Exception("Failed to authenticate with Google Calendar API")
        return self.service
    
    def test_connection(self) -> bool:
        """
        Test the connection to Google Calendar API.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            service = self.get_service()
            # Call the Calendar API to test connection
            calendars_result = service.calendarList().list().execute()
            calendars = calendars_result.get('items', [])
            print(f"Successfully connected to Google Calendar. Found {len(calendars)} calendars.")
            return True
        except Exception as e:
            print(f"Failed to connect to Google Calendar: {str(e)}")
            return False

# Global configuration instance
calendar_config = GoogleCalendarMCPConfig()
