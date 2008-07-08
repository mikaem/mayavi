"""The base class for all objects in the MayaVi pipeline.  This class
basically abstracts out the common parts of the pipeline interface.

"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005-2008, Enthought, Inc.
# License: BSD Style.

# Enthought library imports.
from enthought.traits.api import List, Event, Bool, Instance

# Local imports.
from enthought.mayavi.core.base import Base
from enthought.mayavi.core.pipeline_info import PipelineInfo


######################################################################
# `PipelineBase` class.
######################################################################
class PipelineBase(Base):
    # The version of this class.  Used for persistence.
    __version__ = 0

    # A list of outputs for this object.
    outputs = List

    # The actors generated by this object that will be rendered on the
    # scene.  Changing this list while the actors are renderered *is*
    # safe and will do the right thing.
    actors = List

    # The optional list of actors belonging to this object.  These
    # will be added to the scene at an appropriate time.  Changing
    # this list while the widgets are renderered *is* safe and will do
    # the right thing.
    widgets = List

    # Information about what this object can consume.
    input_info = Instance(PipelineInfo)

    # Information about what this object can produce.
    output_info = Instance(PipelineInfo)

    ########################################
    # Events.
    
    # This event is fired when the pipeline has changed.
    pipeline_changed = Event

    # This event is fired when the data alone changes but the pipeline
    # outputs are the same.
    data_changed = Event

    ##################################################
    # Private traits.
    ##################################################
    # Identifies if `actors` and `widgets` are added to the `scene` or
    # not.
    _actors_added = Bool(False)

    # Stores the state of the widgets prior to disabling them.
    _widget_state = List

    ######################################################################
    # `object` interface.
    ######################################################################
    def __get_pure_state__(self):
        d = super(PipelineBase, self).__get_pure_state__()
        # These are setup dynamically so we should not pickle them.
        for x in ('outputs', 'actors', 'widgets', '_actors_added', ):
            d.pop(x, None)
        return d


    ######################################################################
    # `Base` interface
    ######################################################################
    def start(self):
        """This is invoked when this object is added to the mayavi
        pipeline.  Note that when start is invoked, all the other
        information for the pipeline should be already set.
        """
        if self.running:
            return

        # Add any actors.
        self.add_actors()

        # Call parent method to set the running state.
        super(PipelineBase, self).start()

    def stop(self):
        """Invoked when this object is removed from the mayavi
        pipeline.
        """
        if not self.running:
            return

        # Remove any of our actors from the scene.
        self.remove_actors()
        
        # Call parent method to set the running state.
        super(PipelineBase, self).stop()

    ######################################################################
    # `PipelineBase` interface.
    ######################################################################
    # Normally, you will not need to override the following methods
    # but you can if you really need to for whatever reason.
    def add_actors(self):
        """Adds `self.actors` to the scene.

        This is typically called when start is invoked.  You should
        avoid calling this unless you know what you are doing.
        """
        self.scene.add_actors(self.actors)
        self.scene.add_widgets(self.widgets)
        self._set_widget_visibility(self.widgets)
        self._actors_added = True

    def remove_actors(self):
        """Removes `self.actors` from the scene.

        This is typically called when stop is invoked.  You should
        avoid calling this unless you know what you are doing.
        """
        scene = self.scene
        scene.remove_actors(self.actors)
        scene.remove_widgets(self.widgets)
        self._actors_added = False

    ######################################################################
    # Non-public interface
    ######################################################################
    def _outputs_changed(self, new):
        self.pipeline_changed = True

    def _outputs_items_changed(self, list_event):
        self.pipeline_changed = True

    def _actors_changed(self, old, new):
        if self._actors_added:
            self.scene.remove_actors(old)
            self.scene.add_actors(new)
            self.scene.render()
            
    def _actors_items_changed(self, list_event):
        if self._actors_added:
            self.scene.remove_actors(list_event.removed)
            self.scene.add_actors(list_event.added)
            self.scene.render()

    def _widgets_changed(self, old, new):
        self._handle_widgets_changed(old, new)

    def _widgets_items_changed(self, list_event):
        self._handle_widgets_changed(list_event.removed, list_event.added)

    def _handle_widgets_changed(self, removed, added):
        if self._actors_added:
            scene = self.scene
            scene.remove_widgets(removed)
            scene.add_widgets(added)
            self._set_widget_visibility(added)
        
    def _scene_changed(self, old_scene, new_scene):
        if self._actors_added:
            old_scene.remove_actors(self.actors)
            old_scene.remove_widgets(self.widgets)
            new_scene.add_actors(self.actors)
            new_scene.add_widgets(self.widgets)
            self._set_widget_visibility(self.widgets)
    
    def _backup_widget_state(self):
        # store the enabled trait of the widgets
        # in the _widget_state list
        state = []
        for w in self.widgets:
            state.append(w.enabled)
            self._widget_state[:] = state
        
    def _restore_widget_state(self):
        if len(self._widget_state) != len(self.widgets):
            # someone has played with the widgets
            # we just enable all of them
            for w in self.widgets:
                w.enable = True
        else:
            for i in range(len(self.widgets)):
                self.widgets[i].enabled = self._widget_state[i]
            
    def _visible_changed(self,value):
        if value:
            # restore the state of the widgets from the 
            # backed up values.
            self._restore_widget_state()
        else:
            self._backup_widget_state()
            # disable all the widgets
            self._set_widget_visibility(self.widgets)

        # hide all actors
        for a in self.actors:
            a.visibility = value
       
        self.render()
        super(PipelineBase , self)._visible_changed(value)
        
    def _set_widget_visibility(self, widgets):
        if not self.visible:
            for widget in widgets:
                widget.enabled = False
