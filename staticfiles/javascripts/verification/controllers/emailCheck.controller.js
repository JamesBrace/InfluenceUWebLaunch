/**
 * Created by jamesbrace on 2017-02-04.
 */
/**
 * Created by jamesbrace on 2017-02-02.
 */
/**
* Verification controller
* @namespace verification.controllers
*/
(function () {
  'use strict';

  angular
    .module('verification.controllers')
    .controller('EmailController', EmailController);

    EmailController.$inject = ['$location', '$scope', 'Verification'];

    /**
  * @namespace EmailController
  */
  function EmailController($location, $scope, Verification) {
        var vm = this;

        vm.verifyEmail = verifyEmail;

        activate();

        /**
         * @name activate
         * @desc Actions to be performed when this controller is instantiated
         * @memberOf verification.controllers.VerificationController
         */
        function activate() {
            var message = {
                status: 'success',
                message: 'Hello there!'
            };

            notify(message);

            // If the user is registered, they should not be here.
              if (Verification.isRegistered()) {
                $location.url('/verify');
              }
              if (!Verification.isAuthenticated()){
                $location.url('/redirect');
              }
        }

        function verifyEmail(isValid) {
            if(isValid){
                Verification.verifyEmail(vm.verify_email);
            }
        }
    }


})();