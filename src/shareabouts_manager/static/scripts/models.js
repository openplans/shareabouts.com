/*globals Backbone _ */

var Shareabouts = Shareabouts || {};

(function(NS) {
  'use strict';

  NS.DataSetModel = Backbone.Model.extend({
    initialize: function() {
      // Slug is used in the api, but it also editable. Cache it for the url
      // (see url() below) so we can modify it with the old slug after we have
      // already set the new one.

      // Set when constructed
      this.slug = this.get('slug');
      // Set when synced with the db
      this.on('sync', function() {
        this.slug = this.get('slug');
      });
    },
    url: function() {
      var base = _.result(this.collection, 'url');
      if (this.isNew()) {
        return base;
      }
      return base.replace(/([^\/])$/, '$1/') + encodeURIComponent(this.slug);
    }
  });

  NS.DataSetCollection = Backbone.Collection.extend({
    model: NS.DataSetModel,
    url: function() {
      return '/api/v2/' + NS.Data.username + '/datasets';
    },
    comparator: 'display_name'
  });

}(Shareabouts));
