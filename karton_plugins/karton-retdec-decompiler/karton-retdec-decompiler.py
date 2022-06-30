from karton.core import Karton, Task, Resource
import subprocess
import os

class Retdec(Karton):
    """
    Runs the `retdec` utility on incoming samples
    """

    identity = "karton.retdec"
    filters = [{"type": "sample", "stage": "recognized"}]

    def process(self, task: Task) -> None:
        # Get the incoming sample3
        sample_resource = task.get_resource("sample")
        sample_name = sample_resource.name + " retdec" 
        full_path = "/home/retdec/samples/exec/"+sample_resource.name
        c_file = full_path+ ".c"        
        # Log with self.log
        self.log.info(f"Hi {sample_resource.name}, let me analyse you!")
        os.mkdir("/home/retdec/samples/exec")

            # Download the resource to a temporary file
        sample_resource.download_to_file(full_path)
                # And run `retdec` on it
        retdec01 = subprocess.check_output(["/home/retdec/retdec-install/bin/retdec-decompiler",full_path])
        output = subprocess.check_output(["cat", c_file])
        
        #sample = self.current_task.get_resource(c_file)
        #sample.download_to_file("/home/retdec/samples/")

            # Send our results for further processing or reporting
        task = Task(
                {"type": "sample", "stage": "analyzed"},
                payload={"parent": sample_resource, "sample": Resource(sample_name, output)},
            )
        task.add_payload("tags", ["karton:retdec"])
        self.send_task(task)
        dir = '/home/retdec/samples/exec'
        for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))
        os.rmdir(dir)



if __name__ == "__main__":
    # Here comes the main loop
    Retdec().loop()
