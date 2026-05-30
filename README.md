# OneAtlas Trial — AI AppSpec Generation Pipeline

A multi-stage AI generation pipeline that converts a natural language app description into a validated, machine-readable application specification called **AppSpec**.

The system focuses on structured output generation, validation, repairability, provider routing, integration awareness, real-time progress tracking, and evaluation reliability.

---

## Core Pipeline

```text
User Prompt
→ AppIntent
→ DataSchema
→ AppSpec
→ Validation
→ Repair-ready Output
```

### Stage 1 — AppIntent

Extracts structured intent from a natural language prompt.

Includes:

* appName
* appType
* features
* entities
* integrations_requested
* assumptions
* clarification handling

### Stage 2 — DataSchema

Generates database-ready entity schemas.

Includes:

* entities
* table names
* fields
* relations
* tenantId on every entity

### Stage 3 — AppSpec

Generates the final machine-readable application specification.

Includes:

* pages
* API endpoints
* auth rules
* integration hooks
* workflow stubs

---

## Features

* Multi-stage AI generation pipeline
* Typed schema contracts using Pydantic
* Validation after each major stage
* Repair engine architecture
* Config-driven provider routing
* Integration registry
* Workflow stub generation
* FastAPI backend
* Job-based generation flow
* SSE progress streaming
* Evaluation logging
* 12-prompt evaluation suite

---

## Tech Stack

* Python
* FastAPI
* Pydantic
* LangChain
* Groq
* Gemini fallback support
* SSE streaming
* Uvicorn

---

## Project Structure

```text
agents/          AI generation agents
schemas/         Pydantic schema contracts
validators/      Validation logic
repair/          Repair strategies
pipeline/        Pipeline orchestration
gateway/         Provider routing
integrations/    Integration registry
runtime/         Job store, SSE, evaluation logging
api/             FastAPI routes
evaluation/      Test prompts and results
```

---

## API Endpoints

### Health Check

```http
GET /
```

### Start Generation

```http
POST /api/generate
```

Request:

```json
{
  "prompt": "Build a CRM for a real estate agency..."
}
```

Response:

```json
{
  "jobId": "uuid",
  "status": "completed"
}
```

### Get Job Status

```http
GET /api/generate/{job_id}
```

Returns:

* job status
* events
* generated result
* errors
* repair logs
* evaluation logs

### Stream Progress

```http
GET /api/generate/{job_id}/stream
```

SSE endpoint for real-time pipeline progress.

### Integration Registry

```http
GET /api/integrations
```

Returns supported integrations and actions.

### Manual Repair

```http
POST /api/generate/{job_id}/repair
```

Triggers a repair pass on a generated job.

---

## Supported Integrations

Implemented/stubbed integration registry:

* Slack
* Gmail
* Stripe
* WhatsApp
* Webhook
* Jira
* Google Sheets

Each integration includes:

* id
* display name
* auth type
* supported triggers
* supported actions
* input/output schema metadata

---

## Provider Routing

Model selection is config-driven through `config/routing.json`.

Different pipeline stages can route to different providers/models based on latency, cost, and capability needs.

Example stages:

* intent_extraction
* schema_generation
* appspec_generation
* repair

---

## Evaluation Results

The system was tested on 12 prompts:

* 7 standard product prompts
* 5 edge-case prompts

Final result:

```text
Total Prompts: 12
Passed: 12
Failed: 0
Success Rate: 100%
```

Major issue found during evaluation:

* Invalid relation target validation

Fix applied:

* Two-pass entity validation
* Integration registry expansion
* AppSpec integration normalization

---

## Running Locally

### 1. Clone Repository

```bash
git clone <repo-url>
cd oneatlas-trial
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Add Environment Variables

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 6. Run API Server

```bash
uvicorn api.main_api:app --reload
```

Open Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## Run Evaluation

```bash
python evaluation/run_evaluation.py
```

Evaluation outputs are saved inside:

```text
evaluation/results/
```

---

## Design Decisions

### Why Multi-Stage?

A single prompt is unreliable for complex software generation. This project separates generation into smaller typed stages so each output can be validated and repaired independently.

### Why AppSpec?

AppSpec acts as a machine-readable contract that a downstream code generator or template engine can consume.

### Why Validation?

LLMs can generate malformed or inconsistent structures. Validation ensures required fields, types, relations, integrations, and workflow references are correct before downstream usage.

### Why Repair Engine?

Instead of blindly retrying the whole pipeline, the repair engine is designed around targeted repair strategies:

* structural repair
* field repair
* consistency repair

---

## Current Limitations

* Integration actions are metadata stubs, not live OAuth/API calls.
* Repair endpoint is currently basic and can be improved with deeper stage-specific repair.
* Frontend is intentionally minimal because the core evaluation focus is backend reliability and AppSpec generation.
* Cost estimation can be expanded with more accurate token accounting.

---

## Future Improvements

* Next.js frontend dashboard
* More advanced repair strategies
* OpenRouter fallback
* Token-level cost tracking
* Persistent database-backed job store
* Production deployment with authentication
* More integration templates
* Runtime/code generation from AppSpec

---

## Author

Chetan Mittal
