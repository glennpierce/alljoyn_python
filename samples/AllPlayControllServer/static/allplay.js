var app = angular.module('AllPlayApp', ['checklist-model', 'rzModule'], function($interpolateProvider) {

    // set custom delimiters for angular templates
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});


app.controller('MainController', ['$rootScope', '$scope', '$http', '$timeout', '$interval', 
                                   function($rootScope, $scope, $http, $timeout, $interval) {

  $scope.volumeControls = [];

  $http({ cache: true, url: '/get_devices', method: 'GET'}).success(

      function (data, status, headers, config) {
         $scope.devices = data;

         for (i = 0; i < $scope.devices.length; i++) { 
          $scope.volumeControls.push({
            device_id: $scope.devices[i].id,
            name: $scope.devices[i].name,
            minValue: 0,
            maxValue: 100,
            value: $scope.devices[i].volume,
            options: {
              id: $scope.devices[i].id,
              floor: 0,
              ceil: 100,
              vertical: true,
              showTicksValues: false,
              onChange: function(id, value) {
                  
                  var parameters = {'device_id': id,
                                                 'volume': value};

                  var json_data = JSON.stringify(parameters);

                  return $http({cache: false, url: '/adjust_volume', method: 'post', data: json_data});
              },
            }
          }
          );
        };
      }
  );

  $scope.selected = [];
  $scope.uri = 'http://192.168.1.149:8882/static/test.mp3';

  $scope.devicesChanged = function() {
      var parameters = {'selected_devices': $scope.selected.devices};
      var json_data = JSON.stringify(parameters);
      $http({cache: false, url: '/create_zone', method: 'post', data: json_data});
  };

  $scope.run = function() {

      var parameters = {'selected_devices': $scope.selected.devices,
                                    'uri': $scope.uri};
      var json_data = JSON.stringify(parameters);
      return $http({cache: false, url: '/run', method: 'post', data: json_data});
   };

   $scope.stop = function() {

    return $http({cache: false, url: '/stop', method: 'get'});
   };

   $scope.pause = function() {
      return $http({cache: false, url: '/pause', method: 'get'});
   };

}]);
