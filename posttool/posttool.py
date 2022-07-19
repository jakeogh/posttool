#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4

# pylint: disable=missing-docstring               # [C0111] docstrings are always outdated and wrong
# pylint: disable=missing-module-docstring        # [C0114]
# pylint: disable=fixme                           # [W0511] todo is encouraged
# pylint: disable=line-too-long                   # [C0301]
# pylint: disable=too-many-instance-attributes    # [R0902]
# pylint: disable=too-many-lines                  # [C0302] too many lines in module
# pylint: disable=invalid-name                    # [C0103] single letter var names, name too descriptive
# pylint: disable=too-many-return-statements      # [R0911]
# pylint: disable=too-many-branches               # [R0912]
# pylint: disable=too-many-statements             # [R0915]
# pylint: disable=too-many-arguments              # [R0913]
# pylint: disable=too-many-nested-blocks          # [R1702]
# pylint: disable=too-many-locals                 # [R0914]
# pylint: disable=too-few-public-methods          # [R0903]
# pylint: disable=no-member                       # [E1101] no member for base
# pylint: disable=attribute-defined-outside-init  # [W0201]
# pylint: disable=too-many-boolean-expressions    # [R0916] in if statement
from __future__ import annotations

import os
import sys
from collections.abc import Sequence
from pathlib import Path
from signal import SIG_DFL
from signal import SIGPIPE
from signal import signal

import click
import sh
from asserttool import ic
from classify import classify
from clicktool import click_add_options
from clicktool import click_global_options
from clicktool import tv
from inputtool import yn_question
from mptool import output

signal(SIGPIPE, SIG_DFL)


@click.command()
@click.argument("paths", type=str, nargs=-1)
@click_add_options(click_global_options)
@click.pass_context
def cli(
    ctx,
    paths: Sequence[str],
    verbose: bool | int | float,
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
