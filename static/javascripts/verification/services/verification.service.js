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
        isAuthenticated: isAuthenticated,
        resend: resend,
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
    function register(first_name, last_name, email, password, confirm_password, callback) {
        return $http.post('/api/v1/accounts/', {
            first_name: first_name,
            last_name: last_name,
            email: email,
            password: password,
            confirm_password: confirm_password,
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

    // /**
    // * @name resend
    // * @desc Try to resend verification email
    // * @param {string} email address of user
    // * @returns {Promise}
    // * @memberOf verification.services.Verification
    // */
    // function recaptcha(token) {
    //   return $http.post('https://www.google.com/recaptcha/api/siteverify', {
    //     secret: '6LeYYRQUAAAAAAwClb2avgMj9zPLisORmOsDvgSW',
    //     response: token
    //   }).then(verifySuccessFn, verifyErrorFn);
    //
    //     /**
    //      * @name verifySuccessFn
    //      * @desc Take to options page
    //      */
    //     function verifySuccessFn(data, status, headers, config) {
    //         window.location.reload();
    //     }
    //
    //     /**
    //      * @name verifyErrorFn
    //      * @desc Log "Epic failure!" to the console and notifies user
    //      */
    //     function verifyErrorFn(data, status, headers, config) {
    //         console.error('Verification failure!');
    //         notify(data.data);
    //     }
    // }
    //
    // ////////////////////
    //
    // /**
    // * @name verify
    // * @desc Try to verify a raffle entry
    // * @param {string} verification code received by SMS
    // * @returns {Promise}
    // * @memberOf verification.services.Verification
    // */
    // function verify(code) {
    //   var data = getRegisteredUser();
    //   var email = data.email;
    //
    //   return $http.post('/api/v1/verify/', {
    //     email: email,
    //     verification_code: code
    //   }).then(verifySuccessFn, verifyErrorFn);
    //
    //     /**
    //      * @name verifySuccessFn
    //      * @desc Take to options page
    //      */
    //     function verifySuccessFn(data, status, headers, config) {
    //         $cookies.putObject('verifiedUser', data.data);
    //         window.location = '/options';
    //     }
    //
    //     /**
    //      * @name verifyErrorFn
    //      * @desc Log "Epic failure!" to the console and notifies user
    //      */
    //     function verifyErrorFn(data, status, headers, config) {
    //         console.error('Verification failure!');
    //         notify(data.data);
    //     }
    // }

    ////////////////////

    /**
    * @name verifyEmail
    * @desc Try to verify a raffle entry
    * @param {string} email
    * @returns {Promise}
    * @memberOf verification.services.Verification
    */
    function verifyEmail(email) {

      return $http.post('/api/v1/verifyemail/', {
        email: email,
      }).then(verifyEmailSuccessFn, verifyEmailErrorFn);

        /**
         * @name verifySuccessFn
         * @desc Take to options page
         */
        function verifyEmailSuccessFn(data, status, headers, config) {
            $cookies.putObject('registeredUser', data.data);
            window.location = '/verify';
        }

        /**
         * @name verifyErrorFn
         * @desc Log "Epic failure!" to the console and notifies user
         */
        function verifyEmailErrorFn(data, status, headers, config) {
            console.error('Verification failure!');
            notify(data.data);
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

        if (!$cookies.get('AuthenticatedAccount')){
            return;
        }

        return $cookies.getObject('AuthenticatedAccount');
    }

    /**
     * @name isRegistered
     * @desc Check if the current user is registered
     * @returns {boolean} True is user is registered, else false.
     * @memberOf verification.services.Verification
     */
    function isAuthenticated() {
        // return !!getAuthenticatedAccount();
        return true;
    }
  }
})();