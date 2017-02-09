/**
 * LoginController
 * @namespace verification.controllers
 */
(function () {
    'use strict';

    angular
        .module('verification.controllers')
        .controller('LoginController', LoginController);

    LoginController.$inject = ['$location', '$scope', 'Verification', 'FlashService'];

    /**
     * @namespace LoginController
     */
    function LoginController($location, $scope, Verification, FlashService) {
        var vm = this;

        vm.login = login;

        vm.isSaving = false;
        vm.submitted = false;
        vm.message = null;


        activate();

        /**
         * @name activate
         * @desc Actions to be performed when this controller is instantiated
         * @memberOf verification.controllers.LoginController
         */
        function activate() {

            // if (Verification.isAuthenticated()) {
            //   $location.url('/verify');
            // }
        }

        /**
         * @name login
         * @desc Log the user in
         * @memberOf verification.controllers.LoginController
         */
        function login(isValid) {
            if (isValid) {
                vm.submitted = true;
                vm.isSaving = true;
                Verification.login(vm.email, vm.password, function (response) {
                    if (response) {
                        vm.dataLoading = false;
                        vm.submitted = false;
                        vm.isSaving = false;
                        FlashService.Error(response.message);
                    }
                }, false);
            }
            else {
                vm.submitted = false;
                vm.message = "There are still invalid fields below";
            }
        }


    }
})();