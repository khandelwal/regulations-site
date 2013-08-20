#vim: set encoding=utf-8
from django.views.generic.base import TemplateView

from regulations.generator import generator
from regulations.generator.html_builder import HTMLBuilder
from regulations.generator.node_types import EMPTYPART, REGTEXT
from regulations.views import utils
from regulations.views.partial import generate_html

class PartialSectionDiffView(TemplateView):
    """ A diff view of a partial section. """
    template_name = 'regulation-content.html'

    def get_context_data(self, **kwargs):
        context = super(PartialSectionDiffView, self).get_context_data(**kwargs)

        label_id = context['label_id']
        older = context['version']
        newer = context['newer_version']

        tree = generator.get_tree_paragraph(label_id, older)

        # Apply no layers
        appliers = utils.handle_specified_layers('', label_id, older)

        builder =  HTMLBuilder(*appliers)
        builder.tree = tree
        builder.generate_html()

        # Add a tree layer to account for subpart if this is regtext
        if builder.tree['node_type'] == REGTEXT:
            child_of_root = {
                'node_type': EMPTYPART,
                'children': [builder.tree]}
        context['tree'] = {'children': [child_of_root]}
        #context['navigation'] = self.section_navigation(
        #    context['label_id'], context['version'])
        return context