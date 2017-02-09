/**
 * UserController
 * @namespace verification.controllers
 */
(function () {
    'use strict';

    angular
        .module('verification.controllers')
        .controller('UserController', UserController);

    LoginController.$inject = ['$location', '$scope', 'Verification', 'FlashService'];

    /**
     * @namespace UserController
     */
    function UserController($location, $scope, Verification, FlashService) {
        var vm = this;

        vm.update = update;

        vm.isSaving = false;
        vm.submitted = false;
        vm.message = null;


        activate();

        /**
         * @name activate
         * @desc Actions to be performed when this controller is instantiated
         * @memberOf verification.controllers.UserController
         */
        function activate() {

            if (!Verification.isAuthenticated()) {
                $location.url('/test');
            }
        }

        /**
         * @name update
         * @desc update the user info
         * @memberOf verification.controllers.UserController
         */
        function update(isValid) {
            if (isValid) {
                vm.submitted = true;
                vm.isSaving = true;
                Verification.update(vm.country, vm.phone, vm.gender, vm.size, vm.option, function (response) {
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