from karton.core import Karton, Task, Resource
import subprocess


class PEParser(Karton):
    """
    Runs the `PEParser` utility on incoming samples
    """

    identity = "karton.PEParser"
    filters = [{"type": "sample", "stage": "recognized"}]

    def process(self, task: Task) -> None:
        # Get the incoming sample
        sample_resource = task.get_resource("sample")
        sample_name = sample_resource.name + " PE_Parser"

        # Log with self.log
        self.log.info(f"Hi {sample_resource.name}, let me parse you!")

        # Download the resource to a temporary file
        with sample_resource.download_temporary_file() as sample_file:
            # And run `PEparser` on it
            PE_data = subprocess.check_output(["python3", "PEParser.py", sample_file.name])

        # Send our results for further processing or reporting
        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={"parent": sample_resource, "sample": Resource(sample_name, PE_data)},
        )
        task.add_payload("tags", ["karton:PE_Parser"])
        self.send_task(task)


if __name__ == "__main__":
    # Here comes the main loop
    PEParser().loop()
