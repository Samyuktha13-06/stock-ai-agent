from main import run_agent

try:
    run_agent()
except Exception as e:
    import traceback
    traceback.print_exc()
