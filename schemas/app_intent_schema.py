from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class AppType(str, Enum):
    crm = "crm"
    project_management = "project_management"
    ecommerce = "ecommerce"
    hr_tool = "hr_tool"
    inventory = "inventory"
    content_platform = "content_platform"
    analytics = "analytics"
    custom = "custom"


class AppIntent(BaseModel):
    appName: str
    appType: AppType

    features: List[str]
    entities: List[str]

    integrations_requested: List[str]
    assumptions: List[str]

    clarification_required: bool = False
    clarification_question: Optional[str] = None