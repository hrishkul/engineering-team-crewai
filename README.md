Engineering Team Automation with CrewAI

This project automates a basic software engineering workflow using CrewAI. Given a high-level requirement, a sequence of AI agents performs the following steps:

1. Generate a detailed module design.
2. Write the backend Python implementation.
3. Build a Gradio demo interface.
4. Create unit tests for the module.

Each step is handled by a specific AI agent with a dedicated role.

Project Structure

design_task: Creates a markdown design document with classes and methods.
 coding_task: Generates a Python module based on the design.

 frontend_task: Produces a Gradio app for demoing the backend.

 test_task: Writes unit tests for the backend code.

