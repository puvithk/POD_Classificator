import sys
import json
from src.pipeline.pipeline import PODClassificationPipeline


def main():
    img = sys.argv[1] if len(sys.argv) > 1 else "test.jpg"
    prompt = sys.argv[2] if len(sys.argv) > 2 else "prompts/pod_extraction_prompt.txt"
    report = PODClassificationPipeline().run(img, prompt)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
