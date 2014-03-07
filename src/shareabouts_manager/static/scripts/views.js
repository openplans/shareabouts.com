/*globals Backbone jQuery Handlebars Modernizr _ */

var Shareabouts = Shareabouts || {};

(function(NS, $) {
  'use strict';

    // Handlebars support for Marionette
  Backbone.Marionette.TemplateCache.prototype.compileTemplate = function(rawTemplate) {
    return Handlebars.compile(rawTemplate);
  };

  // View =====================================================================
  NS.ModalView = Backbone.Marionette.ItemView.extend({
    template: '#modal-tpl',
    className: 'overlay',
    ui: {
      closeBtn: '.btn-close'
    },
    events: {
      'click @ui.closeBtn': 'handleClose'
    },
    handleClose: function(evt) {
      evt.preventDefault();
      this.close();
    }
  });

  // NS.WelcomeModalView = NS.ModalView.extend({
  //   template: '#welcome-modal-tpl'
  // });

  NS.DataSetView = Backbone.Marionette.ItemView.extend({
    template: '#dataset-tpl',
    tagName: 'li',
    className: 'dataset clearfix'
  });

  NS.DataSetListView = Backbone.Marionette.CompositeView.extend({
    template: '#dataset-list-tpl',
    itemView: NS.DataSetView,
    itemViewContainer: '.dataset-list'
  });

}(Shareabouts, jQuery));