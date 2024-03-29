import os
import sys
import json


from gpm.__main__ import GPM_HOME


def files_by_pattern(directory, matchFunc):
    for path, dirs, files in os.walk(directory, followlinks=True):
        for f in filter(matchFunc, files):
            yield os.path.join(path, f)


def try_load(name, verbose, i, total):
    name = name.replace("/", ".").replace("\\", ".")[0:-3]
    if verbose:
        print("[" + str(i) + "/" + str(total) + "] Parsing: " + name)
    if name.endswith("__init__") or name.endswith("__main__") or name.endswith("buildNodespec") or name.endswith("debugger") or name.endswith("_Lib"):
        return False, None
    try:
        print(name)
        module = __import__(name, fromlist=["NODES"])
    except (ImportError, SyntaxError) as e:
        if verbose:
            print("Syntax or import error at: " + name)
            print(e)
        return False, (name, e)
    except:
        e = sys.exc_info()[0]
        print("Unknown Error")
        print(e)
        return False, (name, e)
    try:
        out = []
        for node in module.NODES.values():
            code = name.replace("gpm.pyGP.", "")
            node['code'] = f"{code}:{node['name']}"
            out.append(node)
        return True, out
    except (AttributeError, TypeError) as e:
        if verbose:
            print("Failed parsing " + name + "!")
            print(e)
        return False, (name, e)


if __name__ == "__main__":
    verbose = False
    filename = "pyGP.nodes.json"
    for arg in sys.argv:
        if arg == "-v" or arg == "--verbose":
            verbose = True
        if arg == "-h" or arg == "--help":
            print("Usage: command [options] file")
            print("Options:")
            print("-v   --verbose   verbose mode shows modules that are tried to import.")
            print("-h   --help      shows this help")

    if len(sys.argv) > 1 and not sys.argv[-1] == "-v" and not sys.argv[-1] == "--verbose" and not sys.argv[
        -1] == "-h" and not sys.argv[-1] == "--help" and not sys.argv[-1] == "pyGP":
        filename = sys.argv[-1]

    files = [f.replace('./', '').replace('.\\', '') for f in files_by_pattern('.', lambda fn: fn.endswith('.py'))]
    files += [f.replace(GPM_HOME, "gpm") for f in files_by_pattern(GPM_HOME + "/pyGP", lambda fn: fn.endswith('.py'))]
    out_spec = []
    total = len(files)
    i = 1
    errs = []
    for file in files:
        success, nodes = try_load(file, verbose, i, total)
        i += 1
        if success:
            out_spec.extend(nodes)
        elif nodes is not None:
            errs.append(nodes)

    if verbose:
        print("")

    for e in errs:
        name = e[0]
        ex = e[1]
        print("ERROR in module " + name)
        print(ex)
        print("")

    with open(filename, 'w') as f:
        f.write(json.dumps(out_spec, sort_keys=True, indent=4))
    if len(errs) > 0:
        print(str(len(errs)) + " errors occured.")
    else:
        print("Done.")
