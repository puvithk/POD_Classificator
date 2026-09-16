from src.pipeline.classification import PODClassification
from src.pipeline.extraction import PODExtraction



class PODClassificationPipeline:

    def __init__(self):
        self.classification_pipeline = PODClassification()
        self.extraction_pipeline = PODExtraction()

    def run(self ,image_path: str, prompt_path: str) -> dict:
        """Run the complete POD classification pipeline."""
        extraction = self.extraction_pipeline.extract_pod_info(image_path , prompt_path)
        classification = self.classification_pipeline.classify_pod(extraction)
        return {"classification": classification, "extraction": extraction}

        
if __name__ == "__main__":
    pipeline = PODClassificationPipeline()
    result = pipeline.run("test.jpg", "prompts/pod_extraction_prompt.txt")
    print(result)