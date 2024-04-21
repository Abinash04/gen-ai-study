from __future__ import annotations

from typing import TYPE_CHECKING

from llama_index.core import PromptTemplate
from llama_index.core.evaluation import FaithfulnessEvaluator
from llama_index.llms.ollama import Ollama

from app.log import get_logger

if TYPE_CHECKING:
    from llama_index.core.base.llms.types import CompletionResponse
    from llama_index.core.base.response.schema import RESPONSE_TYPE

__all__ = ["evaluate"]
logger = get_logger("evaluate")


def evaluate(response: RESPONSE_TYPE) -> CompletionResponse | None:
    logger.info("Starting..")

    llama = Ollama(
        base_url="http://localhost:11434",
        model="llama2",
        request_timeout=300,
    )

    # TASK: Given the answer generated by the LLM in the previous step, write an evaluation prompt to have the LLM check if the answer
    # appropriately answered the question.
    # - If the answer sufficiently answers the question have the LLM respond with "Yes" and if not then "No".

    template = ""
    prompt = PromptTemplate(template)

    evaluator = FaithfulnessEvaluator(llm=llama, eval_template=prompt)

    for source_node in response.source_nodes:
        eval_result = evaluator.evaluate(
            response=str(response), contexts=[source_node.get_content()]
        )        
        result = eval_result.passing
        return llama.complete(f"If the value of {result} is True then return only one word either Yes or No.")
        

    
