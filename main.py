from pipeline.pipeline_engine import PipelineEngine


prompt = """
Build a CRM for real estate agency with leads,
deals, properties and WhatsApp notifications
when deal closes.
"""


engine = PipelineEngine()

result = engine.run(prompt)

print(result)