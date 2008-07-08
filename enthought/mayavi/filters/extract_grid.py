"""This filter enables one to select a portion of, or subsample an
input dataset which may be a StructuredPoints, StructuredGrid or
Rectilinear.

"""
# Author: Prabhu Ramachandran <prabhu@aero.iitb.ac.in>
# Copyright (c) 2007, Enthought, Inc.
# License: BSD Style.

# Enthought library imports.
from enthought.traits.api import Instance, Int, Range
from enthought.traits.ui.api import View, Group, Item

from enthought.tvtk.api import tvtk

# Local imports
from enthought.mayavi.core.common import error
from enthought.mayavi.filters.filter_base import FilterBase
from enthought.mayavi.core.pipeline_info import PipelineInfo


######################################################################
# `ExtractGrid` class.
######################################################################
class ExtractGrid(FilterBase):
    """This filter enables one to select a portion of, or subsample an
    input dataset which may be a StructuredPoints, StructuredGrid or
    Rectilinear.
    """
    # The version of this class.  Used for persistence.
    __version__ = 0

    # Minimum x value.
    x_min = Range(value=0, low='_x_low', high='_x_high',
                  desc='minimum x value of the domain')

    # Maximum x value.
    x_max = Range(value=10000, low='_x_low', high='_x_high',
                  desc='maximum x value of the domain')

    # Minimum y value.
    y_min = Range(value=0, low='_y_low', high='_y_high',
                  desc='minimum y value of the domain')

    # Maximum y value.
    y_max = Range(value=10000, low='_y_low', high='_y_high',
                  desc='maximum y value of the domain')

    # Minimum z value.
    z_min = Range(value=0, low='_z_low', high='_z_high',
                  desc='minimum z value of the domain')

    # Maximum z value.
    z_max = Range(value=10000, low='_z_low', high='_z_high',
                  desc='maximum z value of the domain')

    # Sample rate in x.
    x_ratio = Range(value=1, low='_min_sample', high='_x_high',
                    desc='sample rate along x')

    # Sample rate in y.
    y_ratio = Range(value=1, low='_min_sample', high='_y_high',
                    desc='sample rate along y')

    # Sample rate in z.
    z_ratio = Range(value=1, low='_min_sample', high='_z_high',
                    desc='sample rate along z')

    # The actual TVTK filter that this class manages.
    filter = Instance(tvtk.Object, tvtk.ExtractVOI(), allow_none=False)

    input_info = PipelineInfo(datasets=['image_data',
                                        'rectilinear_grid',
                                        'structured_grid'],
                              attribute_types=['any'],
                              attributes=['any'])

    output_info = PipelineInfo(datasets=['image_data',
                                         'rectilinear_grid',
                                         'structured_grid'],
                               attribute_types=['any'],
                               attributes=['any'])

    ########################################
    # Private traits.

    # Determines the lower/upper limit of the axes for the sliders.
    _min_sample = Int(1)
    _x_low = Int(0)
    _x_high = Int(10000)
    _y_low = Int(0)
    _y_high = Int(10000)
    _z_low = Int(0)
    _z_high = Int(10000)

    ########################################
    # View related traits.
    
    # The View for this object.
    view = View(Group(Item(label='Select Volume Of Interest'),
                      Item(name='x_min'),
                      Item(name='x_max'),
                      Item(name='y_min'),
                      Item(name='y_max'),
                      Item(name='z_min'),
                      Item(name='z_max'),
                      Item('_'),
                      Item(label='Select Sample Ratio'),
                      Item(name='x_ratio'),
                      Item(name='y_ratio'),
                      Item(name='z_ratio'),
                      label='VOI'
                      ),
                Group(Item(name='filter', style='custom',
                           resizable=True),
                      show_labels=False,
                      label='Filter'),
                resizable=True,
                )

    ######################################################################
    # `object` interface
    ######################################################################
    def __get_pure_state__(self):
        d = super(ExtractGrid, self).__get_pure_state__()
        for axis in ('x', 'y', 'z'):
            for name in ('_min', '_max'):
                d.pop(axis + name, None)
            d.pop('_' + axis + '_low', None)
            d.pop('_' + axis + '_high', None)
            d.pop(axis + '_ratio', None)
        return d

    ######################################################################
    # `Filter` interface
    ######################################################################
    def update_pipeline(self):
        inputs = self.inputs
        if len(inputs) == 0:
            return

        input = inputs[0].outputs[0]
        mapping = {'vtkStructuredGrid': tvtk.ExtractGrid,
                   'vtkRectilinearGrid': tvtk.ExtractRectilinearGrid,
                   'vtkImageData': tvtk.ExtractVOI}

        for key, klass in mapping.iteritems():
            if input.is_a(key):
                self.filter = klass()
                break
        else:
            error('This filter does not support %s objects'%\
                  (input.__class__.__name__))
            return

        fil = self.filter
        fil.input = input
        fil.update_whole_extent()
        fil.update()
        self._set_outputs([fil.output])
        self._update_limits()
        self._update_voi()
        self._update_sample_rate()

    def update_data(self):
        """This method is invoked (automatically) when any of the
        inputs sends a `data_changed` event.
        """
        self._update_limits()
        fil = self.filter
        fil.update_whole_extent()
        fil.update()
        # Propagate the data_changed event.
        self.data_changed = True

    ######################################################################
    # Non-public methods.
    ######################################################################
    def _update_limits(self):
        extents = self.filter.input.whole_extent
        self._x_low, self._x_high = extents[:2]
        self._y_low, self._y_high = extents[2:4]
        self._z_low, self._z_high = extents[4:]
        
    def _x_min_changed(self, val):
        if val > self.x_max:
            self.x_max = val
        else:
            self._update_voi()

    def _x_max_changed(self, val):
        if val < self.x_min:
            self.x_min = val
        else:
            self._update_voi()

    def _y_min_changed(self, val):
        if val > self.y_max:
            self.y_max = val
        else:
            self._update_voi()

    def _y_max_changed(self, val):
        if val < self.y_min:
            self.y_min = val
        else:
            self._update_voi()

    def _z_min_changed(self, val):
        if val > self.z_max:
            self.z_max = val
        else:
            self._update_voi()

    def _z_max_changed(self, val):
        if val < self.z_min:
            self.z_min = val
        else:
            self._update_voi()

    def _x_ratio_changed(self):
        self._update_sample_rate()

    def _y_ratio_changed(self):
        self._update_sample_rate()

    def _z_ratio_changed(self):
        self._update_sample_rate()

    def _update_voi(self):
        f = self.filter
        f.voi = (self.x_min, self.x_max,
                 self.y_min, self.y_max,
                 self.z_min, self.z_max)
        f.update_whole_extent()
        f.update()

    def _update_sample_rate(self):
        f = self.filter
        f.sample_rate = (self.x_ratio, self.y_ratio, self.z_ratio)
        f.update_whole_extent()
        f.update()

    def _filter_changed(self, old, new):
        if old is not None:
            old.on_trait_change(self.render, remove=True)
        new.on_trait_change(self.render)
