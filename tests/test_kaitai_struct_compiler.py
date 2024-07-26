import pytest
from kaitai_struct_python_engine import *


class TestKaitaiStructCompiler(object):
    def setup_method(self):
        self.compiler = KaitaiStructCompiler()

    def test_compile_happy(self):
        self.compiler.compile_ksy_local_files(["tests/ksy/hello_world.ksy"])

    def test_compile_not_found(self):
        with pytest.raises(CompilerException):
            self.compiler.compile_ksy_local_files(["tests/ksy/not_found.ksy"])

    def test_compile_and_import(self):
        parsers = self.compiler.compile_and_import_local_files(["tests/ksy/hello_world.ksy"])
        assert "hello_world" in parsers
        assert getattr(parsers["hello_world"], "_read") is not None
