PK="/home/aitsaidn/PhD/playground/axspike/riscv-lp64d/riscv64-unknown-elf/bin/pk"
DASM="/home/aitsaidn/PhD/playground/axspike/riscv-lp64d/bin/spike-dasm"

# Argument $1  ==> the elf executable file
# Argument $2  ==> csv file
# Argument $3  ==> Benchmark Name

time ../work-ver/Variane_testharness ${PK} $1 2>&1 | spike-dasm | less | python3 generate_insn_breakdown.py $2 $3


