(function () {
  'use strict';

  angular
    .module('app', [
        'config',
        'routes',
        'verification',
        'notify'
    ])
    .run(run);

    /**
    * @name run
    * @desc Update xsrf $http headers to align with Django's defaults
    */
    function run($http) {
      $http.defaults.xsrfHeaderName = 'X-CSRFToken';
      $http.defaults.xsrfCookieName = 'csrftoken';
    }

    angular
        .module('notify', []);

    angular
        .module('routes', ['ngRoute']);

    angular
        .module('config', []);
})();