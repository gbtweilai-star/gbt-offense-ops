# offense_ops

**One capability bit from GBT V8, packaged standalone.** No. 220 of 341,
`security` domain (Security).

<p>
<img alt="python" src="https://img.shields.io/badge/python-3.9%2B-blue">
<img alt="license" src="https://img.shields.io/badge/license-MIT-green">
<img alt="deps" src="https://img.shields.io/badge/runtime%20dependencies-0-brightgreen">
</p>

> **自主渗透编排**（主人令 2026-10-16：pentagi 全部能力→原生）：蒸自 **vxControl/pentagi**（MIT · Go · 30,549 星）的思想—— 多智能体分工（researcher/pentester/coder/reporter）· 工具面（terminal/browser/search/embeddings）· 跨任务记忆 · 证据链与报告。**护栏优先于它的自主性**：五道闸（授权→没范围不动手 · 不可回滚先问 · 凭据只报已配 · 只对授权目标出网 · 无痕即不存在）。op=plan/roles/tools/evidence/memory/gate/check/route（**全只读·零作用域）。

That description is copied verbatim from the registry. `tests/test_spec.py` pins it,
so documentation drift fails the build instead of shipping quietly.

## What this package actually is

It is the **contract** for one capability: its name, its parameters, the values it
accepts, and whether it can change state that cannot be restored. It is not the
implementation — that lives in the runtime this bit was extracted from.

So `run()` goes through a narrow `Backend` protocol, and the default backend is a
stub that **says so**:

```
status="validated"   backend="stub"   data={"executed": false}
```

Never `status="ok"`. A stub that reports success is worse than no stub, because the
caller stops looking for the real thing.

## Install

```bash
git clone https://github.com/gbtweilai-star/gbt-offense-ops.git
cd gbt-offense-ops
python -m pip install -e ".[dev]"
```

## Use

```bash
python -m gbt_offense_ops info                  # capability card
python -m gbt_offense_ops spec --json           # machine-readable contract
python -m gbt_offense_ops check --payload '{}'
python -m gbt_offense_ops run   --payload '{}'
```

Real `info` output from this machine:

```text
offense_ops  (security)  v1.0.0
----------------------------------------
**自主渗透编排**（主人令 2026-10-16：pentagi 全部能力→原生）：蒸自 **vxControl/pentagi**（MIT · Go · 30,549 星）的思想—— 多智能体分工（researcher/pentester/coder/reporter）· 工具面（terminal/browser/search/embeddings）· 跨任务记忆 · 证据链与报告。**护栏优先于它的自主性**：五道闸（授权→没范围不动手 · 不可回滚先问 · 凭据只报已配 · 只对授权目标出网 · 无痕即不存在）。op=plan/roles/tools/evidence/memory/gate/check/route（**全只读·零作用域）。

gated      : True   <- needs explicit consent
external   : False
multi-op   : True
params     : (none)
values     : researcher, pentester, coder, reporter
```

Wire a real implementation:

```python
from gbt_offense_ops import run

class MyBackend:
    name = "my-backend"
    def invoke(self, cap, payload):
        return {"cap": cap, "handled": sorted(payload)}

result = run({}, backend=MyBackend())
assert result.status == "ok"
```

## Parameters

| name | required | notes |
|---|---|---|
| — | no | the registry declares no required parameters |

Registry hint (`params_hint`): (empty)

**注册表登记的取值 / 子动作（4 个）**：`researcher`、`pentester`、`coder`、`reporter`

Types are deliberately absent: the registry does not declare them, and an invented
type is worse than no type, because callers believe it.

## Boundaries

- Gated: this bit is marked `safe: false` in the registry — it can change state that no inverse action restores.
- No external service dependency declared.
- Multi-op (`multi_op: true`): several sub-actions share one name — read `op` before calling.
- No implementation ships here. Bring a backend; the protocol is one method.

## What this is not

Not a wrapper around a hosted API. Not a model. Not a promise that calling it does
anything on its own. It is the typed seam plus the validation, which is the part that
stays correct even when the implementation changes.

## Tests

```bash
python -m pytest
```

```text
20 passed, 3 skipped in 0.14s
```

## Provenance

| field | value |
|---|---|
| capability | `offense_ops` |
| domain | `security` |
| handler | `offense_ops` |
| safe | `False` (gated = `True`) |
| external | `False` |
| atlas page | [security/offense_ops](https://github.com/gbtweilai-star/gbt-caps/blob/main/caps/security/offense_ops.md) |
| full index | [https://github.com/gbtweilai-star/gbt-caps](https://github.com/gbtweilai-star/gbt-caps) |

The parent README says 348 capabilities; an AST pass over the registry enumerates
`341 + 0 unimplemented + 0 disabled = 341`. The extra 7 are historical duplicates.
Numbering here follows 341 and matches the `gbt-caps` index one-to-one.

## License

MIT.
