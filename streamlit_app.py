from src.ui import HealthcareUI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    app = HealthcareUI()
    app.run()