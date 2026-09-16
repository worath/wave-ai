from pydantic import BaseModel, Field


class ProjectRequest(BaseModel):
    description: str = Field(
        ...,
        min_length=10,
        description="توضیحات پروژه از طرف مشتری"
    )