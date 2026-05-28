from pydantic import BaseModel
from typing import List, Optional


class PageSchema(BaseModel):
    name: str
    route: str
    layout: str
    boundEntity: str
    components: List[str]


class APIEndpoint(BaseModel):
    path: str
    method: str
    handler: str
    boundEntity: str
    authRequired: bool
    rateLimit: bool


class Permission(BaseModel):
    entity: str
    read: bool
    write: bool
    delete: bool


class RoleSchema(BaseModel):
    role: str
    permissions: List[Permission]


class IntegrationHook(BaseModel):
    integration: str
    trigger: str
    action: str


class WorkflowTrigger(BaseModel):
    entity: str
    event: str
    condition: Optional[str] = None


class WorkflowStub(BaseModel):
    name: str
    trigger: WorkflowTrigger
    integration: str
    action: str
    payload: dict


class AppSpec(BaseModel):
    pages: List[PageSchema]
    apiEndpoints: List[APIEndpoint]
    authRules: List[RoleSchema]
    integrationHooks: List[IntegrationHook]
    workflowStubs: List[WorkflowStub]