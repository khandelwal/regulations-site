// **Extends** Backbone.View
//
// **Usage** ```require(['toc-view'], function(TOCView) {})```
//
// **Jurisdiction** Expandable Table of Contents
define('toc-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'regs-helpers'], function($, _, Backbone, Dispatch, RegsHelpers) {
    'use strict';
    var TOCView = Backbone.View.extend({
        el: '#table-of-contents',

        events: {
            'click a': 'sendClickEvent'
        },

        initialize: function() {
            // **Event Listeners**
            // when the active section changes, highlight it in the TOC
            Dispatch.on('activeSection:change', this.setActive, this);

            Dispatch.on('openSection:set', this.setActive, this);

            // **TODO** need to work out a bug where it scrolls the content section
            // $('#menu-link:not(.active)').on('click', this.scrollToActive);
        },

        // update active classes, find new active based on the reg entity id in the anchor
        setActive: function(id) {
            this.$el.find('.current').removeClass('current');
            this.$el.find('a[data-section-id=' + RegsHelpers.findBaseSection(id) + ']').addClass('current');

            return this;
        },

        // **Event trigger**
        // when a TOC link is clicked, send an event along with the href of the clicked link
        sendClickEvent: function(e) {
            e.preventDefault();
            Dispatch.trigger('toc:click', $(e.currentTarget).data('section-id'));
        },

        // **Inactive** 
        // Intended to keep the active link in view as the user moves around the doc
        scrollToActive: function() {
            var activeLink = document.querySelectorAll('#table-of-contents .current');

            if (activeLink[0]) {
                activeLink[0].scrollIntoView();
            }
        }
    });

    return TOCView;
});
