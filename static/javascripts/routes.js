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
    $routeProvider.when('/', {
      controller: 'RegisterController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/verification/register.html'
    }).when('/activate/complete', {
      templateUrl: '/static/templates/verification/activated.html'
    }).when('/test', {
        templateUrl: '/static/templates/verification/login.html',
        controller: 'LoginController',
      controllerAs: 'vm'
    }).when('/success', {
      controller: 'ResendController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/verification/success.html'
    });
  }
})();