onerror {exit -code 1}
vlib work
vlog -work work HW1.vo
vlog -work work Waveform2.vwf.vt
vsim -novopt -c -t 1ps -L cyclonev_ver -L altera_ver -L altera_mf_ver -L 220model_ver -L sgate_ver -L altera_lnsim_ver work.carr_select_16_using4_vlg_vec_tst -voptargs="+acc"
vcd file -direction HW1.msim.vcd
vcd add -internal carr_select_16_using4_vlg_vec_tst/*
vcd add -internal carr_select_16_using4_vlg_vec_tst/i1/*
run -all
quit -f
