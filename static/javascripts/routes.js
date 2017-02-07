/**
 * Created by jamesbrace on 2017-02-02.
 */
(function () {
  'use strict';

  angular
    .module('routes')
    .config(config);

  config.$inject = ['$routeProvider'];

  /**
  * @name config
  * @desc Define valid application routes
  */
  function config($routeProvider) {
    $routeProvider.when('/register', {
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/verification/register.html'
    }).when('/redirect', {
      templateUrl: '/static/templates/verification/redirect.html'
    }).when('/success', {
      controller: 'ResendController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/verification/success.html'
    });
  }
})();