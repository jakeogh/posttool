#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=C0111  # docstrings are always outdated and wrong
# pylint: disable=C0114  # Missing module docstring (missing-module-docstring)
# pylint: disable=W0511  # todo is encouraged
# pylint: disable=C0301  # line too long
# pylint: disable=R0902  # too many instance attributes
# pylint: disable=C0302  # too many lines in module
# pylint: disable=C0103  # single letter var names, func name too descriptive
# pylint: disable=R0911  # too many return statements
# pylint: disable=R0912  # too many branches
# pylint: disable=R0915  # too many statements
# pylint: disable=R0913  # too many arguments
# pylint: disable=R1702  # too many nested blocks
# pylint: disable=R0914  # too many local variables
# pylint: disable=R0903  # too few public methods
# pylint: disable=E1101  # no member for base
# pylint: disable=W0201  # attribute defined outside __init__
# pylint: disable=R0916  # Too many boolean expressions in if statement


import os
import sys
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal
from typing import Sequence
from typing import Union

import click
import sh
from asserttool import ic
from classify import classify
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from inputtool import yn_question
from mptool import output
from mptool import unmp

signal(SIGPIPE, SIG_DFL)


@click.command()
@click.argument("paths", type=str, nargs=-1)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    paths: Sequence[str],
    verbose: Union[bool, int, float],
    verbose_inf: bool,
    dict_input: bool,
) -> None:

    tty, verbose = tv(
        ctx=ctx,
        verbose=verbose,
        verbose_inf=verbose_inf,
    )

    iterator = paths
    del paths

    index = 0
    for index, _path in enumerate(iterator):
        path = Path(os.fsdecode(_path)).resolve()
        if verbose:
            ic(index, path)

        path_file_type = classify(path, verbose=verbose)[0]
        ic(path_file_type)
        if yn_question(f"confirm posting {path}", verbose=verbose):
            if path_file_type == "text":
                result = sh.wgetpaste(path)
            elif path_file_type == "image":
                # curl -F'file=@yourfile.png' http://0x0.st
                result = sh.curl(
                    "-F", f"file=@{path.as_posix()}", "http://0x0.st", _err=sys.stdout
                )

            output(
                result,
                reason=_path,
                dict_input=dict_input,
                tty=tty,
                verbose=verbose,
            )


if __name__ == "__main__":
    # pylint: disable=E1120
    cli()
