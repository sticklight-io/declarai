from rich.console import Console
from rich.table import Table

from evals.extraction import (
    multi_value_extraction,
    multi_value_extraction_kwargs,
    multi_value_multi_type_extraction,
    multi_value_multi_type_extraction_kwargs,
    single_value_extraction,
    single_value_extraction_kwargs,
)
from evals.generation import (
    run_strict_complex_structured_generation,
    structured_open_ended,
    structured_open_ended_kwargs,
    unstructured_long_form,
    unstructured_long_form_kwargs,
    unstructured_short_form,
    unstructured_short_form_kwargs,
)
from evals.providers.openai import openai_models
from evals.runner import evaluate_scenario

if __name__ == "__main__":
    console = Console()

    table = Table(show_header=True, header_style="bold magenta", padding=(0, 1))
    table.add_column("Provider", width=15)
    table.add_column("Model", width=15)
    table.add_column("version", width=15)
    table.add_column("Scenario", width=40)
    table.add_column("runtime", width=10)
    table.add_column("output", width=100)
    # TODO: Add a performance

    console.print("[green]Running Evals:")
    console.print("[green]Running Extraction scenarios...")
    evaluate_scenario(
        "single_value_extraction",
        single_value_extraction,
        single_value_extraction_kwargs,
        openai_models,
        table,
    )
    evaluate_scenario(
        "multi_value_extraction",
        multi_value_extraction,
        multi_value_extraction_kwargs,
        openai_models,
        table,
    )
    evaluate_scenario(
        "multi_value_multi_type_extraction",
        multi_value_multi_type_extraction,
        multi_value_multi_type_extraction_kwargs,
        openai_models,
        table,
    )
    console.print("[green]Running Generation scenarios...")
    evaluate_scenario(
        "unstructured_short_form",
        unstructured_short_form,
        unstructured_short_form_kwargs,
        openai_models,
        table,
    )
    evaluate_scenario(
        "unstructured_long_form",
        unstructured_long_form,
        unstructured_long_form_kwargs,
        openai_models,
        table,
    )
    evaluate_scenario(
        "structured_open_ended",
        structured_open_ended,
        structured_open_ended_kwargs,
        openai_models,
        table,
    )
    # run_strict_complex_structured_generation(openai_models)
    # print("Logical tasks:")

    # print("Manipulation:")

    # print("Metadata significance:")
    console.print(table)
