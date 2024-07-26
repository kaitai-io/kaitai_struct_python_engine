import pytest
from kaitai_struct_python_engine import Engine


@pytest.fixture
def elf_engine() -> Engine:
    eng = Engine()
    eng.compile_and_import_local_files(["tests/ksy/elf.ksy"])
    eng.load_and_parse_local_file("tests/input/write", "elf")
    return eng


class TestEngineLoading(object):
    def setup_method(self):
        self.engine = Engine()

    def test_engine_happy(self):
        self.engine.compile_and_import_local_files(["tests/ksy/hello_world.ksy"])
        self.engine.load_and_parse_local_file("tests/input/hello_world.bin", "hello_world")

        assert self.engine.tree is not None
        assert self.engine.tree.hello == 0x31

        assert self.engine.explore([]) == {
            "io": 0,
            "path": [],
            "seq": [
                {"id": "hello", "start": 0, "end": 1, "value": 0x31},
            ],
            "type": "HelloWorld",
        }
        assert self.engine.explore(["hello"]) == 0x31

    def test_engine_all_at_once(self):
        self.engine.compile_and_import_local_files(["tests/ksy/all_at_once.ksy"])
        self.engine.load_and_parse_local_file("tests/input/hello_world.bin", "all_at_once")

        assert self.engine.explore([]) == {
            "io": 0,
            "path": [],
            "seq": [
                {"id": "hello", "start": 0, "end": 1, "value": 0x31},
            ],
            "type": "AllAtOnce",
        }


class TestEngineExploration(object):
    def test_explore_top(self, elf_engine):
        assert elf_engine.explore([], 0) == {
            'io': 0,
            'path': [],
            'seq': [
                {
                    'end': 4,
                    'id': 'magic',
                    'start': 0,
                },
                {
                    'end': 5,
                    'id': 'bits',
                    'start': 4,
                },
                {
                    'end': 6,
                    'id': 'endian',
                    'start': 5,
                },
                {
                    'end': 7,
                    'id': 'ei_version',
                    'start': 6,
                },
                {
                    'end': 8,
                    'id': 'abi',
                    'start': 7,
                },
                {
                    'end': 9,
                    'id': 'abi_version',
                    'start': 8,
                },
                {
                    'end': 16,
                    'id': 'pad',
                    'start': 9,
                },
                {
                    'end': 64,
                    'id': 'header',
                    'start': 16,
                },
            ],
            'type': 'Elf',
        }
