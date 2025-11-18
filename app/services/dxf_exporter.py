from __future__ import annotations

import ezdxf
from ezdxf.document import Drawing

from app.schemas.harness_design import Edge, HarnessDesign, Node


class DxfExporter:
    """Service for exporting harness designs to DXF."""

    LAYER_HARNESS = "HARNESS"
    LAYER_CONNECTOR = "CONNECTOR"
    LAYER_JIG = "JIG"
    LAYER_TEXT = "TEXT"
    JIG_HOLE_RADIUS = 1.5  # 3mm diameter

    def __init__(self, scale: float = 1.0):
        self.scale = scale
        self.doc = ezdxf.new()
        self.msp = self.doc.modelspace()
        self._setup_layers()

    def _setup_layers(self):
        """Create standard layers with distinct colors for the DXF."""
        self.doc.layers.add(self.LAYER_HARNESS, color=ezdxf.colors.WHITE)
        self.doc.layers.add(self.LAYER_CONNECTOR, color=ezdxf.colors.RED)
        self.doc.layers.add(self.LAYER_JIG, color=ezdxf.colors.YELLOW)
        self.doc.layers.add(self.LAYER_TEXT, color=ezdxf.colors.GREEN)

    def export_harness_design(self, design: HarnessDesign) -> Drawing:
        """
        Exports a complete harness design to a DXF document, including connectors,
        wires, and jigging information.
        """
        node_map = {node.id: node for node in design.nodes}

        for node in design.nodes:
            self._draw_connector(node)

        for edge in design.edges:
            source_node = node_map.get(edge.source)
            target_node = node_map.get(edge.target)
            if source_node and target_node:
                self._draw_wire(source_node, target_node, edge)

        return self.doc

    def _draw_connector(self, node: Node):
        """Draw a connector as a rectangle with its ID and jig holes."""
        if node.width is None or node.height is None:
            return  # Skip nodes without dimensions

        # Apply scaling to all coordinates and dimensions
        x = node.position["x"] * self.scale
        # Invert Y for typical CAD coordinate systems
        y = -node.position["y"] * self.scale
        width = node.width * self.scale
        height = node.height * self.scale

        # Draw the connector body
        points = [
            (x, y),
            (x + width, y),
            (x + width, y - height),
            (x, y - height),
            (x, y),  # Close the polyline
        ]
        self.msp.add_lwpolyline(points, dxfattribs={"layer": self.LAYER_CONNECTOR})

        # Add connector ID text
        text = self.msp.add_text(
            node.data.label,
            dxfattribs={
                "layer": self.LAYER_TEXT,
                "height": 5 * self.scale,
            },
        )
        text.dxf.insert = (x, y + 5 * self.scale)
        text.dxf.halign = ezdxf.const.LEFT
        text.dxf.valign = ezdxf.const.BOTTOM

        # Draw jig holes at the center of each side for positioning
        self._draw_jig_hole(x + width / 2, y)
        self._draw_jig_hole(x + width, y - height / 2)
        self._draw_jig_hole(x + width / 2, y - height)
        self._draw_jig_hole(x, y - height / 2)

    def _draw_wire(self, source_node: Node, target_node: Node, edge: Edge):
        """Draw a wire between two connectors and add a label."""
        if (
            source_node.width is None
            or source_node.height is None
            or target_node.width is None
            or target_node.height is None
        ):
            return  # Cannot draw wire if nodes are missing dimensions

        # Calculate center points of the nodes for wire connection
        source_x = (source_node.position["x"] + source_node.width / 2) * self.scale
        source_y = -(source_node.position["y"] + source_node.height / 2) * self.scale
        target_x = (target_node.position["x"] + target_node.width / 2) * self.scale
        target_y = -(target_node.position["y"] + target_node.height / 2) * self.scale

        # Draw the wire as a line
        self.msp.add_line(
            (source_x, source_y),
            (target_x, target_y),
            dxfattribs={"layer": self.LAYER_HARNESS},
        )

        # Add wire ID text at the midpoint of the wire
        mid_x = (source_x + target_x) / 2
        mid_y = (source_y + target_y) / 2
        text = self.msp.add_text(
            edge.data.wire_id,
            dxfattribs={
                "layer": self.LAYER_TEXT,
                "height": 3 * self.scale,
            },
        )
        text.dxf.insert = (mid_x, mid_y)
        text.dxf.halign = ezdxf.const.CENTER
        text.dxf.valign = ezdxf.const.MIDDLE

    def _draw_jig_hole(self, x: float, y: float):
        """Draw a standardized jig hole as a circle."""
        self.msp.add_circle(
            center=(x, y),
            radius=self.JIG_HOLE_RADIUS * self.scale,
            dxfattribs={"layer": self.LAYER_JIG},
        )
