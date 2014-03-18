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

  Handlebars.registerHelper('percent_of', function(whole, part) {
    if (whole) {
      return Math.min(Math.max(part * 100 / whole, 0), 100);
    } else {
      return 0;
    }
  });

  Handlebars.registerHelper('first_of', function() {
    for (var i = 0; i < arguments.length; ++i) {
      if (arguments[i]) { return arguments[i]; }
    }
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
