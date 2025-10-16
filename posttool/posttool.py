#!/usr/bin/env python3
# -*- coding: utf8 -*-
# tab-width:4
# pylint: disable=no-member # sh
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
    paths: tuple[str, ...],
    verbose_inf: bool,
    dict_output: bool,
    verbose: bool = False,
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
                    "-F",
                    f"file=@{path.as_posix()}",
                    "http://0x0.st",
                    _err=sys.stdout,
                )

            output(
                result,
                reason=_path,
                dict_output=dict_output,
                tty=tty,
                verbose=verbose,
            )
