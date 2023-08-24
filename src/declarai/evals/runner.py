from time import time
from typing import Any, Callable, Dict

from rich.progress import Progress
from rich.table import Table

from declarai import Declarai


def evaluate_single_task_scenario(
    scenario_name: str,
    scenario: Callable,
    scenario_kwargs: Dict[str, Any],
    models: Dict[str, Declarai],
    table: Table,
):
    with Progress() as progress:
        evaluator = progress.add_task(f"[red]{scenario_name}...", total=len(models))

        for model, declarai in models.items():
            try:
                initialized_scenario = declarai.task(scenario)

                start_time = time()
                res = initialized_scenario(**scenario_kwargs)
                total_time = time() - start_time
                progress.update(evaluator, advance=1)

                try:
                    input_tokens = str(initialized_scenario.llm_response.prompt_tokens)
                    output_tokens = str(
                        initialized_scenario.llm_response.completion_tokens
                    )
                except:  # noqa
                    input_tokens = "error"
                    output_tokens = "error"

                table.add_row(
                    declarai.llm_config.provider,
                    declarai.llm_config.model,
                    declarai.llm_config.version or "latest",
                    scenario_name,
                    f"{round(total_time, 3)}s",
                    input_tokens,
                    output_tokens,
                    str(res),
                )
            except Exception as e:
                print(f"Error: {e}")
                table.add_row(
                    declarai.llm_config.provider,
                    declarai.llm_config.model,
                    declarai.llm_config.version or "latest",
                    scenario_name,
                    "error",
                    "error",
                    "error",
                    repr(e),
                )


def evaluate_sequence_task_scenario(
    scenario_name: str,
    scenario: Callable,
    scenario_kwargs: Dict[str, Any],
    models: Dict[str, Declarai],
    table: Table,
):
    with Progress() as progress:
        evaluator = progress.add_task(f"[red]{scenario_name}...", total=len(models))

        for model, declarai in models.items():
            try:
                initialized_scenario = scenario(declarai, **scenario_kwargs)
                start_time = time()
                res = initialized_scenario()
                total_time = time() - start_time
                progress.update(evaluator, advance=1)

                try:
                    input_tokens = str(initialized_scenario.llm_response.prompt_tokens)
                    output_tokens = str(
                        initialized_scenario.llm_response.completion_tokens
                    )
                except:  # noqa
                    input_tokens = "error"
                    output_tokens = "error"

                table.add_row(
                    declarai.llm_config.provider,
                    declarai.llm_config.model,
                    declarai.llm_config.version or "latest",
                    scenario_name,
                    f"{round(total_time, 3)}s",
                    input_tokens,
                    output_tokens,
                    str(res),
                )
            except Exception as e:
                print(f"Error: {e}")
                table.add_row(
                    declarai.llm_config.provider,
                    declarai.llm_config.model,
                    declarai.llm_config.version or "latest",
                    scenario_name,
                    "error",
                    "error",
                    "error",
                    repr(e),
                )
