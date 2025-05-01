def build_prompt(user_query, model_metadata):
    prompt = f"PROJECT DESCRIPTION:\n{user_query}\n\n"
    prompt += "CANDIDATE MODELS:\n"
    for m in model_metadata:
        prompt += (
            f"- Model: {m['model']}\n"
            f"  Task: {m['model_task']}\n"
            f"  Framework: {m['framework_library']}\n"
            f"  Overall Score: {m['overall_score']}\n"
            f"  License: {m['license']}\n"
            f"  Hardware: {m['hardware_accelerators']}\n"
            f"  Documentation: {m['detailed_documentation']}\n\n"
        )
    prompt += "Given this project description and model candidates, recommend the BEST model(s) and justify your choice."
    return prompt
