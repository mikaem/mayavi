"""
Metadata for all sources.
"""
# Author: Prabhu Ramachandran <prabhu@aero.iitb.ac.in>
# Copyright (c) 2008, Prabhu Ramachandran Enthought, Inc.
# License: BSD Style.

# Local imports.
from enthought.mayavi.core.metadata import SourceMetadata
from enthought.mayavi.core.pipeline_info import PipelineInfo

BASE = 'enthought.mayavi.sources'

open_3ds = SourceMetadata(
    id            = "3DSFile",
    class_name    = BASE + ".three_ds_importer.ThreeDSImporter",
    tooltip       = "Import a 3D Studio file",
    desc   = "Import a 3D Studio file",
    help   = "Import a 3D Studio file",
    menu_name        = "&3D Studio file",
    extensions = ['3ds'], 
    wildcard = '3D Studio files (*.3ds)|*.3ds',
    output_info = PipelineInfo(datasets=['none'],
                               attribute_types=['any'],
                               attributes=['any'])
)

open_image = SourceMetadata(
    id            = "ImageFile",
    class_name    = BASE + ".image_reader.ImageReader",
    menu_name     = "&Image file (PNG/JPG/BMP/PNM/TIFF)",
    tooltip       = "Import a PNG/JPG/BMP/PNM/TIFF image",
    desc   = "Import a PNG/JPG/BMP/PNM/TIFF image",
    extensions = ['png', 'jpg', 'jpeg', 'bmp', 'pnm', 'tiff'],
    wildcard = 'PNG files (*.png)|*.png|'\
               'JPEG files (*.jpg)|*.jpg|'\
               'JPEG files (*.jpeg)|*.jpeg|'\
               'BMP files (*.bmp)|*.bmp|'\
               'PNM files (*.pnm)|*.pnm|'\
               'TIFF files (*.tiff)|*.tiff',
    output_info = PipelineInfo(datasets=['image_data'],
                               attribute_types=['any'],
                               attributes=['any'])
)

open_plot3d = SourceMetadata(
    id            = "PLOT3DFile",
    class_name    = BASE + ".plot3d_reader.PLOT3DReader",
    menu_name     = "&PLOT3D file",
    tooltip       = "Open a PLOT3D data data",
    desc        = "Open a PLOT3D data data",
    help        = "Open a PLOT3D data data",
    extensions = ['xyz'],
    wildcard = 'PLOT3D files (*.xyz)|*.xyz',
    output_info = PipelineInfo(datasets=['structured_grid'],
                               attribute_types=['any'],
                               attributes=['any'])
)

open_vrml = SourceMetadata(
    id            = "VRMLFile",
    class_name    = BASE + ".vrml_importer.VRMLImporter",
    menu_name     = "V&RML2 file",
    tooltip = "Import a VRML2 data file",
    desc    = "Import a VRML2 data file",
    help    = "Import a VRML2 data file",
    extensions = ['wrl'],
    wildcard = 'VRML2 files (*.wrl)|*.wrl',
    output_info = PipelineInfo(datasets=['none'],
                               attribute_types=['any'],
                               attributes=['any'])
)

open_vtk = SourceMetadata(
    id            = "VTKFile",
    class_name    = BASE + ".vtk_file_reader.VTKFileReader",
    menu_name     = "&VTK file",
    tooltip = "Open a VTK data file",
    desc    = "Open a VTK data file",
    help    = "Open a VTK data file",
    extensions = ['vtk'],
    wildcard = 'VTK files (*.vtk)|*.vtk',
    output_info = PipelineInfo(datasets=['any'],
                               attribute_types=['any'],
                               attributes=['any'])
)

open_vtk_xml = SourceMetadata(
    id            = "VTKXMLFile",
    class_name    = BASE + ".vtk_xml_file_reader.VTKXMLFileReader",
    menu_name     = "VTK &XML file",
    tooltip = "Open a VTK XML data file",
    desc    = "Open a VTK XML data file",
    help    = "Open a VTK XML data file",
    extensions = ['xml', 'vti', 'vtp', 'vtr', 'vts', 'vtu', 
                  'pvti', 'pvtp', 'pvtr', 'pvts', 'pvtu'],
    wildcard = 'VTK XML files (*.xml)|*.xml|'\
               'Image Data (*.vti)|*.vti|'\
               'Poly Data (*.vtp)|*.vtp|'\
               'Rectilinear Grid (*.vtr)|*.vtr|'\
               'Structured Grid (*.vts)|*.vts|'\
               'Unstructured Grid (*.vtu)|*.vtu|'\
               'Parallel Image Data (*.pvti)|*.pvti|'\
               'Parallel Poly Data (*.pvtp)|*.pvtp|'\
               'Parallel Rectilinear Grid (*.pvtr)|*.pvtr|'\
               'Parallel Structured Grid (*.pvts)|*.pvts|'\
               'Parallel Unstructured Grid (*.pvtu)|*.pvtu',
    output_info = PipelineInfo(datasets=['any'],
                               attribute_types=['any'],
                               attributes=['any'])
)

parametric_surface = SourceMetadata(
    id            = "ParametricSurfaceSource",
    class_name    = BASE + ".parametric_surface.ParametricSurface",
    menu_name     = "&Create Parametric surface source",
    tooltip = "Create a parametric surface source",
    desc    = "Create a parametric surface source",
    help    = "Create a parametric surface source",
    extensions = [],
    wildcard = '',
    output_info = PipelineInfo(datasets=['poly_data'],
                               attribute_types=['any'],
                               attributes=['any'])
)

point_load = SourceMetadata(
    id            = "PointLoadSource",
    class_name    = BASE + ".point_load.PointLoad",
    menu_name     = "Create Point &load source",
    tooltip = "Simulates a point load on a cube of data (for tensors)",
    desc    = "Simulates a point load on a cube of data (for tensors)",
    help    = "Simulates a point load on a cube of data (for tensors)",
    extensions = [],
    wildcard = '',
    output_info = PipelineInfo(datasets=['image_data'],
                               attribute_types=['any'],
                               attributes=['any'])
)

# Now collect all the sources for the mayavi registry.
sources = [open_3ds, 
           open_image, 
           open_plot3d,
           open_vrml,
           open_vtk,
           open_vtk_xml,
           parametric_surface,
           point_load
          ]

