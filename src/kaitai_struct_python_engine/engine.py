from typing import Any
from kaitaistruct import KaitaiStream, KaitaiStruct
from . import *


class EngineError(Exception):
    pass


class EngineNavigationError(EngineError):
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)


class Engine(object):
    def __init__(self):
        self.compiler = KaitaiStructCompiler()
        self.parsers = {}
        self.tree = None

        self.stream_id_by_obj = {}
        self.stream_obj_by_id = {}
        self.stream_max_id = -1

    def compile_and_import_local_files(self, files: list[str]):
        add_parsers = self.compiler.compile_and_import_local_files(files)
        self.parsers.update(add_parsers)

    def load_and_parse_local_file(self, filepath: str, parser_name: str) -> None:
        if parser_name not in self.parsers:
            raise ValueError(f"Parser '{parser_name}' not found in modules")

        parser = self.parsers[parser_name]

        self.tree = parser.from_file(filepath)
        self.tree._read()
        self.track_stream(self.tree._io)

    def explore(self, path: list[str], recurse_levels: int = 1) -> any:
        obj = self.traverse_to_object(path)
        return self.explore_object(obj, path, recurse_levels)

    def explore_object(self, obj: any, path: list[str], recurse_levels: int = 1) -> any:
        res = {
            "path": path,
        }

        if isinstance(obj, KaitaiStruct):
            res["type"] = obj.__class__.__name__
            res["io"] = self.track_stream(obj._io)

            # Enumerate seq attributes
            res["seq"] = []
            for name in obj.__class__.SEQ_FIELDS:
                field = {
                    "id": name,
                    "start": obj._debug[name]["start"],
                    "end": obj._debug[name]["end"],
                }

                self.explore_value(obj, path, name, field, recurse_levels)

                res["seq"].append(field)

            if not res["seq"]:
                del res["seq"]

            # Enumerate properties
            res["instances"] = {}
            for name, value in obj.__class__.__dict__.items():
                if isinstance(value, property):
                    field = {}

                    if recurse_levels > 0:
                        value = getattr(obj, name)
                        field["value"] = self.explore_object(value, path + [name], recurse_levels - 1)

                    res["instances"][name] = field

            if not res["instances"]:
                del res["instances"]

            return res

        elif isinstance(obj, list):
            res["type"] = "array"
            res["length"] = len(obj)

            if recurse_levels > 0:
                res["items"] = []
                for i, item in enumerate(obj):
                    res["items"].append(self.explore_object(item, path + [str(i)], recurse_levels - 1))

            return res
        elif isinstance(obj, bytes):
            return None
        else:
            return obj

    def traverse_to_object(self, path: list[str]) -> any:
        if self.tree is None:
            raise ValueError("No tree to explore")

        obj = self.tree
        for p in path:
            if isinstance(obj, KaitaiStruct):
                obj = getattr(obj, p)
            elif isinstance(obj, list):
                p_int = int(p)
                obj = obj[p_int]
            else:
                raise ValueError(f"Cannot traverse further: {obj}")

        return obj

    def explore_value(self, obj: any, path: list[str], field_name: str, result: dict, recurse_levels: int):
        if recurse_levels > 0:
            value = getattr(obj, field_name)
            if isinstance(value, bytes):
                # do nothing, explorer will be able to see raw bytes from the stream anyway,
                # and we don't want to send them over in JSON response
                pass
            else:
                result["value"] = self.explore_object(value, path + [field_name], recurse_levels - 1)

    def track_stream(self, stream: KaitaiStream) -> int:
        if stream in self.stream_id_by_obj:
            return self.stream_id_by_obj[stream]

        self.stream_max_id += 1
        self.stream_id_by_obj[stream] = self.stream_max_id
        self.stream_obj_by_id[self.stream_max_id] = stream

        return self.stream_max_id
