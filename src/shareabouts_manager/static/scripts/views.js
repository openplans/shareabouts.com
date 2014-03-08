/*globals Backbone jQuery Handlebars Modernizr _ */

var Shareabouts = Shareabouts || {};

(function(NS, $) {
  'use strict';

    // Handlebars support for Marionette
  Backbone.Marionette.TemplateCache.prototype.compileTemplate = function(rawTemplate) {
    return Handlebars.compile(rawTemplate);
  };

  // View =====================================================================
  NS.DataSetFormModalView = Backbone.Marionette.ItemView.extend({
    template: '#dataset-form-modal-tpl',
    className: 'overlay',
    ui: {
      closeBtn: '.btn-close',
      form: 'form'
    },
    events: {
      'submit @ui.form': 'handleSubmit',
      'click @ui.closeBtn': 'handleClose'
    },
    save: function(data) {
      var self = this,
          saveFn;

      if (this.model) {
        saveFn = _.bind(this.model.save, this.model);
      } else {
        saveFn = _.bind(this.collection.create, this.collection);
      }

      saveFn(data, {
        wait: true,
        success: function() {
          self.close();
        },
        error: function() {
          window.alert('An error occurred. Dataset was not saved.');
        }
      });
    },
    handleSubmit: function(evt) {
      evt.preventDefault();
      this.save({
        display_name: this.ui.form.find('[name="display_name"]').val(),
        slug: this.ui.form.find('[name="slug"]').val(),
      });
    },
    handleClose: function(evt) {
      evt.preventDefault();
      this.close();
    }

  });

  NS.DataSetView = Backbone.Marionette.ItemView.extend({
    template: '#dataset-tpl',
    tagName: 'li',
    className: 'dataset clearfix',
    ui: {
      editBtn: '.edit-dataset-link'
    },
    events: {
      'click @ui.editBtn': 'handleEdit'
    },
    modelEvents: {
      'change': 'render'
    },
    handleEdit: function(evt) {
      evt.preventDefault();
      NS.app.overlayRegion.show(new NS.DataSetFormModalView({
        model: this.model
      }));
    }
  });

  NS.DataSetListView = Backbone.Marionette.CompositeView.extend({
    template: '#dataset-list-tpl',
    itemView: NS.DataSetView,
    itemViewContainer: '.dataset-list',
    ui: {
      newBtn: '.new-dataset-link'
    },
    events: {
      'click @ui.newBtn': 'handleNew'
    },
    handleNew: function(evt) {
      evt.preventDefault();
      NS.app.overlayRegion.show(new NS.DataSetFormModalView({
        collection: this.collection
      }));
    }
  });

}(Shareabouts, jQuery));