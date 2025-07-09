import logging
import allure
import time
from functools import wraps

class TestLogger:
    def __init__(self, name=__name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log_step(self, step_name):
        """Decorator to log test steps"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                self.logger.info(f"START STEP: {step_name}")
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    self.logger.info(f"END STEP: {step_name} (Duration: {duration:.2f}s)")
                    return result
                except Exception as e:
                    self.logger.error(f"STEP FAILED: {step_name} - {str(e)}")
                    raise
            
            return wrapper
        return decorator

    def attach_to_allure(self, message, level='INFO'):
        """Attach log messages to Allure"""
        with allure.step(f"LOG {level}: {message}"):
            pass
        getattr(self.logger, level.lower())(message)

# Create a global logger instance
logger = TestLogger().logger
step = TestLogger().log_step