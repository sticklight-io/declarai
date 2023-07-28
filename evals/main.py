from evals.extraction import (
    run_single_value_extraction_eval,
    run_multi_value_extraction_eval,
    run_multi_value_multi_type_extraction_eval,
)
from evals.generation import (
    run_unstructured_shortform_generation,
    run_unstructured_longform_generation,
)

from evals.providers.openai import openai_models


if __name__ == "__main__":
    print("Running Evals:")
    # print("Extraction:")
    # run_single_value_extraction_eval(openai_models)
    # run_multi_value_extraction_eval(openai_models)
    # run_multi_value_multi_type_extraction_eval(openai_models)
    # run_unstructured_shortform_generation(openai_models)
    # run_unstructured_longform_generation(openai_models)
