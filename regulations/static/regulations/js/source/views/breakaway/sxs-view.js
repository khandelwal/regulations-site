define('sxs-view', ['jquery', 'underscore', 'backbone', './sxs-model', 'breakaway-events', 'main-events', './regs-router'], function($, _, Backbone, SxSModel, BreakawayEvents, MainEvents, Router) {
    'use strict';

    var SxSView = Backbone.View.extend({
        el: '#breakaway-view',

        events: {
            'click .sxs-back-button': 'remove',
            'click .footnote-jump-link': 'footnoteHighlight',
            'click .return-link': 'removeHighlight'
        },

        initialize: function() {
            var render;
            this.externalEvents = BreakawayEvents;

            // the sxs header wasn't always displaying properly when
            // loaded by ajax. it was because the css transition and 
            // having position: fixed on the header did not play
            // nicely. we add positioning after the transition is done.
            // also, the content was jumping as the header was taken
            // out of the DOM flow by being fixed position, so we
            // balance that out to prevent a jump
            this.el.addEventListener('transitionend', function() {
                var $header  = this.$el.find('.sxs-header');
                $header.css('position', 'fixed');
                this.$el.find('.sxs-content').css('margin-top', '0');
            }.bind(this), true);

            // callback to be sent to model's get method
            // called after ajax resolves sucessfully
            render = function(success, returned) {
                if (success) {
                    this.render(returned);
                }
                else {
                    this.render('<div class="error"><span class="minicon-warning"></span>Due to a network error, we were unable to retrieve the requested information.</div>'); 
                }

                this.$el.addClass('open-sxs');
            }.bind(this);

            SxSModel.get(this.options.url, render),

            this.listenTo(this.externalEvents, 'sxs:close', this.remove);

            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Router.hasPushState === false) {
                this.events = {};
            }
        },

        render: function(analysis) {
            this.$el.html(analysis);
        },

        footnoteHighlight: function(e) {
            var target = $(e.target).attr('href');
            // remove existing highlight
            this.removeHighlight();
            // highlight the selected footnote
            $('.footnotes ' + target).toggleClass('highlight');
        },

        removeHighlight: function() {
            $('.footnotes li').removeClass('highlight');
        },

        remove: function(e) {
            if (typeof e !== 'undefined') {
                e.preventDefault();
                window.history.back();
            }

            this.$el.removeClass('open-sxs');
            this.$el.html('');
            this.stopListening();
            this.$el.off();
            return this;
        }
    });

    return SxSView;
});
