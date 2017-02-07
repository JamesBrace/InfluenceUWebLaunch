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

    // $scope.response = null;
    // $scope.widgetId = null;
    // $scope.model = {
    //     key: '6LeYYRQUAAAAAHWfUXonbgYyLu886SAzyq1H2oGE'
    // };
    // $scope.setResponse = function (response) {
    //     $scope.response = response;
    // };
    // $scope.setWidgetId = function (widgetId) {
    //     $scope.widgetId = widgetId;
    // };
    // $scope.cbExpiration = function() {
    //     vcRecaptchaService.reload($scope.widgetId);
    //     $scope.response = null;
    // };

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
      if (!Verification.isAuthenticated()){
        $location.url('/redirect');
      }
    }




    /**
    * @name register
    * @desc Register a new user
    * @memberOf verification.controllers.RegisterController
    */
    function register(isValid) {

        // var valid;
        // /**
        //  * SERVER SIDE VALIDATION
        //  *
        //  * You need to implement your server side validation here.
        //  * Send the reCaptcha response to the server and use some of the server side APIs to validate it
        //  * See https://developers.google.com/recaptcha/docs/verify
        //  */
        // console.log('sending the captcha response to the server', $scope.response);
        //
        //
        // valid = Verification.recaptcha(response);



        if (isValid && (vm.password == vm.confirm_password)) {
            vm.submitted = true;
            vm.isSaving = true;
            Verification.register(vm.first_name, vm.last_name, vm.email, vm.password, vm.confirm_password,
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
