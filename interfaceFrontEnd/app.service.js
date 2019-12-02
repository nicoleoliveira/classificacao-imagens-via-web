angular
.module("classificacaoApp")
.service('classificacaoService', function() {
    var imageConvert = undefined;
    var imageClassificada = {id: null, imageSrc: null};

    var setImageconvert = function(id, src) {
        imageConvert = {id: id, imageSrc: src};
    };

    var setImageClassificada = (id, src) => {
        return new Promise ( (resolve, reject) => {
            imageClassificada = {id: id, imageSrc: src};
            if (imageClassificada) {
                resolve (imageClassificada);
            } else {
                reject (Error('Erro ao armazenar a imagem classificada.'));
            }
        });
    };
  
    var getImageConvert = function() {
        return imageConvert ? imageConvert.imageSrc: imageTemp;
    };

    var getImageClassificada = function() {
        return 'data:image/jpg;base64,' + imageClassificada.imageSrc;
    };

    var getIdImage = function() {
        return imageConvert.id;
    }
  
    return {
      setImageconvert: setImageconvert,
      getImageConvert: getImageConvert,
      setImageClassificada: setImageClassificada,
      getImageClassificada: getImageClassificada,
      getIdImage: getIdImage,
    };
  
  });
  