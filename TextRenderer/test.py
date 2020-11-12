from bin.renderer import Renderer
Renderer = Renderer("resources/fonts/STIX2Math.otf", "resources/fonts/STIX2Text-Italic.otf")
Renderer.Render("\\sqrt(x)+10y", 0xFFFFFFFF, 64)
Renderer.Image("resources/images/output.png")
Renderer.Clear()
Renderer.Render("\\text[speed]", 0x0000FFFF, 256)
Renderer.Image("resources/images/output2.png")