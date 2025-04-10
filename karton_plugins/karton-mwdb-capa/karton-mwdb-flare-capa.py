from karton.core import Karton, Task, Resource
import subprocess
import os


class Capa(Karton):
    """
    Runs the `flare-capa` utility on incoming samples (supports PE and shellcode)
    """

    identity = "karton.flare-capa"
    filters = [{"type": "sample", "stage": "recognized"}]

    def detect_architecture(self, file_path: str) -> str:
        """
        Naively detect architecture for shellcode. Defaults to sc32.
        """
        with open(file_path, "rb") as f:
            data = f.read(0x1000)

        if b"\x48\x89\xe5" in data or b"\x55\x48\x89\xe5" in data:
            return "sc64"
        elif b"\x55\x89\xe5" in data:
            return "sc32"
        return "sc32"

    def process(self, task: Task) -> None:
        sample_resource = task.get_resource("sample")
        sample_name = sample_resource.name + " Capability"

        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")

        with sample_resource.download_temporary_file() as sample_file:
            file_path = sample_file.name
            capa_output = b""

            try:
                capa_output = subprocess.check_output(
                    ["/app/venv/bin/capa", "-vv", file_path],
                    stderr=subprocess.STDOUT
                )
            except subprocess.CalledProcessError as e:
                self.log.warning("PE analysis failed, trying shellcode mode...")

                arch = self.detect_architecture(file_path)
                self.log.info(f"Detected shellcode architecture: {arch}")

                try:
                    capa_output = subprocess.check_output(
                        ["/app/venv/bin/capa", "-vv", "-f", arch, file_path],
                        stderr=subprocess.STDOUT
                    )
                except subprocess.CalledProcessError as e2:
                    self.log.error("Capa failed completely.")
                    self.log.error(e2.output.decode())
                    return

        task = Task(
            {"type": "sample", "stage": "analyzed"},
            payload={
                "parent": sample_resource,
                "sample": Resource(sample_name, capa_output),
            },
        )
        task.add_payload("tags", ["karton:capability"])
        self.send_task(task)


if __name__ == "__main__":
    Capa().loop()
