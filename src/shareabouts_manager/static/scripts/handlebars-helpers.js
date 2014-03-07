/*globals Handlebars jQuery window _ */

var Shareabouts = Shareabouts || {};

(function(NS, $) {
  'use strict';

  Handlebars.registerHelper('debug', function(obj) {
    return JSON.stringify(obj);
  });

  Handlebars.registerHelper('window_location', function() {
    return window.location.toString();
  });

  Handlebars.registerHelper('pretty_number', function(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  });


  Handlebars.registerHelper('select', function(value, options) {
    var $el = $('<div/>').html(options.fn(this)),
      selectValue = function(v) {
        $el.find('[value="'+v+'"]').attr({
          checked: 'checked',
          selected: 'selected'
        });
      };

    if (_.isArray(value)) {
      _.each(value, selectValue);
    } else {
      selectValue(value);
    }

    return $el.html();
  });

}(Shareabouts, jQuery));
