from pipeline.pipeline_engine import PipelineEngine


prompt = """
Project tracker. Projects, milestones, tasks. Sync tasks to Jira. Update a Google Sheet with weekly progress.
"""


engine = PipelineEngine()

result = engine.run(prompt)

print(result)