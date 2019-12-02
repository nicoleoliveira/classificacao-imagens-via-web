angular.module('classificacaoApp').service('amostrasService', 
['$http', '$window', 'classificacaoService', function ($http, classificacaoService) {
    this.formAmostras = function (dataAmostras, callback) {
        const url = 'http://localhost:8000/amostras/';
        $http.post(url, dataAmostras)
        .then(
        function (response) {
            let data = response.data;
            callback(data);
        }, function (error) {
            let data = error.data;
            callback(null, data);
            
        });
    }
}]);