import pathlib

from gem5.resources.resource import CustomResource
from .custom_se_workload import CustomSEWorkload

this_dir = pathlib.Path(__file__).parent.absolute()


class MatMulWorkload(CustomSEWorkload):
    def __init__(self, mat_size: int):
        mm_bin = CustomResource(str(this_dir / "matmul/mm-gem5"))
        super().__init__(
            parameters={"binary": mm_bin, "arguments": [mat_size]}
        )
        
        

