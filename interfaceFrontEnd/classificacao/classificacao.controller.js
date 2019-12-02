angular.module("classificacaoApp")
.controller("classificacaoController", function ($scope, classificacaoService) {
    $scope.codeImagemClassificada = classificacaoService.getImageClassificada();
});
