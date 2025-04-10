from karton.core import Karton, Task, Resource
from peparser_lib import parse_pe_file
import json


class PEParser(Karton):
    identity = "karton.peparser"
    filters = [{"type": "sample", "stage": "recognized"}]

    def process(self, task: Task) -> None:
        sample_resource = task.get_resource("sample")
        sample_name = sample_resource.name + " PE_Parser"

        self.log.info(f"Hi {sample_resource.name}, let me parse you!")

        with sample_resource.download_temporary_file() as sample_file:
            result = parse_pe_file(sample_file.name)

        if "error" in result:
            self.log.warning(f"{sample_resource.name} is not a valid PE")
            return

        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={
                "parent": sample_resource,
                "metadata": result
            }
        )
        task.add_payload("tags", ["karton:peparser"])
        self.send_task(task)


if __name__ == "__main__":
    PEParser().loop()
