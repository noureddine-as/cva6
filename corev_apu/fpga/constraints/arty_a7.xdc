## Clock signal
set_property -dict { PACKAGE_PIN E3    IOSTANDARD LVCMOS33 } [get_ports sys_clk_i ];
create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5} [get_ports sys_clk_i]

## Buttons
# Button 0 is reset
set_property -dict { PACKAGE_PIN D9    IOSTANDARD LVCMOS33 } [get_ports cpu_resetn ];

## Switches
# Only sw[0-3] are mapped on Arty 
set_property -dict { PACKAGE_PIN A8    IOSTANDARD LVCMOS33 } [get_ports { sw[0] }];
set_property -dict { PACKAGE_PIN C11   IOSTANDARD LVCMOS33 } [get_ports { sw[1] }];
set_property -dict { PACKAGE_PIN C10   IOSTANDARD LVCMOS33 } [get_ports { sw[2] }];
set_property -dict { PACKAGE_PIN A10   IOSTANDARD LVCMOS33 } [get_ports { sw[3] }];

## LEDs
# Only led[0-3] ar mapped on Arty 
set_property -dict { PACKAGE_PIN H5    IOSTANDARD LVCMOS33 } [get_ports { led[0] }];
set_property -dict { PACKAGE_PIN J5    IOSTANDARD LVCMOS33 } [get_ports { led[1] }];
set_property -dict { PACKAGE_PIN T9    IOSTANDARD LVCMOS33 } [get_ports { led[2] }];
set_property -dict { PACKAGE_PIN T10   IOSTANDARD LVCMOS33 } [get_ports { led[3] }];

## SMSC Ethernet PHY
# Ethernet is not mapped on Arty yet

## USB-UART Interface (FTDI FT2232H)
set_property -dict { PACKAGE_PIN D10   IOSTANDARD LVCMOS33  } [get_ports tx ];
set_property -dict { PACKAGE_PIN A9    IOSTANDARD LVCMOS33  } [get_ports rx ];

## Pmod Header JD for FTDI FT2232 JTAG
set_property -dict { PACKAGE_PIN D4    IOSTANDARD LVCMOS33 } [get_ports tdo ];
set_property -dict { PACKAGE_PIN D3    IOSTANDARD LVCMOS33 } [get_ports trst_n ];
set_property -dict { PACKAGE_PIN F4    IOSTANDARD LVCMOS33 } [get_ports tck ];
set_property -dict { PACKAGE_PIN E2    IOSTANDARD LVCMOS33 } [get_ports tdi ];
set_property -dict { PACKAGE_PIN D2    IOSTANDARD LVCMOS33 } [get_ports tms ];

## ChipKit SPI
set_property -dict { PACKAGE_PIN G1    IOSTANDARD LVCMOS33 } [get_ports { spi_miso }];
set_property -dict { PACKAGE_PIN H1    IOSTANDARD LVCMOS33 } [get_ports { spi_mosi }];
set_property -dict { PACKAGE_PIN F1    IOSTANDARD LVCMOS33 } [get_ports { spi_clk_o }];
set_property -dict { PACKAGE_PIN C1    IOSTANDARD LVCMOS33 } [get_ports { spi_ss }];

# Arty A7 100T has a quad SPI flash
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]

# Ignore DRC errors due to unconstrained pins in bitstream generation
# set_property BITSTREAM.General.UnconstrainedPins {Allow} [current_design]

## JTAG
# minimize routing delay

set_max_delay -to   [get_ports { tdo } ] 20
set_max_delay -from [get_ports { tms } ] 20
set_max_delay -from [get_ports { tdi } ] 20
set_max_delay -from [get_ports { trst_n } ] 20

# reset signal
set_false_path -from [get_ports { trst_n } ]
# set_false_path -from [get_pins i_ddr/u_xlnx_mig_7_ddr3_mig/u_ddr3_infrastructure/rstdiv0_sync_r1_reg_rep/C]

## Configuration options, can be used for all designs
set_property CONFIG_VOLTAGE 3.3 [current_design]
set_property CFGBVS VCCO [current_design]

# Accept sub-optimal placement
set_property CLOCK_DEDICATED_ROUTE BACKBONE [get_nets sys_clk_i_IBUF]