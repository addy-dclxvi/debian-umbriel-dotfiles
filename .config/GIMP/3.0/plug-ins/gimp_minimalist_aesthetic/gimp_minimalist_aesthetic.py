#!/usr/bin/env python3

import sys, math, gi

gi.require_version('Gegl', '0.4')
gi.require_version("Gimp", "3.0")
gi.require_version('GimpUi', '3.0')
gi.require_version('Babl', '0.1')

from gi.repository import Gimp, GLib, Babl, Gegl, GObject, GimpUi

M = Gimp.LayerMode

PRESETS = [
    ("SAGE_TINT_VERY_SUBTLE", "Faint Sage Green Tint, Very Subtle [Lighten]",
     "Barely-there sage and warm cream tint. Original colors stay almost untouched.",
     dict(sat=-5, levels=(0.0, 1.0, 1.05, 0.0, 1.0),
          mid=("#7a9a7a", 12, M.SOFTLIGHT), highlight=("#f6efd8", 15, M.MULTIPLY),
          grain=(6, 15))),

    ("PASTEL_HAZE_LIGHT", "Soft Lavender and Pink Haze, Light [Lighten]",
     "Gentle lavender shadows and pale pink highlights with a little bloom.",
     dict(sat=-10, levels=(0.0, 0.99, 1.12, 0.03, 1.0),
          shadow=("#6a5a88", 20, M.SCREEN), highlight=("#fbe6ee", 30, M.MULTIPLY),
          bloom=(15, 0.02), grain=(6, 20))),

    ("GOLDEN_GLOW_LIGHT", "Warm Golden Hour Glow with Magenta Leak, Light [Lighten]",
     "Warm orange mid-tones, soft bloom and a magenta light leak from the top right.",
     dict(sat=-5, levels=(0.0, 1.0, 1.1, 0.03, 1.0),
          mid=("#f0a050", 20, M.SOFTLIGHT), leak=("#e0507a", 25, "radial"),
          bloom=(20, 0.03), grain=(6, 20))),

    ("FROST_BLUE_MEDIUM", "Cool Frost Blue Matte, Medium [Lighten]",
     "Icy blue shadows, pale highlights and a clean desaturated matte finish.",
     dict(sat=-30, levels=(0.0, 0.98, 1.1, 0.05, 0.98),
          shadow=("#1e3550", 40, M.SCREEN), highlight=("#e4f0fa", 50, M.MULTIPLY),
          mid=("#7aa4c8", 25, M.SOFTLIGHT), grain=(8, 25))),

    ("SAGE_FADE_MEDIUM", "Dusty Sage Grey-Green Fade, Medium [Lighten]",
     "Washed-out grey-green with lifted blacks and bone-white highlights.",
     dict(sat=-40, levels=(0.0, 0.97, 1.08, 0.07, 0.96),
          shadow=("#33463b", 45, M.SCREEN), highlight=("#ece6d6", 55, M.MULTIPLY),
          mid=("#8aa08a", 25, M.SOFTLIGHT),
          floor=("#2c3a31", 55, M.LIGHTEN_ONLY), ceiling=("#e6e2d4", 55, M.DARKEN_ONLY),
          grain=(8, 25))),

    ("SAND_PLASTER_MEDIUM", "Warm Sand Plaster Matte, Medium [Lighten]",
     "Sandy plaster tones with soft brown shadows and a lifted matte floor.",
     dict(sat=-40, levels=(0.0, 0.97, 1.1, 0.07, 0.95),
          shadow=("#4a3a30", 45, M.SCREEN), highlight=("#f4e6d2", 60, M.MULTIPLY),
          mid=("#d0b090", 25, M.SOFTLIGHT),
          floor=("#3a2e26", 55, M.LIGHTEN_ONLY), ceiling=("#efe2cf", 55, M.DARKEN_ONLY),
          bloom=(12, 0.02), grain=(8, 25))),

    ("FOG_HAZE_STRONG", "Foggy Grey Haze with Heavily Lifted Blacks, Strong [Lighten]",
     "Nearly monochrome cool grey haze. Blacks are lifted far above zero.",
     dict(sat=-65, levels=(0.0, 0.95, 1.2, 0.12, 0.94),
          shadow=("#546670", 60, M.SCREEN), highlight=("#f0f2f2", 70, M.MULTIPLY),
          floor=("#4a5a62", 80, M.LIGHTEN_ONLY), ceiling=("#eef0f0", 80, M.DARKEN_ONLY),
          bloom=(20, 0.03), grain=(6, 25))),

    ("PASTEL_DREAM_STRONG", "Dreamy Lavender and Rose Wash with Heavy Bloom, Strong [Lighten]",
     "Strongly lifted pastel look with heavy bloom and a purple-pink cast.",
     dict(sat=-30, levels=(0.0, 0.95, 1.25, 0.10, 1.0),
          shadow=("#5a4a78", 60, M.SCREEN), highlight=("#fbe6ee", 75, M.MULTIPLY),
          mid=("#cdb8e0", 35, M.SOFTLIGHT),
          floor=("#4d4560", 80, M.LIGHTEN_ONLY), ceiling=("#f8eef2", 70, M.DARKEN_ONLY),
          bloom=(30, 0.04), grain=(6, 25))),

    ("OLIVE_SHADOW_SUBTLE", "Gentle Olive Shadow Tint, Subtle [Darken]",
     "Slightly darker exposure with a faint olive tint in the shadows.",
     dict(sat=-10, levels=(0.02, 0.98, 0.92, 0.0, 1.0),
          shadow=("#2a3020", 20, M.SCREEN), mid=("#6a5a30", 15, M.SOFTLIGHT),
          vignette=15, grain=(8, 20))),

    ("TEAL_PLASTER_MEDIUM", "Teal Shadows with Plaster Highlights, Medium [Darken]",
     "Deep teal shadows and warm plaster highlights without flattening contrast.",
     dict(sat=-35, levels=(0.02, 0.97, 0.92, 0.0, 0.95),
          shadow=("#0c3a3c", 55, M.SCREEN), highlight=("#f0e4d0", 55, M.MULTIPLY),
          mid=("#2f6a62", 25, M.SOFTLIGHT),
          floor=("#0e2c2e", 60, M.LIGHTEN_ONLY), vignette=22, grain=(10, 30))),

    ("EARTH_TERRACOTTA_MEDIUM", "Muted Terracotta and Ochre Earth, Medium [Darken]",
     "Desaturated terracotta shadows and ochre mids with a warm matte floor.",
     dict(sat=-40, levels=(0.02, 0.97, 0.92, 0.06, 0.94),
          shadow=("#4a2a1c", 50, M.SCREEN), highlight=("#e8caa0", 60, M.MULTIPLY),
          mid=("#b0724e", 30, M.SOFTLIGHT),
          floor=("#2e1e16", 60, M.LIGHTEN_ONLY), ceiling=("#dcc8a8", 55, M.DARKEN_ONLY),
          grain=(12, 35))),

    ("SLATE_MATTE_MEDIUM", "Blue-Grey Slate Matte, Medium [Darken]",
     "Flat, architectural blue-grey with muted contrast and a soft vignette.",
     dict(sat=-50, levels=(0.02, 0.97, 0.95, 0.06, 0.93),
          shadow=("#1c2a38", 55, M.SCREEN), highlight=("#dde0e2", 60, M.MULTIPLY),
          mid=("#5a6c80", 25, M.SOFTLIGHT),
          floor=("#18222c", 75, M.LIGHTEN_ONLY), ceiling=("#d6d9db", 70, M.DARKEN_ONLY),
          vignette=28, grain=(10, 30))),

    ("UNDEREXPOSED_STRONG", "Underexposed Olive and Brown Film, Strong [Darken]",
     "Dark exposure with olive-brown shadows, heavy vignette and visible grain.",
     dict(sat=-30, levels=(0.04, 0.95, 0.80, 0.04, 0.92),
          shadow=("#1f2414", 55, M.SCREEN), highlight=("#d8c8a0", 65, M.MULTIPLY),
          mid=("#6a5a30", 35, M.SOFTLIGHT),
          floor=("#1c2012", 80, M.LIGHTEN_ONLY), vignette=50, grain=(14, 40))),

    ("CINEMATIC_STRONG", "Cyan and Tangerine Cinematic Split Tone, Strong [Darken]",
     "Strong cyan shadows against tangerine highlights with dramatic contrast.",
     dict(sat=-20, levels=(0.05, 0.95, 0.85, 0.04, 0.95),
          shadow=("#0b3a4a", 70, M.SCREEN), highlight=("#ffc080", 65, M.MULTIPLY),
          mid=("#1a6a7a", 30, M.OVERLAY),
          floor=("#0a2230", 80, M.LIGHTEN_ONLY), bloom=(14, 0.025),
          vignette=40, grain=(10, 35))),

    ("STEEL_CONCRETE_STRONG", "Cold Steel Concrete Grit, Strong [Darken]",
     "Nearly desaturated slate and steel blue with hard contrast and heavy grain.",
     dict(sat=-70, levels=(0.06, 0.94, 0.85, 0.05, 0.92),
          shadow=("#1a2430", 60, M.SCREEN), highlight=("#c8d2dc", 70, M.MULTIPLY),
          mid=("#64788c", 30, M.OVERLAY),
          floor=("#161c24", 85, M.LIGHTEN_ONLY), ceiling=("#cfd6dc", 75, M.DARKEN_ONLY),
          vignette=40, grain=(16, 45))),

    ("MOSS_NOIR_VERY_STRONG", "Near-Black Moss Green Noir, Very Strong [Darken]",
     "Almost black green shadows with pale lichen highlights and a heavy vignette.",
     dict(sat=-55, levels=(0.05, 0.93, 0.78, 0.03, 0.90),
          shadow=("#0c2418", 75, M.SCREEN), highlight=("#c8d4b8", 65, M.MULTIPLY),
          mid=("#2a5a40", 40, M.OVERLAY),
          floor=("#08160e", 90, M.LIGHTEN_ONLY), ceiling=("#c8d0bc", 75, M.DARKEN_ONLY),
          vignette=55, grain=(14, 40))),

    ("MATTE_FADE_SUBTLE", "Neutral Matte Film Fade, Subtle [Stylized]",
     "Keeps all colors and only lifts the blacks slightly for a soft matte feel.",
     dict(sat=-8, levels=(0.0, 0.99, 1.0, 0.04, 0.97),
          floor=("#1a1a1a", 35, M.LIGHTEN_ONLY), grain=(6, 15))),

    ("CONCRETE_FERN_MEDIUM", "Teal Shadows and Cream Highlights, Reference Style, Medium [Stylized]",
     "Matte teal-black shadows, creamy capped highlights and muted greens.",
     dict(sat=-35, levels=(0.03, 0.97, 1.0, 0.0, 1.0),
          shadow=("#0f2a2a", 55, M.SCREEN), highlight=("#f3e6d0", 65, M.MULTIPLY),
          mid=("#4f7f6f", 28, M.SOFTLIGHT),
          floor=("#0d2424", 75, M.LIGHTEN_ONLY), ceiling=("#e6dccb", 75, M.DARKEN_ONLY),
          bloom=(10, 0.02), vignette=12, grain=(10, 30))),

    ("POLAROID_STRONG", "Mint and Coral Polaroid with Red Edge Leak, Strong [Stylized]",
     "Mint shadows, coral highlights, faded blacks and a red leak along the left edge.",
     dict(sat=-22, levels=(0.03, 0.93, 1.05, 0.12, 0.92),
          shadow=("#3f8f78", 40, M.SCREEN), highlight=("#ffc8b8", 70, M.MULTIPLY),
          mid=("#e07060", 25, M.SOFTLIGHT),
          floor=("#2f4a42", 70, M.LIGHTEN_ONLY), ceiling=("#f4e6dc", 70, M.DARKEN_ONLY),
          leak=("#d83030", 30, "linear"), vignette=25, grain=(12, 40))),

    ("BW_CLEAN_LIGHT", "Clean Black and White, Light Grain [Neutral]",
     "Plain luminance black and white with gentle contrast and fine grain.",
     dict(mono=True, levels=(0.02, 0.98, 1.0, 0.02, 0.98),
          grain=(10, 25))),

    ("BW_FILM_HEAVY", "Contrasty Black and White, Vignette and Heavy Grain [Neutral]",
     "Punchy black and white with a strong vignette and coarse 35mm grain.",
     dict(mono=True, levels=(0.06, 0.94, 0.95, 0.04, 0.96),
          vignette=45, grain=(24, 55))),
]

PRESET_DATA = {identifier: params for identifier, _, _, params in PRESETS}

Effects = Gimp.Choice.new()
for index, (identifier, label, description, _) in enumerate(PRESETS):
    Effects.add(identifier, index, label, description)


class MinimalistAesthetic(Gimp.PlugIn):
    def do_query_procedures(self):
        return ["minimalist-aesthetic"]

    def do_create_procedure(self, name):
        proc = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            self.run,
            None
        )
        proc.set_image_types("*")
        proc.set_menu_label("Minimalist Aesthetic...")
        proc.add_menu_path("<Image>/Filters/Addy")
        proc.set_documentation("Applies diverse light and dark analog film aesthetics.",
                               "Split toning, matte floor and ceiling, bloom, leaks and grain.",
                               name)
        proc.set_attribution("Gemini", "Gemini", "2026")

        proc.add_choice_argument("effect",
                                 "Aesthetic Style",
                                 "Select the specific look and feel.",
                                 Effects,
                                 "SAGE_TINT_VERY_SUBTLE",
                                 GObject.ParamFlags.READWRITE)
        proc.add_double_argument("intensity",
                                 "Intensity",
                                 "Overall strength of the effect.",
                                 0.0, 100.0, 100.0,
                                 GObject.ParamFlags.READWRITE)
        return proc

    def run(self, procedure, run_mode, image, drawables, config, data):
        if run_mode == Gimp.RunMode.INTERACTIVE:
            GimpUi.init('minimalistaesthetic')
            dialog = GimpUi.ProcedureDialog(procedure=procedure, config=config)
            dialog.fill(['effect', 'intensity'])

            if not dialog.run():
                dialog.destroy()
                return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, None)
            dialog.destroy()

        image.undo_group_start()
        Gimp.context_push()

        effect = config.get_property('effect')
        intensity = config.get_property('intensity')
        preset = PRESET_DATA[effect]
        label = Gimp.Choice.get_label(Effects, effect)

        w = image.get_width()
        h = image.get_height()

        group = Gimp.GroupLayer.new(image, label)
        image.insert_layer(group, None, 0)
        group.set_opacity(float(intensity))

        Gimp.Selection.all(image)

        base = Gimp.Layer.new_from_visible(image, image, "Base Image")
        image.insert_layer(base, group, 0)

        if preset.get('mono'):
            base.desaturate(Gimp.DesaturateMode.LUMINANCE)
        else:
            base.hue_saturation(Gimp.HueRange.ALL, 0.0, 0.0, float(preset['sat']), 0.0)
        lo, hi, gamma, out_lo, out_hi = preset['levels']
        base.levels(Gimp.HistogramChannel.VALUE, lo, hi, True, gamma, out_lo, out_hi, True)

        if 'bloom' in preset:
            opacity, frac = preset['bloom']
            self.AddBloom(image, group, base, opacity, max(w, h) * frac)

        if 'mid' in preset:
            color, opacity, mode = preset['mid']
            self.AddColorLayer(image, group, "Mid Tone", w, h, color, opacity, mode)

        if 'shadow' in preset:
            color, opacity, mode = preset['shadow']
            self.AddColorLayer(image, group, "Shadow Tint", w, h, color, opacity, mode)

        if 'highlight' in preset:
            color, opacity, mode = preset['highlight']
            self.AddColorLayer(image, group, "Highlight Tint", w, h, color, opacity, mode)

        if 'leak' in preset:
            color, opacity, kind = preset['leak']
            self.AddLeak(image, group, w, h, color, opacity, kind)

        if 'vignette' in preset:
            self.AddVignette(image, group, w, h, preset['vignette'])

        if 'floor' in preset:
            color, opacity, mode = preset['floor']
            self.AddColorLayer(image, group, "Matte Floor", w, h, color, opacity, mode)

        if 'ceiling' in preset:
            color, opacity, mode = preset['ceiling']
            self.AddColorLayer(image, group, "Matte Ceiling", w, h, color, opacity, mode)

        if 'grain' in preset:
            amount, opacity = preset['grain']
            self.AddGrain(image, group, w, h, amount / 100.0, opacity)

        Gimp.Selection.none(image)
        Gimp.displays_flush()
        Gimp.context_pop()
        image.undo_group_end()

        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())

    def MakeColor(self, hexcode):
        return Gegl.Color.new(hexcode)

    def PrepareContext(self, hexcode, reverse=False):
        Gimp.context_set_opacity(100.0)
        Gimp.context_set_paint_mode(Gimp.LayerMode.NORMAL)
        Gimp.context_set_gradient_blend_color_space(Gimp.GradientBlendColorSpace.RGB_LINEAR)
        Gimp.context_set_gradient_reverse(reverse)
        Gimp.context_set_foreground(self.MakeColor(hexcode))
        Gimp.context_set_gradient_fg_transparent()

    def AddLayer(self, image, group, w, h, name, opacity, mode):
        layer = Gimp.Layer.new(image, name, w, h, Gimp.ImageType.RGBA_IMAGE, float(opacity), mode)
        image.insert_layer(layer, group, 0)
        layer.fill(Gimp.FillType.TRANSPARENT)
        return layer

    def AddColorLayer(self, image, group, name, w, h, hexcode, opacity, mode):
        layer = self.AddLayer(image, group, w, h, name, opacity, mode)
        self.PrepareContext(hexcode)
        layer.edit_fill(Gimp.FillType.FOREGROUND)
        return layer

    def AddLeak(self, image, group, w, h, hexcode, opacity, kind):
        layer = self.AddLayer(image, group, w, h, "Light Leak", opacity, M.SCREEN)
        self.PrepareContext(hexcode)
        if kind == "radial":
            layer.edit_gradient_fill(Gimp.GradientType.RADIAL, 0.0, False, 1, 0.0, True,
                                     w * 0.9, h * 0.1, w * 0.9 + w * 0.7, h * 0.1)
        else:
            layer.edit_gradient_fill(Gimp.GradientType.LINEAR, 0.0, False, 1, 0.0, True,
                                     0, 0, w * 0.4, 0)
        return layer

    def AddVignette(self, image, group, w, h, opacity):
        layer = self.AddLayer(image, group, w, h, "Vignette", opacity, M.MULTIPLY)
        self.PrepareContext("#05090a", reverse=True)
        radius = math.hypot(w, h) / 2.0
        layer.edit_gradient_fill(Gimp.GradientType.RADIAL, 0.0, False, 1, 0.0, True,
                                 w / 2.0, h / 2.0, w / 2.0 + radius * 0.95, h / 2.0)
        return layer

    def AddBloom(self, image, group, source, opacity, radius):
        layer = Gimp.Layer.new_from_drawable(source, image)
        image.insert_layer(layer, group, 0)
        layer.set_name("Optical Bloom")
        layer.set_mode(M.SCREEN)
        layer.set_opacity(float(opacity))
        blur = Gimp.DrawableFilter.new(layer, "gegl:gaussian-blur", "Gaussian Blur")
        config = blur.get_config()
        config.set_property('std-dev-x', float(radius))
        config.set_property('std-dev-y', float(radius))
        blur.update()
        layer.append_filter(blur)
        return layer

    def AddGrain(self, image, group, w, h, amount, opacity):
        layer = self.AddLayer(image, group, w, h, "Film Grain", opacity, M.OVERLAY)
        self.PrepareContext("#808080")
        layer.edit_fill(Gimp.FillType.FOREGROUND)
        noise = Gimp.DrawableFilter.new(layer, "gegl:noise-rgb", "Noise RGB")
        config = noise.get_config()
        config.set_property('correlated', True)
        config.set_property('independent', False)
        config.set_property('linear', False)
        config.set_property('gaussian', True)
        config.set_property('red', amount)
        config.set_property('green', amount)
        config.set_property('blue', amount)
        config.set_property('alpha', 0.0)
        noise.update()
        layer.append_filter(noise)
        return layer


Gimp.main(MinimalistAesthetic.__gtype__, sys.argv)
