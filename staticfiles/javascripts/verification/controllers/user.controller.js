/**
 * UserController
 * @namespace verification.controllers
 */
(function () {
    'use strict';

    angular
        .module('verification.controllers')
        .controller('UserController', UserController);

    UserController.$inject = ['$location', '$scope', 'Verification', 'FlashService'];

    /**
     * @namespace UserController
     */
    function UserController($location, $scope, Verification, FlashService) {
        var vm = this;

        vm.update = update;

        vm.isSaving = false;
        vm.submitted = false;
        vm.message = null;
        vm.modal_message = null;

        vm.continue =false;

        vm.country = null;
        vm.phone = null;
        vm.gender = null;


        vm.object = {
            country:vm.country,
            phone:vm.phone,
            gender:vm.gender,
            size:vm.size,
            option:vm.option
        };


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
            if (!isValid) {
                vm.message = "There are still invalid fields below";
            }
            else{
                vm.modal_message=  "Make sure all the information you have submitted is correct! " +
                    "You will not be able to change your submission once you press \"Continue\" below. " +
                    "Once your profile has been submitted, you will be asked to verify your account with a code you" +
                    " will receive through SMS shortly after. NOTE: YOUR PHONE NUMBER MUST BE INPUTTED IN " +
                    " (555)555-5555 FORMAT OR YOU WILL NOT BE ABLE TO RECEIVE YOUR VERIFICATION TEXT"



                $scope.$watch( "vm.continue" , function(n,o){
                   if(n!=o) {
                       vm.submitted = true;
                       vm.isSaving = true;
                       vm.modal_message = "Updating your profile and sending SMS verification code...";

                       var new_phone = vm.country + vm.phone
                        console.log(new_phone);
                       Verification.update(vm.country, new_phone, vm.gender, vm.size, vm.option, function (response) {
                            if (response) {
                                vm.dataLoading = false;
                                vm.submitted = false;
                                vm.isSaving = false;
                                vm.modal_message = response.message;
                            }
                        });
                   }
               },true);
            }
        }
    }
})();