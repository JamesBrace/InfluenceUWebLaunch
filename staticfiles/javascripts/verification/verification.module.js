(function () {
  'use strict';

  angular
    .module('verification', [
      'verification.controllers',
      'verification.services'
    ]);

  angular
    .module('verification.controllers', []);

  angular
    .module('verification.services', ['ngCookies']);
})();
