from typing import List, Optional
from pydantic import BaseModel, Field


class Resource(BaseModel):
    title: str = Field(..., description="Title of the learning resource")

    url: str = Field(..., description="URL of the learning resource")

    type: str = Field(
        ...,
        description="Type of resource such as Documentation, Course, Video, Book or GitHub Repository",
    )


class ResourceList(BaseModel):
    resources: List[Resource] = Field(
        ..., description="List of learning resources found"
    )
