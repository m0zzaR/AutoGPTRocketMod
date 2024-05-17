import json
import pprint
from forge.actions import ActionRegister
from .sdk import PromptEngine
from forge.sdk import (
    Agent,
    AgentDB,
    ForgeLogger,
    Step,
    StepRequestBody,
    Task,
    TaskRequestBody,
    Workspace,
)
from forge.utils import chat_completion_request  # Assuming this is a utility function for making the LLM request

LOG = ForgeLogger(__name__)

class ForgeAgent(Agent):
    def __init__(self, database: AgentDB, workspace: Workspace):
        super().__init__(database, workspace)
        self.prompt_engine = PromptEngine("gpt-3.5-turbo")
        self.abilities = ActionRegister(self)

    async def create_task(self, task_request: TaskRequestBody) -> Task:
        task = await super().create_task(task_request)
        LOG.info(f"📦 Task created: {task.task_id} input: {task.input[:40]}{'...' if len(task.input) > 40 else ''}")
        return task

    async def execute_step(self, task_id: str, step_request: StepRequestBody) -> Step:
        try:
            task = await self.db.get_task(task_id)
            if not task:
                LOG.error(f"Task {task_id} not found.")
                return None

            # Load prompts for the task
            system_prompt = self.prompt_engine.load_prompt("system-format")
            task_kwargs = {
                "task": task.input,
                "abilities": self.abilities.list_abilities_for_prompt(),
            }
            task_prompt = self.prompt_engine.load_prompt("task-step", **task_kwargs)

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task_prompt}
            ]

            # Define parameters for the LLM completion request
            chat_completion_kwargs = {
                "messages": messages,
                "model": "gpt-3.5-turbo",
            }

            # Make the LLM completion request and handle the response
            chat_response = await chat_completion_request(**chat_completion_kwargs)
            response_content = chat_response.choices[0].message.content
            LOG.info(f"LLM response: {response_content}")

            try:
                answer = json.loads(response_content)
            except json.JSONDecodeError as e:
                LOG.error(f"Error decoding JSON response: {response_content}")
                raise e

            LOG.info(f"Answer: {pprint.pformat(answer)}")

            # Add a new step to the database
            step = await self.db.create_step(task_id=task_id, input=step_request, is_last=True)
            return step

        except json.JSONDecodeError as e:
            LOG.error(f"JSON decode error: {e}")
        except Exception as e:
            LOG.error(f"Error executing step: {e}")

        return None
