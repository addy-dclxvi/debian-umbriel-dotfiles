-- sequence theme for neovim by addy
-- this theme follows terminal colorscheme
-- NOTE need different color for background, black (0), & gray (8)
-- NOTE need different color for foreground, white (7), & light-gray (15)

if vim.version().minor < 8 then
	vim.notify('Neovim 0.8+ is required for sequence colorscheme', vim.log.levels.ERROR, { title = 'Sequence colorscheme' })
	return
end

vim.api.nvim_command('hi clear')
if vim.fn.exists('syntax_on') then
	vim.api.nvim_command('syntax reset')
end

vim.g.VM_theme_set_by_colorscheme = true

-- Enforce terminal colors and cursorline
vim.o.termguicolors = false
vim.opt.cursorline = true
vim.g.colors_name = 'sequence'

local groups = {
	-- Interface & Base (Minimalist, blending with terminal background)
	Normal = { ctermfg = "NONE", ctermbg = "NONE" },
	NormalFloat = { ctermfg = "NONE", ctermbg = 0 },
	FloatBorder = { ctermfg = 8, ctermbg = "NONE" },
	FloatTitle = { ctermfg = 7, ctermbg = 0 },
	ColorColumn = { ctermbg = 0 },
	Cursor = { ctermfg = 8, ctermbg = 11 },
	CursorColumn = { ctermbg = 0 },
	CursorLine = { ctermbg = 0 },
	CursorLineNr = { ctermfg = 7, ctermbg = 0 }, 
	LineNr = { ctermfg = 8, ctermbg = "NONE" },
	Whitespace = { ctermfg = 8 },

	Directory = { ctermfg = 4 },
	ErrorMsg = { ctermfg = 1, bold = true },
	WinSeparator = { ctermfg = 8, ctermbg = "NONE" },
	VertSplit = { link = 'WinSeparator' },
	Folded = { ctermfg = 8, ctermbg = "NONE" },
	FoldColumn = { ctermbg = "NONE" },
	SignColumn = { ctermbg = "NONE" },

	MatchParen = { ctermfg = 3, underline = true },
	ModeMsg = { ctermfg = 3, bold = true },
	MoreMsg = { ctermfg = 4 },
	NonText = { ctermfg = 8 },
	Pmenu = { ctermfg = "NONE", ctermbg = 0 },
	PmenuSel = { ctermfg = 0, ctermbg = 7 },
	Question = { ctermfg = 4 },

	-- Forced foregrounds for readable highlights over comments
	Search = { ctermfg = 7, ctermbg = 8 },
	CurSearch = { ctermfg = 0, ctermbg = 11 },
	IncSearch = { ctermfg = 0, ctermbg = 11 },
	Visual = { ctermfg = 7, ctermbg = 8 },

	SpecialKey = { ctermfg = 8 },
	SpellCap = { ctermfg = 4, undercurl = true },
	SpellLocal = { ctermfg = 4, undercurl = true },
	SpellBad = { ctermfg = 1, undercurl = true },
	SpellRare = { ctermfg = 11, undercurl = true },

	-- Statusline backgrounds (Minimal default)
	StatusLine = { ctermfg = "NONE", ctermbg = "NONE" },
	StatusLineNC = { ctermfg = 8, ctermbg = "NONE" },

	-- Tabline (Blends with terminal background)
	WildMenu = { ctermfg = 0, ctermbg = 7 },
	TabLine = { ctermfg = 7, ctermbg = "NONE" },
	TabLineFill = { ctermfg = "NONE", ctermbg = "NONE" },
	TabLineSel = { ctermfg = "NONE", ctermbg = 8 },
	Title = { ctermfg = 3, bold = true },
	WarningMsg = { ctermfg = 11 },

	-- Core Syntax Highlights (Mapped strictly to Helix reference)
	Comment = { ctermfg = 7, italic = true }, 
	Constant = { ctermfg = 5 },
	Boolean = { ctermfg = 5 }, 
	Number = { ctermfg = 5 },
	String = { ctermfg = 2 },
	Identifier = { ctermfg = "NONE" }, 
	Function = { ctermfg = 11 },
	Statement = { ctermfg = 3 },
	Keyword = { ctermfg = 3 },
	Operator = { ctermfg = 3 },
	Exception = { ctermfg = 1 },
	PreProc = { ctermfg = 11 },
	Type = { ctermfg = 4 },
	Structure = { ctermfg = 4 },
	Special = { ctermfg = 3 },
	Delimiter = { ctermfg = "NONE" }, 
	Underlined = { underline = true },
	Ignore = { ctermfg = "NONE" },
	Error = { ctermfg = 1, bold = true },
	Todo = { ctermfg = 3, bold = true },
	Conceal = { ctermfg = 8 },

	-- Standard TOML Syntax Overrides (Forces tables to blue)
	tomlTable = { ctermfg = 4 },
	tomlTableArray = { ctermfg = 4 },
	tomlKey = { ctermfg = "NONE" },

	-- Diffs
	Added = { ctermfg = 2 },
	Removed = { ctermfg = 1 },
	Changed = { ctermfg = 6 },
	DiffAdd = { ctermfg = 2, ctermbg = "NONE" },
	DiffDelete = { ctermfg = 1, ctermbg = "NONE" },
	DiffChange = { ctermfg = 6, ctermbg = "NONE" },
	DiffText = { ctermbg = 8 },

	-- LSP Diagnostics
	DiagnosticError = { ctermfg = 1 },
	DiagnosticWarn = { ctermfg = 11 },
	DiagnosticInfo = { ctermfg = 4 },
	DiagnosticHint = { ctermfg = 4 },
	DiagnosticUnderlineError = { ctermfg = 1, undercurl = true },
	DiagnosticUnderlineWarn = { ctermfg = 11, undercurl = true },
	DiagnosticUnderlineInfo = { ctermfg = 4, undercurl = true },
	DiagnosticUnderlineHint = { ctermfg = 4, undercurl = true },
	DiagnosticUnnecessary = { ctermfg = 8 },
	DiagnosticDeprecated = { strikethrough = true },

	-- TreeSitter (Exact Helix mapping)
	['@type'] = { ctermfg = 4 },
	['@type.builtin'] = { ctermfg = 4 },
	['@constructor'] = { ctermfg = 2 },
	['@constant'] = { ctermfg = 5 },
	['@constant.builtin'] = { ctermfg = 5 }, 
	['@boolean'] = { ctermfg = 5 },
	['@number'] = { ctermfg = 5 },
	['@number.float'] = { ctermfg = 5 },
	['@string'] = { ctermfg = 2 },
	['@string.regexp'] = { ctermfg = 3 },
	['@string.special'] = { ctermfg = 6 },
	['@comment'] = { ctermfg = 8, italic = true },
	['@variable'] = { ctermfg = "NONE" },
	['@variable.builtin'] = { ctermfg = 6 },
	['@variable.member'] = { ctermfg = "NONE" },
	['@label'] = { ctermfg = 3 },
	['@punctuation.delimiter'] = { ctermfg = "NONE" },
	['@punctuation.bracket'] = { ctermfg = "NONE" },
	['@punctuation.special'] = { ctermfg = "NONE" },
	['@keyword'] = { ctermfg = 3 },
	['@keyword.control'] = { ctermfg = 11 },
	['@keyword.directive'] = { ctermfg = 11 },
	['@operator'] = { ctermfg = 3 },
	['@function'] = { ctermfg = 11 },
	['@function.macro'] = { ctermfg = 6 },
	['@tag'] = { ctermfg = 4 },
	['@tag.attribute'] = { ctermfg = 14 },
	['@module'] = { ctermfg = 4 },
	['@markup.heading'] = { ctermfg = 3, bold = true },
	['@markup.list'] = { ctermfg = 11 },
	['@markup.bold'] = { ctermfg = 3, bold = true },
	['@markup.italic'] = { ctermfg = 3, italic = true },
	['@markup.strikethrough'] = { strikethrough = true },
	['@markup.raw.block'] = { ctermfg = 3 },
	['@markup.link.url'] = { ctermfg = 4, underline = true },
	['@markup.link.text'] = { ctermfg = 11 },
	['@markup.link.label'] = { ctermfg = 2 },
	['@markup.quote'] = { ctermfg = 11 },

	-- TreeSitter TOML Specific Overrides
	['@property.toml'] = { ctermfg = "NONE" }, 
	['@label.toml'] = { ctermfg = 4 },         
	['@markup.heading.toml'] = { ctermfg = 4 },
	['@type.toml'] = { ctermfg = 4 },          
	['@variable.member.toml'] = { ctermfg = 4 },

	-- Telescope
	TelescopePromptBorder = { ctermfg = 8 },
	TelescopeResultsBorder = { ctermfg = 8 },
	TelescopePreviewBorder = { ctermfg = 8 },
	TelescopeSelection = { ctermfg = 7, ctermbg = 8 },

	-- Cmp / Completion
	CmpGhostText = { ctermfg = 8 },
	CmpItemAbbrMatch = { ctermfg = 3 },
	CmpItemAbbrMatchFuzzy = { ctermfg = 3 },
	CmpItemMenu = { ctermfg = 8 },

	-- Mini.nvim Core Modules
	MiniFilesTitleFocused = { ctermfg = "NONE", bold = true },
	MiniFilesBorder = { ctermfg = 8 },
	MiniFilesCursorLine = { ctermbg = 8 },
	MiniIconsAzure = { ctermfg = 6 },
	MiniIconsBlue = { ctermfg = 4 },
	MiniIconsCyan = { ctermfg = 14 },
	MiniIconsGreen = { ctermfg = 2 },
	MiniIconsGrey = { ctermfg = 7 },
	MiniIconsOrange = { ctermfg = 3 },
	MiniIconsPurple = { ctermfg = 5 },
	MiniIconsRed = { ctermfg = 1 },
	MiniIconsYellow = { ctermfg = 11 },
	MiniIndentscopeSymbol = { ctermfg = 8 },
	MiniIndentscopeSymbolOff = { ctermfg = 8 },
	MiniJump = { ctermfg = 1, bold = true, italic = true },
	MiniJump2dDim = { ctermfg = 8 },
	MiniStarterItemPrefix = { ctermfg = 3 },
	MiniStarterFooter = { link = 'Comment' },
	MiniSurround = { ctermbg = 8 },
	MiniTrailspace = { ctermbg = 1 },

	-- Mini.Statusline
	MiniStatuslineDevinfo = { ctermfg = 7, ctermbg = 0 },
	MiniStatuslineFileinfo = { ctermfg = 7, ctermbg = 0 },
	MiniStatuslineFilename = { ctermfg = 7, ctermbg = 0 }, 
	MiniStatuslineInactive = { ctermfg = 8, ctermbg = "NONE" },
	MiniStatuslineModeNormal = { ctermfg = 0, ctermbg = 4, bold = true },
	MiniStatuslineModeInsert = { ctermfg = 0, ctermbg = 2, bold = true },
	MiniStatuslineModeVisual = { ctermfg = 0, ctermbg = 3, bold = true },
	MiniStatuslineModeCommand = { ctermfg = 0, ctermbg = 5, bold = true },
	MiniStatuslineModeReplace = { ctermfg = 0, ctermbg = 1, bold = true },
	MiniStatuslineModeOther = { ctermfg = 0, ctermbg = 6, bold = true },

	-- Mini.Tabline (Matches Helix bufferline UI)
	MiniTablineCurrent = { ctermfg = "NONE", ctermbg = 8 },
	MiniTablineFill = { ctermfg = "NONE", ctermbg = "NONE" },
	MiniTablineHidden = { ctermfg = 7, ctermbg = "NONE" },
	MiniTablineModifiedCurrent = { ctermfg = 3, ctermbg = 8, bold = true },
	MiniTablineModifiedHidden = { ctermfg = 3, ctermbg = "NONE" },
	MiniTablineModifiedVisible = { ctermfg = 3, ctermbg = "NONE" },
	MiniTablineVisible = { ctermfg = 7, ctermbg = "NONE" },

	-- LSP Inlay Hints
	LspInlayHint = { ctermfg = 11, ctermbg = 0 },

	-- Snacks
	SnacksPickerDir = { link = 'Comment' },
	SnacksPickerPathHidden = { link = 'Comment' },
	SnacksPickerPathIgnored = { link = 'Comment' },
	SnacksPickerGitStatusUntracked = { link = 'Special' },
}

for group, parameters in pairs(groups) do
	vim.api.nvim_set_hl(0, group, parameters)
end
