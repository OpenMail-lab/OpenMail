import logging
import os
import sys
import traceback
from datetime import datetime

class ErrorCollector:
    def __init__(self):
        # Setup simple console logging
        self.logger = logging.getLogger('OpenMail')
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler with formatting
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def log_error(self, error, context=""):
        """Log error to console"""
        error_msg = f"❌ {context} Error: {str(error)}"
        self.logger.error(error_msg)
        print(traceback.format_exc())  # Print stack trace to console
        return error_msg
        
    def log_info(self, message):
        """Log info to console"""
        self.logger.info(f"ℹ️ {message}")
        
    def log_success(self, message):
        """Log success to console"""
        self.logger.info(f"✅ {message}")

# Create a singleton instance
error_collector = ErrorCollector()
