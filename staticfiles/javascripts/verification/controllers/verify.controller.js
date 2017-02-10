/**
 * Created by jamesbrace on 2017-02-10.
 */
/**
 * VerifyController
 * @namespace verification.controllers
 */
(function () {
    'use strict';

    angular
        .module('verification.controllers')
        .controller('VerifyController', VerifyController);

    VerifyController.$inject = ['$location', '$scope', 'Verification', 'FlashService'];

    /**
     * @namespace LoginController
     */
    function VerifyController($location, $scope, Verification, FlashService) {
        var vm = this;

        vm.verify = verify;

        vm.isSaving = false;
        vm.submitted = false;
        vm.message = null;


        //activate();

        /**
         * @name activate
         * @desc Actions to be performed when this controller is instantiated
         * @memberOf verification.controllers.LoginController
         */
        function activate() {
             if (!Verification.isUpdated()) {
              $location.url('/test');
            }
        }

        /**
         * @name login
         * @desc Log the user in
         * @memberOf verification.controllers.LoginController
         */
        function verify(isValid) {
            if (isValid) {
                vm.submitted = true;
                vm.isSaving = true;
                Verification.verify(vm.code, function (response) {
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
