class LLMConfig(BaseModel):
    client: Literal["openai", "azure_openai", "anthropic", "vllm", "litellm"]
    model: Optional[str] = None
    max_tokens: int = Field(default=400)
    temperature: float = 0
    response_format: Literal["json_beg", "text","json_object","structured_output","tool"] = "text"
    use_cache: bool = True

    @model_validator(mode="after")
    def validate_response_format(self) -> Self:
        if self.response_format == "json_object" and self.client in ["vllm", "litellm","anthropic"]:
            raise ValueError(f"{self.client} does not support json_object response format")
        elif self.response_format == "structured_output" and self.client == "anthropic":
            raise ValueError(f"Anthropic does not support structured_output response format use json_beg or tool instead")
        return self
    
class Persona(BaseModel):
    name: str
    role: str
    persona: str
    objectives: List[str]