function ufetch_debian -d "A simple screenfetch alternative (Debian)"
	# 1. System Info
	set -l user_host "$USER@"(hostname)
	set -l distro Debian

	# Use Fish's native string replace (with -- to prevent flag confusion)
	set -l kernel_val (uname -sr | string replace -r -- '-.*' '')
	set -l uptime_val (uptime -p | string replace 'up ' '')

	# Use dpkg-query instead of dpkg -l so we don't accidentally count the 5 table headers
	set -l packages (dpkg-query -W 2>/dev/null | wc -l | string trim)

	# Shell
	set -l shell_val (basename $SHELL)

	# 2. Window Manager / Desktop Environment Detection
	set -l envtype
	set -l wm_val

	if set -q WM; and test -n "$WM"
		set envtype WM
		set wm_val $WM
	else if set -q XDG_CURRENT_DESKTOP; and test -n "$XDG_CURRENT_DESKTOP"
		set envtype DE
		set wm_val $XDG_CURRENT_DESKTOP
	else if set -q DESKTOP_SESSION; and test -n "$DESKTOP_SESSION"
		set envtype DE
		set wm_val $DESKTOP_SESSION
	else
		set envtype WM
		set wm_val (tail -n 1 ~/.xinitrc 2>/dev/null | cut -d ' ' -f 2)
	end

	# 3. Define Colors using Fish's built-in set_color
	set -l accent_color red # Debian defaults to red

	switch "$argv[1]"
		case --red
			set accent_color red
		case --yellow
			set accent_color yellow
		case --blue
			set accent_color blue
		case --magenta
			set accent_color magenta
		case --cyan
			set accent_color cyan
		case --green
			set accent_color green
	end

	set -l reset (set_color normal)
	set -l cbg (set_color -b $accent_color black) # accent background with color0 foreground
	set -l c1 (set_color $accent_color)

	# 4. Output ASCII Art (Backslashes are escaped)
	echo
	echo "  $cbg    _____    $reset$c1    USER       $reset$user_host"
	echo "  $cbg   /  __ \\   $reset$c1    DISTRO     $reset$distro"
	echo "  $cbg  |  /    |  $reset$c1    KERNEL     $reset$kernel_val"
	echo "  $cbg  |  \\___-   $reset$c1    UPTIME     $reset$uptime_val"
	echo "  $cbg  -_         $reset$c1    $envtype         $reset$wm_val"
	echo "  $cbg    --_      $reset$c1    SHELL      $reset$shell_val"
	echo "  $cbg             $reset$c1    PACKAGES   $reset$packages"
	echo
end
