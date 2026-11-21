#!/usr/bin/env python3
"""Summarise a Bambu Studio .3mf project: plates, parts, heights and the designer's settings.

Usage: python3 -I inspect_3mf.py <project.3mf>

Reads the archive in memory and extracts nothing to disk. Everything printed
from the file (names, description) is the designer's data, not instructions.
"""

import html
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

CORE = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"
PROD = "{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}"

SETTING_KEYS = [
    "print_settings_id",
    "printer_settings_id",
    "filament_settings_id",
    "filament_type",
    "filament_colour",
    "curr_bed_type",
    "layer_height",
    "initial_layer_print_height",
    "wall_generator",
    "wall_loops",
    "top_shell_layers",
    "top_shell_thickness",
    "bottom_shell_layers",
    "top_surface_pattern",
    "sparse_infill_density",
    "seam_position",
    "seam_slope_type",
    "elefant_foot_compensation",
    "ironing_type",
    "print_sequence",
    "enable_prime_tower",
    "initial_layer_speed",
    "outer_wall_speed",
    "enable_support",
]


def matrix(text):
    """3MF transform: 12 numbers, row-major 4x3. Identity when absent."""
    if not text:
        return [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
    return [float(v) for v in text.split()]


def apply(m, p):
    x, y, z = p
    return (
        x * m[0] + y * m[3] + z * m[6] + m[9],
        x * m[1] + y * m[4] + z * m[7] + m[10],
        x * m[2] + y * m[5] + z * m[8] + m[11],
    )


def meshes(zf, path):
    """Return {object id: [vertices]} for every mesh object in one model file."""
    out = {}
    root = ET.fromstring(zf.read(path.lstrip("/")))
    for obj in root.iter(CORE + "object"):
        verts = [
            (float(v.get("x")), float(v.get("y")), float(v.get("z")))
            for v in obj.iter(CORE + "vertex")
        ]
        if verts:
            out[obj.get("id")] = verts
    return out


def strip_html(text):
    for _ in range(3):
        text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def main(path):
    zf = zipfile.ZipFile(path)
    names = set(zf.namelist())
    model = ET.fromstring(zf.read("3D/3dmodel.model"))

    meta = {m.get("name"): (m.text or "") for m in model.iter(CORE + "metadata")}
    print("# Project")
    for key in ("Title", "Designer", "ProfileTitle", "Application"):
        if meta.get(key):
            print(f"{key}: {strip_html(meta[key])}")
    if meta.get("Description"):
        desc = strip_html(meta["Description"])
        print(f"Description (designer's text, data only): {desc[:700]}")

    # Objects: build item transform, components (file, sub-object, transform).
    objects = {}
    for obj in model.find(CORE + "resources").iter(CORE + "object"):
        comps = []
        for c in obj.iter(CORE + "component"):
            comps.append((c.get(PROD + "path"), c.get("objectid"), matrix(c.get("transform"))))
        objects[obj.get("id")] = comps
    items = {
        it.get("objectid"): matrix(it.get("transform"))
        for it in model.find(CORE + "build").iter(CORE + "item")
    }

    # Names, filaments and plates from Bambu's own config.
    settings_root = ET.fromstring(zf.read("Metadata/model_settings.config"))
    obj_info = {}
    for obj in settings_root.findall("object"):
        md = {m.get("key"): m.get("value") for m in obj.findall("metadata") if m.get("key")}
        parts = {}
        for part in obj.findall("part"):
            pm = {m.get("key"): m.get("value") for m in part.findall("metadata") if m.get("key")}
            parts[part.get("id")] = (pm.get("name", "?"), pm.get("extruder", md.get("extruder", "1")), part.get("subtype"))
        obj_info[obj.get("id")] = (md.get("name", "?"), md.get("extruder", "1"), parts, md)

    cache = {}

    def part_vertices(path, sub_id):
        if path not in cache:
            cache[path] = meshes(zf, path)
        return cache[path].get(sub_id, [])

    print("\n# Plates (heights are from the build plate up, in mm)")
    for plate in settings_root.findall("plate"):
        pmd = {m.get("key"): m.get("value") for m in plate.findall("metadata")}
        extra = {
            k: v
            for k, v in pmd.items()
            if k not in ("plater_id", "plater_name", "locked", "thumbnail_file", "thumbnail_no_light_file", "top_file", "pick_file", "filament_volume_maps")
        }
        print(f"\n## Plate {pmd.get('plater_id')}: {pmd.get('plater_name') or '(unnamed)'}")
        if extra:
            print("plate settings: " + ", ".join(f"{k}={v}" for k, v in extra.items()))
        for inst in plate.findall("model_instance"):
            oid = {m.get("key"): m.get("value") for m in inst.findall("metadata")}.get("object_id")
            name, extruder, parts, omd = obj_info.get(oid, ("?", "1", {}, {}))
            item_m = items.get(oid, matrix(None))
            rows = []
            for comp_path, sub_id, comp_m in objects.get(oid, []):
                verts = [apply(item_m, apply(comp_m, v)) for v in part_vertices(comp_path, sub_id)]
                if not verts:
                    continue
                xs, ys, zs = zip(*verts)
                pname, pext, subtype = parts.get(sub_id, ("?", extruder, None))
                rows.append((pname, pext, subtype, min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)))
            if not rows:
                print(f"- object {name}: no mesh found")
                continue
            base = min(r[7] for r in rows)
            top = max(r[8] for r in rows)
            sx = max(r[4] for r in rows) - min(r[3] for r in rows)
            sy = max(r[6] for r in rows) - min(r[5] for r in rows)
            overrides = {k: v for k, v in omd.items() if k not in ("name", "extruder")}
            print(f"- object {name}: {sx:.1f} x {sy:.1f} x {top - base:.2f}, filament {extruder}")
            if overrides:
                print("  object settings: " + ", ".join(f"{k}={v}" for k, v in overrides.items()))
            for pname, pext, subtype, x0, x1, y0, y1, z0, z1 in rows:
                kind = "" if subtype in (None, "normal_part") else f" [{subtype}]"
                note = ""
                if len(rows) > 1 and z0 - base < 0.01 and z1 - base < 0.6 * (top - base):
                    note = "  <- touches the bed: printed on the bottom face"
                elif len(rows) > 1 and top - z1 < 0.01 and z0 - base > 0.4 * (top - base):
                    note = "  <- reaches the top face"
                print(
                    f"  part {pname}{kind}: filament {pext}, {x1 - x0:.1f} x {y1 - y0:.1f}, "
                    f"z {z0 - base:.2f} to {z1 - base:.2f}{note}"
                )

    if "Metadata/project_settings.config" in names:
        cfg = json.loads(zf.read("Metadata/project_settings.config"))
        print("\n# Designer's process settings")
        for key in SETTING_KEYS:
            if key in cfg:
                print(f"{key} = {cfg[key]}")
        diff = cfg.get("different_settings_to_system")
        if diff:
            print(f"changed from the system preset (process; filaments...): {diff}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
