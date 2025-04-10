from karton.core import Karton, Task, Resource
import subprocess
import os


class Floss(Karton):
    """
    Runs the `flare-floss` utility on incoming samples, supporting PE and shellcode (sc32/sc64)
    """

    identity = "karton.flare-floss"
    filters = [{"type": "sample", "stage": "recognized"}]

    def detect_architecture(self, file_path: str) -> str:
        """
        Naive architecture detection based on file size or hint from filename.
        Modify this as needed to use metadata or external hints.
        """
        with open(file_path, "rb") as f:
            data = f.read(0x1000)

        if b"\x48\x89\xe5" in data or b"\x55\x48\x89\xe5" in data:
            return "sc64"  # Common function prologue in 64-bit shellcode
        elif b"\x55\x89\xe5" in data:
            return "sc32"  # 32-bit x86 prologue
        else:
            return "sc32"  # Default fallback

    def process(self, task: Task) -> None:
        sample_resource = task.get_resource("sample")
        sample_name = sample_resource.name + " floss"

        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")

        with sample_resource.download_temporary_file() as sample_file:
            file_path = sample_file.name

            # Try running normally first
            try:
                floss_output = subprocess.check_output(
                    ["/usr/bin/floss", file_path], stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError as e:
                self.log.warning("Standard FLOSS analysis failed, trying shellcode mode...")

                arch = self.detect_architecture(file_path)
                self.log.info(f"Detected architecture: {arch}")

                floss_output = subprocess.check_output(
                    ["/usr/bin/floss", "-f", arch, file_path], stderr=subprocess.STDOUT
                )

        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={"parent": sample_resource, "sample": Resource(sample_name, floss_output)},
        )
        task.add_payload("tags", ["karton:floss"])
        self.send_task(task)


if __name__ == "__main__":
    Floss().loop()
