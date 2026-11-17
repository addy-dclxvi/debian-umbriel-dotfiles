function color_stick -d "Show the terminal colorscheme as blocks"
    # Standard colors (color0 - color7)
    set -l c0 "\e[30m" # Black
    set -l c1 "\e[31m" # Red
    set -l c2 "\e[32m" # Green
    set -l c3 "\e[33m" # Yellow
    set -l c4 "\e[34m" # Blue
    set -l c5 "\e[35m" # Magenta
    set -l c6 "\e[36m" # Cyan
    set -l c7 "\e[37m" # White

    # Bright colors (color8 - color15)
    set -l c8 "\e[90m" # Bright Black
    set -l c9 "\e[91m" # Bright Red
    set -l c10 "\e[92m" # Bright Green
    set -l c11 "\e[93m" # Bright Yellow
    set -l c12 "\e[94m" # Bright Blue
    set -l c13 "\e[95m" # Bright Magenta
    set -l c14 "\e[96m" # Bright Cyan
    set -l c15 "\e[97m" # Bright White

    set -l t "\e[0m" # Reset

    echo
    echo -e "  $c0██  $c1██  $c2██  $c3██  $c4██  $c5██  $c6██  $c7██$t"
    echo -e "  $c8██  $c9██  $c10██  $c11██  $c12██  $c13██  $c14██  $c15██$t"
    echo
end
