# draw.io Rules

Rules for creating and editing draw.io diagrams.

## Absolute Requirement

**Always export to PNG and visually verify after creating/editing.**

XML alone will miss issues. Always follow this flow:

```
1. Create/edit drawio file
2. Export to PNG
3. Load image and visually verify
4. Fix issues if found -> go to 2
5. Complete if no issues
```

## PNG Export Command

```powershell
powershell.exe -Command "& 'C:\Program Files\draw.io\draw.io.exe' --export --format png --output '<output_path>.png' '<input_path>.drawio'"
```

## Font Settings

| Setting | Required Value |
|---------|---------------|
| mxGraphModel | `defaultFontFamily="Meiryo"` |
| Each text element style | `fontFamily=Meiryo;` |
| Font size | 14px+ (titles 24px, body 14-16px) |

## Arrow Placement

| Rule | Reason |
|------|--------|
| Place at beginning of XML | Renders at back layer |
| Specify source/target explicitly | More reliable than auto-connect |
| Set exitX/exitY/entryX/entryY | Controls connection points |
| Specify points with Array | Explicitly controls path |

### Arrow Example

```xml
<mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeWidth=2;strokeColor=#666666;fontFamily=Meiryo;exitX=0.5;exitY=1;entryX=0.5;entryY=0;" parent="1" source="box1" target="box2" edge="1">
    <mxGeometry relative="1" as="geometry">
        <Array as="points">
            <mxPoint x="500" y="200"/>
        </Array>
    </mxGeometry>
</mxCell>
```

## Layout

| Rule | Value |
|------|-------|
| Arrow-to-label distance | 20px+ |
| Japanese text width | 30-40px per character |
| Box spacing | Vertical 40-60px, Horizontal 50-100px |
| Hierarchy spacing | 60-80px |

## Background/Page Settings

| Setting | Value |
|---------|-------|
| Background | None (transparent) |
| page | `page="0"` |

## XML Template

```xml
<mxfile host="65bd71144e">
    <diagram name="Diagram Name" id="unique-id">
        <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="0" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0" defaultFontFamily="Meiryo">
            <root>
                <mxCell id="0"/>
                <mxCell id="1" parent="0"/>

                <!-- ========== Arrows (back layer) ========== -->

                <!-- ========== Title ========== -->

                <!-- ========== Elements ========== -->

            </root>
        </mxGraphModel>
    </diagram>
</mxfile>
```

## Verification Checklist

After creating a diagram, verify:

- [ ] All text elements have `fontFamily=Meiryo;`
- [ ] Font size is sufficient (title 24px, body 14-16px)
- [ ] Arrows are at beginning of XML (back layer)
- [ ] Arrows and labels don't overlap
- [ ] Japanese text has no unintended line breaks
- [ ] **Exported to PNG and visually verified** (required)
- [ ] Hierarchy is clear
- [ ] Connections are correct

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Arrow position off | Explicitly set exitX/exitY/entryX/entryY |
| Arrow hidden behind element | Move arrow to beginning of XML |
| Text wrapping | Increase width (30-40px per Japanese char) |
| Font changed | Add fontFamily=Meiryo; to each element style |
| Connection point off | Explicitly set points with Array |
