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
    }).when('0caae4fd7d905316ac58cdcb5dd04600', {
      templateUrl: '/static/templates/verification/activated.html',
      controller: 'VerifyController',
      controllerAs: 'vm'
    }).when('/success', {
      controller: 'ResendController',
      controllerAs: 'vm',
      templateUrl: '/static/templates/verification/success.html'
    });
  }
})();