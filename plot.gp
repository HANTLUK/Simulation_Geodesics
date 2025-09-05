set term cairolatex pdf size 8cm,5cm color colortext font ",11"

set decimalsign "." # für den input
#               Style
# !!!___________________________ !!!
set grid xtics
set grid ytics
# set grid mxtics
# set grid mytics
set style line 80 linetype 1 linecolor rgb "#888888"
set style line 81 linetype 1 linecolor rgb "#808080" linewidth 0.5
set border back linestyle 80
set grid back linestyle 81
set xtics textcolor rgb "#808080"
set ytics textcolor rgb "#808080"
set y2tics textcolor rgb "#808080"


set xlabel "Angle $\\alpha$ of Rotation in $x$ Direction"
set ylabel "Gate Error $\\epsilon$"

set xrange [-pi+0.1:pi-0.1]
set yrange [0:2.5]

set nokey

set output "Figures/gnuplot_error_dia_x.tex"

set title "Comparison of Numerical Error for $x$ Rotations"
plot 'Tabs/tab_error_dia_x.dat' using 1:2 with points lw 2 ps 0.4, 'Tabs/tab_error_dia_x.dat' using 1:3 with lines lw 2


set xlabel "Arclength for Rotation in $y$ Direction"
set ylabel "Gate Error $\\epsilon$"

set xrange [0:5.4]
set yrange [0:1.8]

set nokey

set output "Figures/gnuplot_error_dia_y_arclength.tex"

set title "Comparison of Numerical Error for $y$ Rotations"
plot 'Tabs/tab_error_dia_y.dat' using 1:2 with points lw 2 ps 0.4, 'Tabs/tab_error_dia_y.dat' using 1:3 with lines lw 2


set term cairolatex pdf size 8cm,7cm color colortext font ",11"

set xlabel "Arclength for Rotation in $y$ Direction"
set ylabel "Distance and Bounds"

set xrange [0:pi]
set yrange [0:2*pi]

set nokey

set output "Figures/gnuplot_y_arclength.tex"

set title "Estimates of the sub-Riemannian $\\dd_{CC}$ Distance"
plot 'Tabs/tab_arclength_y.dat' using 1:2 with lines lw 2 lc "#4433FF", 'Tabs/tab_arclength_y.dat' using 1:6 with lines lw 2 lc"#FF5566", 'Tabs/tab_arclength_y.dat' using 1:4 with lines lw 2 lc "#4433FF", 'Tabs/tab_arclength_y.dat' using 1:5 with lines lw 2 lc "#FF5566", 'Tabs/tab_arclength_y.dat' using 3:7 with lines lw 2 lc "#000000"

# Plot der Control Function
set term cairolatex pdf size 9cm,6.3cm color colortext font ",11"

set output "Figures/gnuplot_controls.tex"

set xlabel "Time $t$"
set ylabel "Controls $c(t)$"

set xrange [*:*]
set yrange [*:*]

set title "Controls of the Geodesic"
plot 'Tabs/tab_curve_controls.dat' using 1:2 with lines lw 2, \
'Tabs/tab_curve_controls.dat' using 1:3 with lines lw 2


set term cairolatex pdf size 8cm,8cm color colortext font ",11"

set xlabel ""
set ylabel ""
set zlabel ""

set arrow from -0.2,0,0 to 0.5,0,0 nohead lc rgb 'black' lw 2  # X-axis arrow
set arrow from 0,0,0 to 0,0.8,0 nohead lc rgb 'black' lw 2 # Y-axis arrow
set arrow from 0,0,0 to 0,0,0.7 nohead lc rgb 'black' lw 2  # Z-axis arrow
set label 'X' at 0.6,0,0 center
set label 'Y' at 0,1.1,0 center
set label 'Z' at 0,0,0.8 center

unset grid
unset border
set view equal xyz
set ticslevel 0
set notics

set xrange [-0.2:0.5]
set yrange [0:0.9]
set zrange [0:0.7]

set lmargin at screen 0.2  # Left margin
set rmargin at screen 1.2  # Right margin
set tmargin at screen 0.90  # Top margin
set bmargin at screen 0.2  # Bottom margin

set nokey

set output "Figures/gnuplot_trotter_y.tex"

set title "Geodesic and Lie-Trotter-Suzuki Product Formula"
splot 'Tabs/tab_curve_comppi_3.dat' using 1:2:3 with lines lw 2, 'Tabs/tab_curve_comppi_3.dat' using 4:5:6 with lines lw 2

# Plot der Geodesic in klein
set term cairolatex pdf size 6cm,6cm color colortext font ",11"

set xlabel ""
set ylabel ""
set zlabel ""

set arrow from -0.2,0,0 to 0.5,0,0 nohead lc rgb 'black' lw 2  # X-axis arrow
set arrow from 0,0,0 to 0,0.8,0 nohead lc rgb 'black' lw 2 # Y-axis arrow
set arrow from 0,0,0 to 0,0,0.7 nohead lc rgb 'black' lw 2  # Z-axis arrow
set label 'X' at 0.6,0,0 center
set label 'Y' at 0,1.1,0 center
set label 'Z' at 0,0,0.8 center

unset grid
unset border
set view equal xyz
set ticslevel 0
set notics

set xrange [-0.2:0.5]
set yrange [0:0.9]
set zrange [0:0.7]

set lmargin at screen 0.2  # Left margin
set rmargin at screen 1.2  # Right margin
set tmargin at screen 0.90  # Top margin
set bmargin at screen 0.2  # Bottom margin

set nokey

set output "Figures/gnuplot_trotter_y_small.tex"

set title "Geodesic and Lie-Trotter-Suzuki Product Formula"
splot 'Tabs/tab_curve_comppi_3.dat' using 1:2:3 with lines lw 2, 'Tabs/tab_curve_comppi_3.dat' using 4:5:6 with lines lw 2
