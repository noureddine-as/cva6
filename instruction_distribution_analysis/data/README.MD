

Example commands:


### In order to re-generate the plots only

First set the `PLOT_ONLY` variable in the `generate_insn_breakdown.py` python script to `True`, then execute the command :

```bash
python3 generate_insn_breakdown.py data/jacobi Jacobi
python3 generate_insn_breakdown.py data/gauss_seidel Gauss-Seidel
```

WARNING: You may have to permute the last two lines, to modify the order of `#Insns` and `#Cycles per Insn`

### TO launch the total simulation

```bash
./run_with_cva6.sh JACOBI_pk_0 data/jacobi Jacobi
./run_with_cva6.sh GAUSS_SEIDEL_pk_0 data/gauss_seidel Gauss-Seidel
```

Where `GAUSS_SEIDEL_pk_0` is the application compiled using `riscv64-unknown-elf-gcc`, with printfs and VPT deactivated.



