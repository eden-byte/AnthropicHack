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

    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Break down a complex task into subtasks
        user_request = task.get("request", "")
        self.log(f"Planning for: {user_request}")

        system_prompt = """You are a strategic planner agent. Your job is to break down complex tasks into clear, actionable subtasks.
        For each task, output a JSON structure with:
        {
        "subtasks": [
            {
            "id": 1,
            "action": "specific action to take",
            "agent_type": "data_fetcher|data_analyzer|report_generator|web_scraper",
            "parameters": {"key": "value"},
            "dependencies": []
            }
        ],
        "execution_order": [1, 2, 3]
        }

        Available agent types:
        - data_fetcher: Gets data from files or APIs
        - data_analyzer: Performs analysis, statistics, ML
        - report_generator: Creates summaries, reports, visualizations
        - web_scraper: Extracts information from websites

        Be specific and practical."""

        prompt = f"""Break down this task into subtasks:
        Task: {user_request}
        Output ONLY valid JSON, no other text."""

        response = self.think(prompt, system_prompt)

        #extracting JSON from response
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                plan = json.loads(response[json_start:json_end])
            else:
                plan = json.loads(response)
        except json.JSONDecodeError:
            self.log("Failed to parse JSON, creating simple plan")
            plan = {
                "subtasks" : [
                    {
                        "id": 1,
                        "action": user_request,
                        "agent_type": "data_analyzer",
                        "parameters": {},
                        "dependencies": []
                    }
                ],
                "execution_order": [1]
            }

        self.log(f"Created plan with {len(plan.get('subtasks', []))} subtasks")
        return {
            "status": "success",
            "plan": plan
        }