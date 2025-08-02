from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew""" 

    agents_config='config/agents.yaml'
    tasks_config='config/tasks.yaml'

    @agent
    def lead_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_engineer'],
            verbose=True
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode='safe',
            max_execution_time=240,
            max_retries=5,
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer'],
            verbose=True,
        )

    @agent
    def testing_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['testing_engineer'],
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=240,
            max_retries=5
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'],
        )
    
    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task 
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task']
        )


    @crew
    def crew(self) -> Crew:
        """Creates the EngineeringTeam crew"""

        return Crew (
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
