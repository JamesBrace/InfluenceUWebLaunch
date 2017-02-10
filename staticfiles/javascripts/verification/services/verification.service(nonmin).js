/**
 * Created by jamesbrace on 2017-02-02.
 */
/**
* Authentication
* @namespace InfluenceUApp.authentication.services
*/
(function () {
  'use strict';

  angular
    .module('verification.services')
    .factory('Verification', Verification);

  Verification.$inject = ['$cookies', '$http'];

  /**
  * @namespace Verification
  * @returns {Factory}
  */
  function Verification($cookies, $http) {
    /**
    * @name Authentication
    * @desc The Factory to be returned
    */
    var Verification = {
        register: register,
        getRegisteredUser: getRegisteredUser,
        isRegistered: isRegistered,
        resend: resend,
        login: login,
        isAuthenticated: isAuthenticated,
        getAuthenticatedAccount: getAuthenticatedAccount,
        isUpdated: isUpdated,
        getUpdatedUser: getUpdatedUser,
        setAuthenticatedAccount: setAuthenticatedAccount,
        update: update,
        verify: verify,
    };

    return Verification;

    ////////////////////


    /**
    * @name register
    * @desc Try to register a new user
    * @param {string} first_name The full name entered by the user
    * @param {string} last_name The phone_number entered by the user
    * @param {string} email The email entered by the user
    * @param {string} password The password entered by the user
    * @param {string} confirm_password
    * @param {function} callback function
    * @returns {Promise}
    * @memberOf verification.services.Verification
    */
    function register(first_name, email, password, callback) {
        return $http.post('/api/v1/accounts/', {
            full_name: first_name,
            email: email,
            password: password
        }).then(registerSuccessFn, registerErrorFn);

        /**
         * @name registerSuccessFn
         * @desc Take to code input page
         */
        function registerSuccessFn(data, status, headers, config) {

            $cookies.putObject('registeredUser', data.data);
            window.location = '/success';
        }

        /**
         * @name registerErrorFn
         * @desc Log "Epic failure!" to the console
         */
        function registerErrorFn(data, status, headers, config) {
            var response;
            response = { success: false, message: data.data.message };
            callback(response);
        }
    }

    ////////////////////

    /**
    * @name resend
    * @desc Try to resend verification email
    * @param {string} email address of user
    * @returns {Promise}
    * @memberOf verification.services.Verification
    */
    function resend(callback) {
      var cookie = getRegisteredUser();
      var email = cookie.email;
      console.log(email);
      return $http.post('/api/v1/resend/', {
        email: email
      }).then(resendSuccessFn, resendErrorFn);

        /**
         * @name resendSuccessFn
         * @desc Reload
         */
        function resendSuccessFn(data, status, headers, config) {
            var response;
            response = {success: true, message: "Successfully resent your email! Don't forget to check your spam folder!"};
            callback(response);
        }

        /**
         * @name resendErrorFn
         * @desc Log "Epic failure!" to the console and notifies user
         */
        function resendErrorFn(data, status, headers, config) {
            var response;
            response = {success: false, message: "Sorry something went wrong on our part! Try giving us call if you have any further issues"};
            callback(response);
        }
    }


    ////////////////////

      /**
       * @name login
       * @desc Try to login
       * @param {string} email address of user
       * @param {string} password of user
       * @param {function} callback function
       * @returns {Promise}
       * @memberOf verification.services.Verification
       */
      function login(email, password, callback) {
          return $http.post('/api/v1/auth/login/', {
              email: email,
              password: password
          }).then(function (data, status, headers, config) {
              Verification.setAuthenticatedAccount(data.data);
              window.location = '/user-info';
          }, function (response) {
              var response_;
              response_ = {success: false, message: response.data.message};
              callback(response_);
              console.error('Epic failure!');
          });
      }


      ////////////////////

      /**
       * @name update
       * @desc Try to update
       * @returns {Promise}
       * @memberOf verification.services.Verification
       */
      function update(country, phone, gender, size, option, callback) {
          var temp = getAuthenticatedAccount();
          var email = temp.email;
          console.log(email + " " + country + " " + phone + " " + gender + " " + size + " " + option);
          return $http.post('/api/v1/auth/update/', {
              email: email,
              country: country,
              phone: phone,
              gender: gender,
              size: size,
              option: option
          }).then(function (data, status, headers, config) {
                $cookies.remove('authenticatedAccount');
                $cookies.putObject('updatedAccount', email);
                window.location = '/verify';
          }, function (response) {
              var response_;
              response_ = {success: false, message: response.data.message};
              callback(response_);
              console.error('Epic failure!');
          });
      }

    ////////////////////

    /**
    * @name verifyEmail
    * @desc Try to verify a raffle entry
    * @param {string} email
    * @returns {Promise}
    * @memberOf verification.services.Verification
    */
    function verify(code) {
        var temp = getUpdatedUser();
        var email = temp;
        console.log(email);
      return $http.post('api/v1/auth/verifyphone/', {
        email: email,
        special_key: code,
      }).then(verifySuccessFn, verifyErrorFn);

        /**
         * @name verifySuccessFn
         * @desc Take to options page
         */
        function verifySuccessFn(data, status, headers, config) {
            $cookies.remove('updatedAccount');
            $cookies.putObject('success', data.data);
            window.location = '/complete';
        }

        /**
         * @name verifyErrorFn
         * @desc Log "Epic failure!" to the console and notifies user
         */
        function verifyErrorFn(data, status, headers, config) {
            var response_;
              response_ = {success: false, message: response.data.message};
              callback(response_);
              console.error('Epic failure!');
        }
    }

    /**
     * @name getRegisteredAccount
     * @desc Return the currently registered account
     * @returns {object|undefined} Account if registered, else `undefined`
     * @memberOf verification.services.Verification
     */
    function getRegisteredUser() {

        if (!$cookies.get('registeredUser')){
            return;
        }

        return $cookies.getObject('registeredUser');
    }


    function getUpdatedUser() {

        if (!$cookies.get('updatedAccount')){
            return;
        }

        return $cookies.getObject('updatedAccount');
    }

    function isUpdated() {
        return !!getUpdatedUser();
    }
    /**
     * @name isRegistered
     * @desc Check if the current user is registered
     * @returns {boolean} True is user is registered, else false.
     * @memberOf verification.services.Verification
     */
    function isRegistered() {
        return !!getRegisteredUser();
    }

      /**
     * @name getAuthenticatedAccount
     * @desc Return the currently authenticated account
     * @returns {object|undefined} Account if authenticated, else `undefined`
     * @memberOf verification.services.Verification
     */

    function getAuthenticatedAccount() {

          //console.log($cookies.getObject('authenticatedAccount'));
          if (!$cookies.get('authenticatedAccount')) {
            return;
        }

          return $cookies.getObject('authenticatedAccount');
          //return JSON.parse($cookies.authenticatedAccount);
    }
    /**
     * @name isAuthenticated
     * @desc Check if the current user is authenticated
     * @returns {boolean} True is user is authenticated, else false.
     * @memberOf verification.services.Verification
     */
    function isAuthenticated() {
        //console.log("account:" + getAuthenticatedAccount());

        return !!getAuthenticatedAccount();
    }

      /**
       * @name setAuthenticatedAccount
       * @desc Stringify the account object and store it in a cookie
       * @param {Object} user The account object to be stored
       * @returns {undefined}
       * @memberOf verification.services.Verification
       */

      function setAuthenticatedAccount(account) {

          $cookies.putObject('authenticatedAccount', account);
          //$cookies.authenticatedAccount = "authenticated";
          //console.log($cookies.getObject('authenticatedAccount'));
    }
  }
})();