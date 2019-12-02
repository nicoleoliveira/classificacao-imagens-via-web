angular
.module("classificacaoApp")
.controller("uploadController", ['$scope', 'FileUploader', '$cookies', '$window', '$http', 'classificacaoService',
function($scope, FileUploader, $cookies, $window, $http, classificacaoService) {

 $scope.uploader = new FileUploader({
  url: 'http://localhost:8000/imagemUpload/',
  method: 'post'
 });

 $scope.imageResponse = undefined;

 $scope.uploader.onCompleteItem = function(item, response, status, headers) {
    $scope.imageResponse = 'data:image/jpg;base64,'+ response.data.imagem;
    classificacaoService.setImageconvert(response.id, $scope.imageResponse);
    $window.location.href = '#!amostras';
};

}]);
