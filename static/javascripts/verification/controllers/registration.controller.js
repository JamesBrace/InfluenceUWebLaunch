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
    .controller('RegisterController', RegisterController);

  RegisterController.$inject = ['$location', '$scope', 'Verification', 'FlashService'];

  /**
  * @namespace RegisterController
  */
  function RegisterController($location, $scope, Verification, FlashService) {
    var vm = this;

    vm.register = register;
    vm.isSaving = false;
    vm.submitted = false;


    activate();

    /**
    * @name activate
    * @desc Actions to be performed when this controller is instantiated
    * @memberOf verification.controllers.RegisterController
    */
    function activate() {

      // If the user is registered, they should not be here.
      if (Verification.isRegistered()) {
        $location.url('/success');
      }
    }




    /**
    * @name register
    * @desc Register a new user
    * @memberOf verification.controllers.RegisterController
    */
    function register(isValid) {


        if (isValid) {
            vm.submitted = true;
            vm.isSaving = true;
            Verification.register(vm.full_name, vm.email, vm.password,
                function (response) {
                    if(response){
                        vm.dataLoading = false;
                        vm.submitted = false;
                        vm.message = response.message;
                    }
                });
        } else {
            vm.submitted = false;
            vm.message = "There are still invalid fields below";
        }
    }
}

})();
