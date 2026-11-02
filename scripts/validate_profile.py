#!/usr/bin/env python3
"""Validate profile markup and reproduce every SVG without third-party packages."""

import importlib.util
import re
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "profile_assets", ROOT / "scripts" / "generate_profile_assets.py"
)
assets = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(assets)

GENERATORS = {
    "hero": assets.hero,
    "stack": assets.stack,
    "flow": assets.flow,
    "connect": assets.footer,
    "hero-mobile": assets.hero_mobile,
    "stack-mobile": assets.stack_mobile,
    "flow-mobile": assets.flow_mobile,
    "connect-mobile": assets.footer_mobile,
}


def main() -> None:
    for theme in (assets.DARK, assets.LIGHT):
        for name, generate in GENERATORS.items():
            expected = generate(theme)
            for variant, content in [("", expected), ("-static", assets.static_variant(expected))]:
                path = ROOT / "assets" / f"{name}{variant}-{theme.name}.svg"
                source = path.read_text(encoding="utf-8")
                assert source == content, f"Stale artwork: {path.name}; regenerate it."
                root = ElementTree.fromstring(source)
                assert root.attrib["viewBox"] == (
                    f'0 0 {root.attrib["width"]} {root.attrib["height"]}'
                ), f"Invalid viewBox: {path.name}"
                assert "prefers-reduced-motion: reduce" in source, path.name
                if variant:
                    assert ".motion, .role { animation: none !important; }" in source
                assert "<script" not in source.lower(), path.name
                assert "foreignobject" not in source.lower(), path.name
                for element in root.iter():
                    for attribute, value in element.attrib.items():
                        if attribute.endswith("href"):
                            assert not value.startswith(("https:", "http:", "data:")), (
                                f"Remote SVG resource: {path.name}"
                            )
    for name in ("email", "linkedin", "github"):
        path = ROOT / "assets" / f"badge-{name}.svg"
        ElementTree.fromstring(path.read_text(encoding="utf-8"))

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for reference in re.findall(r'(?:srcset|src)="([^"]+)"', readme):
        if not reference.startswith("https://"):
            assert (ROOT / reference).is_file(), f"Missing image: {reference}"
    ids = set(re.findall(r'<a id="([^"]+)"', readme))
    for anchor in re.findall(r'href="#([^"]+)"', readme):
        assert anchor in ids, f"Broken section link: #{anchor}"
    for name in GENERATORS:
        assert readme.count(f"assets/{name}-dark.svg") == 1, name
        expected = 1 if name.endswith("-mobile") else 2  # desktop also has a fallback img
        assert readme.count(f"assets/{name}-light.svg") == expected, name
    assert readme.count("<picture>") == readme.count("</picture>") == 6
    assert readme.count("<table>") == readme.count("</table>") == 2
    print("PASS: 35 local SVGs, reproducible artwork, static alternatives, image paths, and section links.")


if __name__ == "__main__":
    main()
