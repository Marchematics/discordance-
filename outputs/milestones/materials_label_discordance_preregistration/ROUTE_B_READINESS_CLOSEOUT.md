# Route B Readiness Closeout

Route B was frozen as the only allowed rescue:

```text
Materials Project API-derived records
vs independently downloaded Alexandria/alex-mp snapshot
strict StructureMatcher denominator
n_common >= 200
same ALIGNN-FF / CHGNet / MACE-MP denominator
stable-class F1 endpoint unchanged
```

The data-source side is ready enough for a future snapshot export:

- Materials Project API smoke query passed.
- Local `alex_mp_20.zip` exists.

The primary model-denominator gate is not ready:

- CHGNet is locally executable.
- MACE-MP is locally executable.
- ALIGNN-FF is not currently executable as a same-denominator scorer. The
  installed `alignn.ff` default model download attempted
  `v12.2.2024_dft_3d_307k`, but the response was not a valid zip and raised
  `BadZipFile`.

Under the frozen Route B protocol, the endpoint cannot be replaced by
CHGNet/MACE-only. Therefore Route B is blocked before the full rescue outcome.
The NMI discordance line remains closed unless a legal, reproducible ALIGNN-FF
scorer becomes available before the one-shot rescue is run.

This closeout does not consume a full Route B outcome because the strict
same-denominator primary model set could not be assembled.
