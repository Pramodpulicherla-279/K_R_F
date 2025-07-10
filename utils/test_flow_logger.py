# utils/test_flow_logger.py
test_flow_log = []

def log_step(step_description):
    test_flow_log.append(step_description)

def get_logged_steps():
    return test_flow_log
