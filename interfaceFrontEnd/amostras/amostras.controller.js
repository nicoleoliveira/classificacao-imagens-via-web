angular.module("classificacaoApp")
    .controller("amostrasController", function ($scope, $rootScope, $location, classificacaoService, amostrasService) {
        $scope.points = [[]];
        $scope.labels = [];
        $scope.color = '';
        $scope.label = '';
        $scope.imageSrc = classificacaoService.getImageConvert();
        $scope.enabled = true;
        // $scope.colorArray = ['#FF0000', '#FFFF00', '#0000FF', '#008000', '#C0C0C0'];
        $scope.colorArray = [];
        $scope.activePolygon = 0;
        $scope.samples = [];
        $scope.colorPolygonActive = '';

        $scope.undo = function () {
            $scope.points[$scope.activePolygon].splice(-1, 1);
        };

        $scope.clearAll = function () {
            $scope.points[$scope.activePolygon] = [];
        };

        $scope.removePolygon = function (index) {
            $scope.points.splice(index, 1);
            if (index <= $scope.activePolygon) {
                --$scope.activePolygon;
            }
            if ($scope.points.length == 0) {
                $scope.enabled = false;
            }
        };

        $scope.add = function (index) {
            $scope.enabled = true;
            $scope.points.push([]);
            $scope.activePolygon = $scope.points.length - 1;
            $scope.samples.push(
                {
                    id: $scope.activePolygon,
                    label: $scope.label,
                    color: $scope.colorPolygonActive,
                    points: $scope.points[$scope.activePolygon - 1]
                }
            );
            $scope.label, $scope.colorPolygonActive = '';
        };

        $scope.classificar = function (samples) {
            if(samples.length > 0){
                const id = classificacaoService.getIdImage();
                data = {id: id, samples: samples};
                console.time('Tempo');
                amostrasService.formAmostras(data, function(imagem){
                    classificacaoService.setImageClassificada(imagem.id, imagem.imagem).then(
                        (resolve) => {
                            console.timeEnd('Tempo')
                            $rootScope.$apply(function () { $location.path('/classificacao'); });
                        }
                    );
                });
            }
        };
    });
