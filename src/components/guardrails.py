from agents import Runner, GuardrailFunctionOutput, input_guardrail
from ..models.data_models import PromptAnalysis
from ..config.settings import config
from ..components.guardrail_agents import prompt_guardrail_agent

@input_guardrail
async def prompt_guardrail(ctx, agent, input):
    """Analyzes user prompts for safety, validaty and scope defined."""
    try:
        result = await Runner.run(prompt_guardrail_agent, input=input, context=ctx.context, run_config=config)
        final_output = result.final_output_as(PromptAnalysis)

        if final_output.is_safe:
            print(f"🟢 Your prompt is safe. \n is_safe={final_output.is_safe} \n Reasoning: {final_output.reasoning}")
        else:
            print(f"🔴 Your prompt is not safe. \n is_safe={final_output.is_safe} \n Reasoning: {final_output.reasoning}")  

        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=not final_output.is_safe,
        )
    except Exception as e:
        print(f"🔴 Exception in guardrail: {str(e)}")
        return GuardrailFunctionOutput(
            output_info=PromptAnalysis(is_safe=False, reasoning=f"Error analyzing prompt: {str(e)}"),
            tripwire_triggered=True,
        )
