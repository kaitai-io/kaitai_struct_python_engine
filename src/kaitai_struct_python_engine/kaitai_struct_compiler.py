import json
import os
import subprocess
import importlib.util
import sys

class CompilerException(Exception):
    def __init__(self, json_obj: dict) -> None:
        self.json_obj = json_obj

    @staticmethod
    def from_json(json_obj: dict):
        return CompilerException(json_obj)

    def to_json(self):
        return self.json_obj

class KaitaiStructCompiler:
    def __init__(self):
        self.output_dir = "/tmp/ksc-vis"

    def compile_and_import_local_files(self, ksy_files: list[str]):
        return self.import_local_files(self.compile_ksy_local_files(ksy_files))

    def compile_ksy_local_files(self, ksy_files: list[str]) -> dict:
        cmd = [
            'kaitai-struct-compiler',
            '-t', 'python',
            '--ksc-json-output',
            '--debug',
            '--outdir', self.output_dir,
        ]
        cmd.extend(ksy_files)
        print("cmd=", repr(cmd))

        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        json_output = json.loads(result.stdout)

        first_file = json_output[ksy_files[0]]
        if "errors" in first_file:
            raise CompilerException.from_json(first_file["errors"])
        else:
            return json_output

    def import_local_files(self, js: dict):
        # js = {
        #     "tests/ksy/hello_world.ksy": {
        #         "firstSpecName": "hello_world",
        #         "output": {
        #             "python": {
        #                 "hello_world": {
        #                     "topLevelName": "HelloWorld",
        #                     "files": [
        #                         {
        #                             "fileName": "hello_world.py"
        #                         }
        #                     ]
        #                 }
        #             }
        #         }
        #     }
        # }

        parsers = {}

        for input_file in js:
            py_outputs = js[input_file]["output"]["python"]
            for spec_name in py_outputs:
                top_level_name = py_outputs[spec_name]["topLevelName"]
                for file in py_outputs[spec_name]["files"]:
                    module_name = os.path.splitext(file["fileName"])[0]
                    module_path = os.path.join(self.output_dir, file["fileName"])

                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    parser_class = getattr(module, top_level_name)
                    parsers[spec_name] = parser_class

        return parsers
