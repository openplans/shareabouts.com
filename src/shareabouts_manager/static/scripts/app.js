/*globals Backbone jQuery Modernizr */

var Shareabouts = Shareabouts || {};

(function(NS, $) {
  'use strict';

  // App ======================================================================
  NS.app = new Backbone.Marionette.Application();

  NS.app.addRegions({
    mainRegion: '#page',
    overlayRegion: '#overlay-container'
  });

  NS.app.addInitializer(function(options){
    var datasetsCollection = new Backbone.Collection(NS.Data.datasets);

    NS.app.mainRegion.show(new NS.DataSetListView({
      collection: datasetsCollection
    }));
  });

  // Init =====================================================================
  $(function() {
    NS.app.start();
  });

}(Shareabouts, jQuery));