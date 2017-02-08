(function(){'use strict';angular.module('verification.controllers').controller('RegisterController',RegisterController);RegisterController.$inject=['$location','$scope','Verification','FlashService'];function RegisterController($location,$scope,Verification,FlashService){var vm=this;vm.register=register;vm.isSaving=false;vm.submitted=false;activate();function activate(){if(Verification.isRegistered()){$location.url('/success');}}function register(isValid){if(isValid){vm.submitted=true;vm.isSaving=true;Verification.register(vm.full_name,vm.email,vm.password,function(response){if(response){vm.dataLoading=false;vm.submitted=false;vm.message=response.message;}});}else{vm.submitted=false;vm.message="There are still invalid fields below";}}}})();