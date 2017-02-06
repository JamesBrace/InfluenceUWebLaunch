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
        .controller('VerificationController', VerificationController);

    VerificationController.$inject = ['$location', '$scope', 'Verification'];

    function VerificationController($location, $scope, Verification) {
        var vm = this;

        vm.verify = verify;

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

        function verify(isValid) {
            if(isValid){
                Verification.verify(vm.verify_code);
            }
        }
    }
})();
