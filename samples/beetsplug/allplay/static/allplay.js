var app = angular.module('AllPlayApp', ['checklist-model', 'rzModule'], function($interpolateProvider) {

    // set custom delimiters for angular templates
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});


app.directive("track", function() {
    return {
      restrict: 'E',
        templateUrl: '/track.html',
        replace: true,
        scope: {itemObject: "="}
    }
});

app.controller('MainController', ['$rootScope', '$scope', '$http', '$timeout', '$interval', 
                                   function($rootScope, $scope, $http, $timeout, $interval) {

  $scope.devices = [];

  $http({ cache: true, url: '/get_devices', method: 'GET'}).success(

      function (data, status, headers, config) {
        var devices = data['devices'];

         for (i = 0; i < devices.length; i++) { 
          $scope.devices.push({
            device_id: devices[i].id,
            name: devices[i].name,
            minValue: 0,
            maxValue: 100,
            value: devices[i].volume,
            options: {
              id: devices[i].id,
              floor: 0,
              ceil: 100,
              vertical: false,
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

  $http({ cache: true, url: '/tracks', method: 'GET'}).success(

      function (data, status, headers, config) {
         $scope.items = data['items'];
      }
  );

  $scope.selected = [];
  $scope.uri = 'http://192.168.1.149:8882/static/test.mp3';

  $scope.devicesChanged = function() {
      var parameters = {'selected_devices': $scope.selected.devices};
      var json_data = JSON.stringify(parameters);
      $http({cache: false, url: '/create_zone', method: 'post', data: json_data});
  };

  $scope.play = function() {

      var parameters = {'selected_devices': $scope.selected.devices,
                                    'uri': $scope.uri};
      var json_data = JSON.stringify(parameters);
      return $http({cache: false, url: '/play', method: 'post', data: json_data});
   };

   $scope.stop = function() {

    return $http({cache: false, url: '/stop', method: 'get'});
   };

   $scope.pause = function() {
      return $http({cache: false, url: '/pause', method: 'get'});
   };

   $scope.track_select = function(id) {
      var parameters = {'id': id};
      var json_data = JSON.stringify(parameters);
      return $http({cache: false, url: '/play', method: 'post', data: json_data});
   };


}]);
