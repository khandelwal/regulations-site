// Module called on app load, once doc.ready
//
// **TODO**: Consolidate/minimize module dependencies
//
// **Usage**: require(['app-init'], function(app) { $(document).ready(function() { app.init(); }) })
define(['jquery', 'underscore', 'backbone', 'content-view', 'reg-model', 'definition-view', 'sub-head-view', 'drawer-view', 'dispatch', 'sidebar-view', 'konami', 'header-view', 'analytics-handler', 'regs-helpers', './regs-router'], function($, _, Backbone, ContentView, RegModel, DefinitionView, SubHeadView, DrawerView, Dispatch, SidebarView, Konami, HeaderView, AnalyticsHandler, RegsHelpers, Router) {
    'use strict';
    return {
        // Temporary method. Recurses DOM and builds front end representation of content.
        // API should make this obsolete.
        getTree: function($obj) {
            var parent = this;
            $obj.children().each(function() {
                var $child = $(this),
                    cid = $child.attr('id'),
                    clist = $child.find('ol'),
                    $nextChild;

                RegModel.set({
                    'text': cid,
                    'content': $child.html()
                }); 

                if (typeof (cid, clist) !== 'undefined') {
                    $nextChild = clist ? $(clist) : $child;
                    parent.getTree($nextChild);
                }
            });
        },

        // Purgatory for DOM event bindings that should happen in a View
        bindEvents: function() {

            /* ssshhhhh */
            new Konami(function() {
                /* http://thenounproject.com/noun/hamburger/#icon-No17373 */
                /* http://thenounproject.com/noun/carrot/#icon-No7790 */
                document.getElementById('menu-link').className += ' hamburgerify';
                $('.inline-interpretation .expand-button').addClass('carrotify');
                $('#about-tool').html('Made with <span style="color: red"><3</span> by:');
                $('#about-reg').html('Find our brilliant attorneys at:');
            });
        },

        init: function() {
            var openSection,
                urlPrefix,
                regVersion,
                regSection = $('.main-content section[data-base-version]');

            // set open section and version for ajax calls
            openSection = regSection.attr('id');
            Dispatch.set('section', openSection);

            regVersion = regSection.data('base-version');
            Dispatch.set('version', regVersion);

            // init primary Views that require only a single instance
            window.Regs = {};
            window.Regs.subhead = new SubHeadView();
            window.Regs.drawer = new DrawerView();
            window.Regs.sidebar = new SidebarView();
            window.Regs.regContent = new ContentView();
            window.Regs.analytics = new AnalyticsHandler();
            window.Regs.mainHeader = new HeaderView();

            // cache URL prefix
            urlPrefix = RegsHelpers.findURLPrefix();
            if (urlPrefix) {
                Dispatch.set('urlprefix', urlPrefix);
            }
            Router.start();

            // cache open section content
            RegModel.set(openSection, regSection.html());

            this.bindEvents();
        }
    };
});
