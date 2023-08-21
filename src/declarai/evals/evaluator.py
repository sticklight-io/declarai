from rich.console import Console
from rich.table import Table

from declarai.evals.extraction import (
    multi_value_extraction,
    multi_value_extraction_kwargs,
    multi_value_multi_type_extraction,
    multi_value_multi_type_extraction_kwargs,
    single_value_extraction,
    single_value_extraction_kwargs,
    single_value_multi_type_extraction,
    single_value_multi_type_extraction_kwargs,
)
from declarai.evals.generation import (
    structured_open_ended,
    structured_open_ended_kwargs,
    structured_strict_complex,
    structured_strict_complex_kwargs,
    unstructured_long_form,
    unstructured_long_form_kwargs,
    unstructured_short_form,
    unstructured_short_form_kwargs,
)
from declarai.evals.manipulation import data_manipulation, data_manipulation_kwargs
from declarai.evals.metadata_significance import (
    generate_a_poem_no_metadata,
    generate_a_poem_only_return_doc,
    generate_a_poem_only_return_magic,
    generate_a_poem_only_return_type,
    generate_a_poem_return_all,
    generate_a_poem_return_doc_return_magic,
    generate_a_poem_return_type_return_doc,
    generate_a_poem_return_type_return_magic,
    simple_task_significance_kwargs,
)
from declarai.evals.providers.openai import openai_models
from declarai.evals.runner import evaluate_single_task_scenario

if __name__ == "__main__":
    console = Console()

    table = Table(show_header=True, header_style="bold magenta", padding=(0, 1))
    table.add_column("Provider", width=15)
    table.add_column("Model", width=15)
    table.add_column("version", width=15)
    table.add_column("Scenario", width=40)
    table.add_column("runtime", width=10)
    table.add_column("input_tokens", width=10)
    table.add_column("output_tokens", width=10)
    table.add_column("output", width=100)

    console.print("[green]Running Evals:")
    console.print("[green]Running Extraction scenarios...")
    evaluate_single_task_scenario(
        "single_value_extraction",
        single_value_extraction,
        single_value_extraction_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "multi_value_extraction",
        multi_value_extraction,
        multi_value_extraction_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "multi_value_multi_type_extraction",
        multi_value_multi_type_extraction,
        multi_value_multi_type_extraction_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "single_value_multi_type_extraction",
        single_value_multi_type_extraction,
        single_value_multi_type_extraction_kwargs,
        openai_models,
        table,
    )

    console.print("[green]Running Generation scenarios...")
    evaluate_single_task_scenario(
        "unstructured_short_form",
        unstructured_short_form,
        unstructured_short_form_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "unstructured_long_form",
        unstructured_long_form,
        unstructured_long_form_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "structured_open_ended",
        structured_open_ended,
        structured_open_ended_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "structured_strict_complex",
        structured_strict_complex,
        structured_strict_complex_kwargs,
        openai_models,
        table,
    )

    # TODO:
    #  Chain of thought needs some love,
    #  currently only working on older model versions
    # console.print("[green]Running Logical scenarios...")
    # evaluate_sequence_task_scenario(
    #     "chain_of_thought",
    #     chain_of_thought,
    #     chain_of_thought_kwargs,
    #     openai_models,
    #     table,
    # )

    console.print("[green]Running Manipulation scenarios...")
    evaluate_single_task_scenario(
        "data_manipulation",
        data_manipulation,
        data_manipulation_kwargs,
        openai_models,
        table,
    )

    console.print("[green]Running Metadata-Significance scenarios...")
    evaluate_single_task_scenario(
        "generate_a_poem_no_metadata",
        generate_a_poem_no_metadata,
        simple_task_significance_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "generate_a_poem_only_return_type",
        generate_a_poem_only_return_type,
        simple_task_significance_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "generate_a_poem_only_return_doc",
        generate_a_poem_only_return_doc,
        simple_task_significance_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "generate_a_poem_only_return_magic",
        generate_a_poem_only_return_magic,
        simple_task_significance_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "generate_a_poem_return_type_return_doc",
        generate_a_poem_return_type_return_doc,
        simple_task_significance_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "generate_a_poem_return_type_return_magic",
        generate_a_poem_return_type_return_magic,
        simple_task_significance_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "generate_a_poem_return_doc_return_magic",
        generate_a_poem_return_doc_return_magic,
        simple_task_significance_kwargs,
        openai_models,
        table,
    )
    evaluate_single_task_scenario(
        "generate_a_poem_return_all",
        generate_a_poem_return_all,
        simple_task_significance_kwargs,
        openai_models,
        table,
    )
    console.print(table)
