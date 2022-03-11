from karton.core import Karton, Task, Resource
import subprocess


class Floss(Karton):
    """
    Runs the `flare-floss` utility on incoming samples
    """

    identity = "karton.flare-floss"
    filters = [{"type": "sample", "stage": "recognized"}]

    def process(self, task: Task) -> None:
        # Get the incoming sample
        sample_resource = task.get_resource("sample")
        sample_name = sample_resource.name + " floss" 

        # Log with self.log
        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")

        # Download the resource to a temporary file
        with sample_resource.download_temporary_file() as sample_file:
            # And run `floss` on it
            floss = subprocess.check_output(["floss", sample_file.name])

        # Send our results for further processing or reporting
        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={"parent": sample_resource, "sample": Resource(sample_name, floss)},
        )
        task.add_payload("tags", ["karton:floss"])
        self.send_task(task)


if __name__ == "__main__":
    # Here comes the main loop
    Floss().loop()
