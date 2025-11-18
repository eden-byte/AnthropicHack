"""
Base Agent class for the multi-agent system
"""
from anthropic import Anthropic
import os
from typing import Dict, Any, List
import json

class BaseAgent:
    def __init__(self, name: str, role: str, api_key: str = None):
        self.name = name
        self.role = role
        self.client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.conversation_history = []
        
    def think(self, prompt: str, system_prompt: str = None) -> str:
        """
        Core thinking method using Claude
        """
        messages = [{"role": "user", "content": prompt}]
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt or f"You are {self.name}, a {self.role}.",
            messages=messages
        )
        
        return response.content[0].text
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task - to be overridden by specific agents
        """
        raise NotImplementedError("Each agent must implement execute()")
    
    def log(self, message: str):
        """Log agent activity"""
        print(f"[{self.name}] {message}")