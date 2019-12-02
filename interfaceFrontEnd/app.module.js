angular.module("classificacaoApp", [
    'ngResource',
    'ngCookies',
    'ngRoute',
    'sd.canvas-area-draw',
    'angularFileUpload'
]).run( function run( $http, $cookies ){

    // For CSRF token compatibility with Django
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.get('csrftoken');
});
