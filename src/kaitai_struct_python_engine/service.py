from flask import Flask, json, request
from flask_cors import CORS
from . import *

api = Flask(__name__)
CORS(api)
eng = Engine()


@api.route('/struct')
def struct_index():
    return list(eng.parsers.keys())

@api.route('/struct/load_local', methods = ['POST'])
def struct_load_local():
    local_file = request.args.get("local_file")
    try:
        eng.compile_and_import_local_files([local_file])
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "error": str(e)}, 500

@api.route('/engine/load_local', methods = ['POST'])
def engine_load():
    try:
        eng.load_and_parse_local_file(request.args.get("local_file"), request.args.get("struct"))
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "error": str(e)}, 500

@api.route('/engine/explore')
def engine_explore():
    try:
        if "path" in request.args:
            path = request.args.get("path")
            if path == "":
                path = []
            else:
                path = path.split(".")
        else:
            path = []

        if "depth" in request.args:
            recurse_levels = int(request.args.get("depth"))
        else:
            recurse_levels = 1

        print("engine_explore => path:", repr(path))
        return eng.explore(path, recurse_levels)
    except Exception as e:
        return {"status": "error", "error": str(e)}, 500
