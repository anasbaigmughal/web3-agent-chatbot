import logfire

def configure_logging():
    logfire.configure(send_to_logfire="if-token-present")
    logfire.instrument_openai_agents()