/*globals Backbone */

var Shareabouts = Shareabouts || {};

(function(NS) {
  'use strict';

  NS.DataSetModel = Backbone.Model.extend({
    idAttribute: 'slug'
  });

  NS.DataSetCollection = Backbone.Collection.extend({
    model: NS.DataSetModel,
    url: function() {
      return '/api/v2/' + NS.Data.username + '/datasets';
    },
    comparator: 'display_name'
  });

}(Shareabouts));
