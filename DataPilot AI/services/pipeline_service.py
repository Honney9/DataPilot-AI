# services/pipeline_service.py

from crews.dynamic_crew import DynamicCrew

class PipelineService:
    def __init__(self):
        self.crew = DynamicCrew()

    def run_pipeline(self, file_path: str):
        return self.crew.run(file_path)