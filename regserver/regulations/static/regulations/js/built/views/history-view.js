define("history-view",["jquery","underscore","backbone","dispatch"],function(e,t,n,r){var i=n.View.extend({el:"#history",initialize:function(){e(".status-list").removeClass("current"),this.$el.find(".status-list[data-base-version="+r.getVersion()+"]").addClass("current")}});return i});