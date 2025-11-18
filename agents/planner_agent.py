"""
Planner Agent - Breaks down the complex tasks into subtasks
"""

from agents.base_agent import BaseAgent
import json
from typing import Dict, Any, List

class PlannerAgent(BaseAgent):
    def __init__(self, api_key: str =  None):
        super().__init__(
            name="Planner",
            role="strategic task decomposition specalist",
            api_key=api_key
        )