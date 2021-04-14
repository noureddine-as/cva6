#!/usr/bin/python3

import sys
import re
from functools import reduce

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import seaborn as sns
from matplotlib.colors import ListedColormap
from classify_insn_cincluded import *



BENCH_array        =  []
FMEM_array         =  ["FP mem. insns."]# ["FMEM"]
FARITH_array       =  ["FP arith. insns."]# ["FARITH"]
FOTHERS_array      =  ["Other FP insns."]# ["FOTHERS"]
IMEM_array         =  ["Integer mem. insns."]# ["IMEM"]
IARITH_array       =  ["Integer arith. insns."]# ["IARITH"]
OTHERS_array       =  ["Others insns."]# ["OTHERS"]

#########
# Setup graphs
# Setup

# import pandas as pd
# import numpy as np

# import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pl

from matplotlib.font_manager import FontProperties

fontP = FontProperties()
# fontP.set_size('x-small')
fontP.set_size('small')

# plt.style.use('fivethirtyeight')

# plt.style.use(['science','ieee', 'grid', 'bright']) # , 'high-vis'])
plt.style.use(['science','ieee', 'grid', 'bright']) # , 'high-vis'])

# plt.rcParams['figure.figsize'] = [8, 5]
plt.rcParams['figure.dpi'] = 300 # 200 e.g. is really fine, but slower

params = {'legend.fontsize': 8,
          'legend.handlelength': 0.75}
plt.rcParams.update(params)

pd.set_option('precision', 17)


# CONVERGENCE_THRESHOLD = 1.e-10
#########

def export_dict_to_file(file_name, dicto, column_title):
    with open(file_name, 'w') as f:
        f.write("Instruction names,%s\n"%column_title)
        for item in dicto.items():
            f.write(item[0] + ',' + str(item[1]) + '\n')
            # f.write('Ray, a drop of golden sun\n')
    f.close()

def collect_statistics_dictionaries(in_stream):
    """
        2 Steps: - Insn. registration: keep a log of all translated insns
                 - insn. counting    : cont instructions only whe START_INSTRUMENTATION is True
    """
    # VPT Code -------------------------------------------------------------------------
    # inline uint64_t VPT_START_INSTRUMENTATION(void){
    #     unsigned int returned_value = 0;
    #     __asm__ volatile ("csrrw    %0, 0x803, %1"  /* read and write atomically */
    # 10320:	00100513          	li	a0,1
    # 10324:	80351573          	csrrw	a0,0x803,a0
    # inline uint64_t VPT_STOP_INSTRUMENTATION(void){
    #     unsigned int returned_value = 0;
    #     __asm__ volatile ("csrrw    %0, 0x803, %1"  /* read and write atomically */
    # 10334:	00000513          	li	a0,0
    # 10338:	80351573          	csrrw	a0,0x803,a0
    # INSTRUMENTATION_CODE = "80351573"  # 80379773

    new_insn_coming        = False

    addr_to_insn_dict = {}   # {known instruction name : count}
    insns_counts_dict = {}  # {known instruction name : count}

    START_INSTRUMENTATION     = False
    START_INSTRUMENTATION_pcs = []
    STOP_INSTRUMENTATION_pcs  = []
    for line in in_stream:
        # Remove trailing newline characters using strip()
        # if 'exit' == line.strip():
        #     print('Found exit. Terminating the program')
        #     exit(0)
        # else:
        # print('Message from sys.stdin: ---> {} <---'.format(line))
        # print(line)

        # Remove additional spaces
        line = re.sub(' +', ' ', line).strip()
        
        if new_insn_coming :
            # Register new instruction
            if line[0:2] == "0x" :

                def register_normal_insn():
                    # Extract address and insn
                    addr = line[2:].split(":")[0]
                    insn = line[2:].split(":")[1].lstrip().split(" ")[1].split(" ")[0]

                    # Register this instruction
                    addr_to_insn_dict.update( {addr : insn} )                   # @addr -->  insn   register
                    insns_counts_dict[insn] = insns_counts_dict.get(insn, 0)    # insn  -->  count  register

                def register_csrrw_insn():
                    # Extract address and insn
                    addr = line[2:].split(":")[0]
                    insn = line[2:].split(":")[1].lstrip().split(" ")[1].split(" ")[0]

                    # Register this instruction
                    addr_to_insn_dict.update( {addr : insn} )                   # @addr -->  insn   register
                    insns_counts_dict[insn] = insns_counts_dict.get(insn, 0)    # insn  -->  count  register

                    return addr

                # INSTRUMENTATION Management
                if      ("0x803" in line) \
                    and ("803"  in line):

                    instrumentation_insn = register_csrrw_insn()

                    # print(line)
                    # print(instrumentation_insn)
                    # exit()

                    if START_INSTRUMENTATION :
                        # print("Found STOP_INSTRUMENTATION")
                        STOP_INSTRUMENTATION_pcs.append(instrumentation_insn)
                    else :
                        # print("Found START_INSTRUMENTATION")
                        START_INSTRUMENTATION_pcs.append(instrumentation_insn)

                    # We assume we always start with a START_INSTRUMENTATION
                    # We assume a STOP_INSTRUMENTATION always comes after a START_INSTRUMENTATION
                    # START_INSTRUMENTATION = not(START_INSTRUMENTATION)

                else :
                    # Normal Instruction to be counted
                    # if ( START_INSTRUMENTATION ) :
                    register_normal_insn()

                new_insn_coming = False


        elif "IN:" in line :
            # Signal that a new instruction is coming

            new_insn_coming = True
            # @TODO COllect function from here if you want

        elif "pc" in line :
            addr = line.split("pc")[1].strip()
            
            if addr in START_INSTRUMENTATION_pcs :
                # print("Found START_INSTRUMENTATION")
                START_INSTRUMENTATION = True
                # continue
            elif addr in STOP_INSTRUMENTATION_pcs :
                # print("Found STOP_INSTRUMENTATION")
                START_INSTRUMENTATION = False
                # continue
            elif ( START_INSTRUMENTATION ):
                # If we're here, it means the insn has already been registered
                corresponding_insn = addr_to_insn_dict[addr]
                # insns_counts_dict[corresponding_insn] = insns_counts_dict.get(corresponding_insn, 0) + 1
                insns_counts_dict[corresponding_insn] = insns_counts_dict[corresponding_insn] + 1

                # print("Address found: %s"%addr)
                # print("Instru. found: %s"%insn)

    # To verify that the counting was OK
    # Check that all the counted instructions figure out in the <@addr to insn> map values

    counted_insns_set    = set(insns_counts_dict.keys())
    all_mapped_insns_set = set(addr_to_insn_dict.values())


    if counted_insns_set == all_mapped_insns_set :
        print("RESULTS ARE VALID")
    else :
        print("RESULTS ARE (IN)VALID - Please check!!")
        print(counted_insns_set)
        print(all_mapped_insns_set)
        raise

    # print(insns_counts_dict)
    # print(addr_to_insn_dict)
    return (insns_counts_dict,addr_to_insn_dict)

def collect_statistics_dictionaries_cva6(in_stream):
    """
        2 Steps: - Insn. registration: keep a log of all translated insns
                 - insn. counting    : cont instructions only whe START_INSTRUMENTATION is True

        Example of CVA6 dump
              323566                    1 0x80001390 M (0x00379793) slli    a5, a5, 3
              323568                    2 0x80001394 M (0x00f707b3) add     a5, a4, a5
              323571                    3 0x80001398 M (0x0007b703) ld      a4, 0(a5)
              323572                    1 0x8000139c M (0x00177693) andi    a3, a4, 1
              323573                    1 0x800013a0 M (0x02068063) beqz    a3, pc + 32
              323574                    1 0x800013a4 M (0x00c55513) srli    a0, a0, 12
              323575                    1 0x800013a8 M (0x00a75713) srli    a4, a4, 10
              323576                    1 0x800013ac M (0x1ff57513) andi    a0, a0, 511
    """
    # VPT Code -------------------------------------------------------------------------
    # inline uint64_t VPT_START_INSTRUMENTATION(void){
    #     unsigned int returned_value = 0;
    #     __asm__ volatile ("csrrw    %0, 0x803, %1"  /* read and write atomically */
    # 10320:	00100513          	li	a0,1
    # 10324:	80351573          	csrrw	a0,0x803,a0
    # inline uint64_t VPT_STOP_INSTRUMENTATION(void){
    #     unsigned int returned_value = 0;
    #     __asm__ volatile ("csrrw    %0, 0x803, %1"  /* read and write atomically */
    # 10334:	00000513          	li	a0,0
    # 10338:	80351573          	csrrw	a0,0x803,a0
    # INSTRUMENTATION_CODE = "80351573"  # 80379773

    addr_to_insn_dict = {}   # {known instruction name : count}
    insns_counts_dict = {}  # {known instruction name : count}
    insns_cycles_dict = {}  # {known instruction name : count}

    START_INSTRUMENTATION     = False

    START_INSTRUMENTATION_count = 0
    STOP_INSTRUMENTATION_count = 0
    # START_INSTRUMENTATION_pcs = []
    # STOP_INSTRUMENTATION_pcs  = []

    last_registered_cycle_li    = 0
    last_registered_cycle_csrrw = 0

    for line in in_stream:
        # Remove additional spaces
        line = re.sub(' +', ' ', line).strip()

        # print(line)

        if "VPTMAGICOP write fvpt_exec_mode" in line :
            new_val = line.split("write fvpt_exec_mode")[1].strip().split(" ")[0]
            # print(new_val)
            
            if new_val == '0' :
                START_INSTRUMENTATION = False

                STOP_INSTRUMENTATION_count += 1

                # Uncount the last li and csrrw cycles
                insns_cycles_dict['li']    = insns_cycles_dict.get('li',    last_registered_cycle_li   ) - last_registered_cycle_li
                insns_cycles_dict['csrrw'] = insns_cycles_dict.get('csrrw', last_registered_cycle_csrrw) - last_registered_cycle_csrrw

                # Uncount the last li and csrrw instructions
                insns_counts_dict['li']    = insns_counts_dict.get('li',    1) - 1
                insns_counts_dict['csrrw'] = insns_counts_dict.get('csrrw', 1) - 1

            elif new_val == '1' :
                START_INSTRUMENTATION = True

                START_INSTRUMENTATION_count += 1
            
            continue
      
        if START_INSTRUMENTATION and (" U (0x" in line) :
            # We detected a valid insn
            # def register_normal_insn():
            # Extract address and insn
            addr   = line.split(" U (0x")[0].split(" ")[-1][2:]   # Avoid the 0x
            insn   = line.split(" U (0x")[1].split(" ")[1]
            cycles = int(line.split(" U (0x")[0].split(" ")[-2])

            # print('Addr = "' + addr +'"')
            # print('Insn = "' + insn +'"')
            # print('Cycles = "' + str(cycles) +'"')

            # Register this instruction
            addr_to_insn_dict.update( {addr : insn} )                       # @addr -->  insn   register
            insns_counts_dict[insn] = insns_counts_dict.get(insn, 0) + 1    # insn  -->  count  register
            insns_cycles_dict[insn] = insns_cycles_dict.get(insn, 0) + cycles       # insn  -->  count  register

            # Save nb of cycles if csrrw or li
            if insn == 'li' :
                last_registered_cycle_li = cycles
            if insn == 'csrrw' :
                last_registered_cycle_csrrw = cycles

            # register_normal_insn()

    # To verify that the counting was OK
    # Check that all the counted instructions figure out in the <@addr to insn> map values

    counted_insns_set    = set(insns_counts_dict.keys())
    all_mapped_insns_set = set(addr_to_insn_dict.values())
    cyclecounted_insns_set    = set(insns_cycles_dict.keys())
    

    if      (counted_insns_set == all_mapped_insns_set ) \
        and (counted_insns_set == cyclecounted_insns_set) :
        print("RESULTS ARE VALID")
        print("Nb. of START_INSTRUMENTATION =   %d"%START_INSTRUMENTATION_count)
        print("Nb. of STOP_INSTRUMENTATION  =   %d"%STOP_INSTRUMENTATION_count)
    else :
        print("RESULTS ARE (IN)VALID - Please check!!")
        print(counted_insns_set)
        print(all_mapped_insns_set)
        raise

    # print(insns_counts_dict)
    # print(addr_to_insn_dict)
    return (insns_counts_dict, insns_cycles_dict, addr_to_insn_dict)

def csv_to_figure(csv_file, app_name, figure_title, plot_only=False):
        # brute data executions
    data_executions = pd.read_csv(csv_file, sep=',', index_col =0, header=0,
                        names=["Instruction names", app_name])
    summ = sum(data_executions[ app_name ])
    
    data_executions_percentages = 100. * data_executions / float(summ)

    # FMEM type count
    fmem_count = 0.0
    for insn in FMEM :
        if insn in data_executions_percentages.index :
            fmem_count += data_executions_percentages.loc[ insn ][0]

    # FARITH type count
    farith_count = 0.0
    for insn in FARITH :
        if insn in data_executions_percentages.index :
            farith_count += data_executions_percentages.loc[ insn ][0]

    # FOTHERS type count
    fothers_count = 0.0
    for insn in FMOV :
        if insn in data_executions_percentages.index :
            fothers_count += data_executions_percentages.loc[ insn ][0]
    for insn in FMAX_MIN :
        if insn in data_executions_percentages.index :
            fothers_count += data_executions_percentages.loc[ insn ][0]
    for insn in FSGN_INJECT :
        if insn in data_executions_percentages.index :
            fothers_count += data_executions_percentages.loc[ insn ][0]
    for insn in FCOMPARE :
        if insn in data_executions_percentages.index :
            fothers_count += data_executions_percentages.loc[ insn ][0]
    for insn in FCLASS :
        if insn in data_executions_percentages.index :
            fothers_count += data_executions_percentages.loc[ insn ][0]
    for insn in FCONV :
        if insn in data_executions_percentages.index :
            fothers_count += data_executions_percentages.loc[ insn ][0]

    # IMEM type count
    imem_count = 0.0
    for insn in IMEM :
        if insn in data_executions_percentages.index :
            imem_count += data_executions_percentages.loc[ insn ][0]

    # IARITH
    iarith_count = 0.0
    for insn in IARITH :
        if insn in data_executions_percentages.index :
            iarith_count += data_executions_percentages.loc[ insn ][0]

    # Others_count
    others_count = 100.0 - fmem_count - farith_count - fothers_count - imem_count - iarith_count

    # Append to the external dataframe
    BENCH_array.append(app_name)
    FMEM_array.append(fmem_count)
    FARITH_array.append(farith_count)
    FOTHERS_array.append(fothers_count)
    IMEM_array.append(imem_count)
    IARITH_array.append(iarith_count)
    OTHERS_array.append(others_count)

    # Summary
    df = pd.DataFrame(columns=["Instruction types"] + BENCH_array)
    df.loc[5] = FARITH_array
    df.loc[4] = FMEM_array
    df.loc[3] = FOTHERS_array
    df.loc[2] = IMEM_array
    df.loc[1] = IARITH_array
    df.loc[0] = OTHERS_array

    # Create fig, ax
    figure, ax = plt.subplots()

    df.set_index('Instruction types')\
        .reindex(df.set_index('Instruction types').sum().sort_values().index, axis=1)\
        .T.plot(ax=ax, kind='barh', stacked=True, align='center', width=0.7,
                colormap=ListedColormap(sns.color_palette()), # "r_rocket", 6)), 
                figsize=(5, 1.25))

    ### ---------------- ANNOTATE ----------------------------

    cnt=0
    for p in ax.patches:

        # print(p)

        width = p.get_width()
        x = p.get_x() + p.get_width()/2.
        y = p.get_y() + p.get_height()/2.
        
        # Only print percentages that are >= 5%
        if width >= 5.0 :
            ax.text(x, y,'{:1.1f}\%'.format(p.get_width()), color='k',
                            ha='center', va='center')
            
        cnt=cnt+1
        continue

        # width = p.get_width()
        # a = p.get_width()-5
        # clr = 'black'

        ax.text(a, p.get_y()+0.55*p.get_height(),'{:1.2f}'.format(width),color=clr,ha='center', va='center')
    ### ---------------- END OF ANNOTATE ----------------------------


    ax.set_xticks(ticks=np.arange(0,101,5)) #rotation=90)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    # figure = plt.gcf() # get current figure

    figure.suptitle('%s'%(figure_title), y = 0.98) # 92)
    # figure.suptitle('%s - %s'%(figure_title, app_name), y = 0.98) # 92)

    ax.grid(False)

    # plt.savefig('%s_%s.png'%(csv_file, app_name), bbox_inches='tight', dpi=300)
    figure.savefig('%s.pdf'%(csv_file), format='pdf',
                transparent=False, bbox_inches='tight')

    if plot_only :
        with open('%s.tex'%(csv_file), 'w') as f:
            f.write(df.to_latex(index = False))
        f.close()

if __name__ == "__main__":
    PLOT_ONLY = True

    stdin_fileno = sys.stdin
    output_csv = sys.argv[1]
    benchmark_name = sys.argv[2]

    if not PLOT_ONLY :
        # Keeps reading from stdin and quits only if the word 'exit' is there
        # Analyse the trace
        (insns_counts_dict, insns_cycles_dict, addr_to_insn_dict) = collect_statistics_dictionaries_cva6(in_stream=stdin_fileno) 
        # Save executed insns to a CSV file
        export_dict_to_file("%s_insn_count.csv"%output_csv, insns_counts_dict, column_title="#Executions")
        export_dict_to_file("%s_insn_cycles.csv"%output_csv, insns_cycles_dict, column_title="#Cycles")

    # Read back the CSV file and save the stats as png
    csv_to_figure("%s_insn_cycles.csv"%output_csv, "\#Cycles per Insn", figure_title="%s"%benchmark_name, plot_only=PLOT_ONLY)
    csv_to_figure("%s_insn_count.csv"%output_csv , "\#Insns", figure_title="%s"%benchmark_name, plot_only=PLOT_ONLY)

