import sys
from types import ModuleType


class Dummy(object):
    def __init__(self, *args, **kwargs):
        object.__setattr__(self, "___dict", {})

    def __add__(self, other):
        return Dummy()

    def __sub__(self, other):
        return Dummy()

    def __mul__(self, other):
        return Dummy()

    def __truediv__(self, other):
        return Dummy()

    def __floordiv__(self, other):
        return Dummy()

    def __mod__(self, other):
        return Dummy()

    def __pow__(self, other, modulo=None):
        return Dummy()

    def __lshift__(self, other):
        return Dummy()

    def __rshift__(self, other):
        return Dummy()

    def __and__(self, other):
        return Dummy()

    def __xor__(self, other):
        return Dummy()

    def __or__(self, other):
        return Dummy()

    def __iadd__(self, other):
        pass

    def __isub__(self, other):
        pass

    def __imul__(self, other):
        pass

    def __idiv__(self, other):
        pass

    def __ifloordiv__(self, other):
        pass

    def __imod__(self, other):
        pass

    def __ipow__(self, other, modulo=None):
        pass

    def __ilshift__(self, other):
        pass

    def __irshift__(self, other):
        pass

    def __iand__(self, other):
        pass

    def __ixor__(self, other):
        pass

    def __ior__(self, other):
        pass

    def __neg__(self):
        return Dummy()

    def __pos__(self):
        return Dummy()

    def __abs__(self):
        return Dummy()

    def __invert__(self):
        return Dummy()

    def __complex__(self):
        return 1 + 0j

    def __int__(self):
        return 1

    def __long__(self):
        return 1

    def __float__(self):
        return 1.0

    def __oct__(self):
        return oct(1)

    def __hex__(self):
        return hex(1)

    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return True

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __getattr__(self, attr):
        return self[attr]

    def __getitem__(self, key):
        d = object.__getattribute__(self, "___dict")
        if key in d:
            return d[key]
        dummy = Dummy()
        d[key] = dummy
        return dummy

    def __setitem__(self, key, value):
        object.__getattribute__(self, "___dict")[key] = value

    def __setattr__(self, key, value):
        self[key] = value

    def __call__(self, *args, **kwargs):
        return Dummy()

    def __len__(self):
        return 1

    def __str__(self):
        return ""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is None

    def __repr__(self):
        return ""

    def __nonzero__(self):
        return True

    def __bool__(self):
        return True


class DummyModule(Dummy, ModuleType):
    pass


class DummyDict(dict):
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        val = dict.__getitem__(self, key)
        if isinstance(val, dict) and not isinstance(val, DummyDict):
            val = DummyDict(val)
            self[key] = val
        return val


def disable(globals_=None):
    """
    Replaces all active wandb objects with dummy objects
    """
    import wandb

    wandb_module = wandb._wandb_module
    for m in sys.modules:
        # if m == wandb_module or (  # we leave wandb so that wandb.log etc works
        if m.startswith(wandb_module + ".") and not m.startswith(
            wandb_module + ".dummy"
        ):
            sys.modules[m] = DummyModule()
    if globals_:
        for k, v in globals_.items():
            m = getattr(
                v, "__module__", v.__name__ if isinstance(v, ModuleType) else ""
            )
            # if m == wandb_module or (
            if m.startswith(wandb_module + ".") and not m.startswith(
                wandb_module + ".dummy"
            ):
                globals_[k] = Dummy()

    class ImportHook:
        def find_module(self, fullname, path=None):
            if fullname.startswith(wandb_module + "."):
                return self

        def load_module(self, fullname):
            module = DummyModule()
            sys.modules[fullname] = module
            return module

    # disable importing wandb sub modules
    sys.meta_path.insert(0, ImportHook())
