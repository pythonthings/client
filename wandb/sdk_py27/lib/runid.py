"""
runid util.
"""

import shortuuid  # type: ignore


def generate_id():
    # ~3t run ids (36**8)
    run_gen = shortuuid.ShortUUID(alphabet=list("0123456789abcdefghijklmnopqrstuvwxyz"))
    return run_gen.random(8)
