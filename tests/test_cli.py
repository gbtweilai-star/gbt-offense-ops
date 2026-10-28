"""CLI tests: the commands a stranger will actually type."""

from __future__ import annotations

import json

import pytest

from gbt_offense_ops.cli import main


def test_info_exits_zero_and_names_the_capability(capsys):
    assert main(["info"]) == 0
    out = capsys.readouterr().out
    assert "offense_ops" in out
    assert "security" in out


def test_spec_json_is_machine_readable(capsys):
    assert main(["spec", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["name"] == "offense_ops"
    assert isinstance(data["params"], list)


def test_check_reports_the_contract(capsys):
    code = main(["check", "--payload", "{}"])
    out = capsys.readouterr().out
    assert code in (0, 1)
    assert "ok" in out or "rejected" in out


def test_run_prints_a_json_envelope(capsys):
    assert main(["run", "--payload", '{}']) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["cap"] == "offense_ops"
    assert envelope["status"] in ("ok", "validated")


def test_bad_json_exits_two(capsys):
    assert main(["check", "--payload", "{oops"]) == 2
    assert "not valid JSON" in capsys.readouterr().err
