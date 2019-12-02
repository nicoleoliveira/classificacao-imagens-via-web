angular.module('classificacaoApp').config(function ($routeProvider, $httpProvider) {
    $routeProvider.
    when('/upload', {
        templateUrl: 'upload/upload.view.html',
        controller: 'uploadController'
    }).
    when('/amostras', {
        templateUrl: 'amostras/amostras.view.html',
        controller: 'amostrasController'
    }).
    when('/classificacao', {
        templateUrl: 'classificacao/classificacao.view.html',
        controller: 'classificacaoController'
    }).
    otherwise({
        redirectTo: '/upload'
    })});
