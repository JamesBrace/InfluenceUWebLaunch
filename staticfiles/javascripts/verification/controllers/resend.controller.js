/**
 * Created by jamesbrace on 2017-02-05.
 */

/**
* Resend controller
* @namespace verification.controllers
*/
(function () {
  'use strict';

  angular
    .module('verification.controllers')
    .controller('ResendController', ResendController);

  ResendController.$inject = ['$location', '$scope', 'Verification'];

  /**
  * @namespace ResendController
  */
  function ResendController($location, $scope, Verification) {
    var vm = this;

    vm.resend = resend;
    vm.reset = reset;
    vm.sending = false;
    vm.message_success = null;
    vm.message_fail = null;
    vm.sent = false;
    vm.success=false;
    vm.fail=false;

    activate();

        /**
         * @name activate
         * @desc Actions to be performed when this controller is instantiated
         * @memberOf verification.controllers.VerificationController
         */
    function activate() {

        // If the user is not registered, they should not be here.
        if (!Verification.isRegistered()) {
            $location.url('/register');
        }

        // if the user is not logged in, they should not be here.
        if (!Verification.isAuthenticated()) {
            $location.url('/redirect');
        }
    }

    function reset() {
        vm.sending = false;
        vm.message_success = null;
        vm.message_fail = null;
        vm.sent = false;
        vm.success=false;
        vm.fail=false;
    }

  /**
    * @name register
    * @desc Register a new user
    * @memberOf verification.controllers.RegisterController
    */
    function resend() {
        vm.sending = true;
        Verification.resend(function (response) {
            if(response){
                vm.sending = false;
                vm.sent = true;
                if(response.success == true){
                    vm.success=true;
                    vm.message_success = response.message;
                }
                else{
                    vm.fail=true;
                    vm.message_fail = response.message;
                }
            }
        });
    }
  }
})();