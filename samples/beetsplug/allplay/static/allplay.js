var app = angular.module('AllPlayApp', ['ngRoute',
					'checklist-model',
                                        'rzModule', 
                                        'angularUtils.directives.dirPagination'], function($interpolateProvider) {

    // set custom delimiters for angular templates
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/showtracks', {
        templateUrl: '/showtracks.html',
        controller: 'MainController'
      }).
      when('/showqueue', {
        templateUrl: '/showqueue.html',
        controller: 'QueueController'
      }).
      otherwise({
        redirectTo: '/showtracks'
      });
}]);

app.directive("audiotrack", function() {
    return {
      restrict: 'E',
        templateUrl: '/track.html',
        replace: true,
        scope: {itemObject: "=",
                onTrackPlay: "&",
                onQueueAdd: "&"}
    }
});


app.service("QueueService", function() {
     var self = this;
     this.items = [];

     this.length = function() {
         return self.items.length;
     };

     this.add = function(item) {
         return self.items.push(item);
     };

     this.prepend = function(item) {
         return self.items.unshift(item);
     };
});

app.controller('MainController', ['$rootScope', '$scope', '$http', '$timeout', '$interval', '$location', 'QueueService',
                                   function($rootScope, $scope, $http, $timeout, $interval, $location, QueueService) {

  $scope.currentView = 'showtracks';  
  $scope.currentPage = 1;
  $scope.pageSize = 10;
  $scope.devices = [];
  $scope.selected_devices = [];
  $scope.queueService = QueueService;

  $scope.changeView = function(view){
  	$location.path(view); // path not hash
  }

  $http({ cache: true, url: '/get_devices', method: 'GET'}).success(

      function (data, status, headers, config) {
        var devices = data['devices'];

         for (i = 0; i < devices.length; i++) { 

          if(devices[i].state == 'playing') {
              $scope.selected_devices.push(devices[i].id);
          }

          $scope.devices.push({
            device_id: devices[i].id,
            state: devices[i].state,
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

  $scope.devicesChanged = function() {
      var parameters = {'selected_devices': $scope.selected_devices};
      var json_data = JSON.stringify(parameters);
      $http({cache: false, url: '/create_zone', method: 'post', data: json_data});
  };

  // $scope.playqueue = function() {

  //     var parameters = {'queue': $scope.queueService.items};
  //     var json_data = JSON.stringify(parameters);
  //     return $http({cache: false, url: '/playqueue', method: 'post', data: json_data});
  //  };

   $scope.stop = function() {

    return $http({cache: false, url: '/stop', method: 'get'});
   };

   $scope.pause = function() {
      return $http({cache: false, url: '/pause', method: 'get'});
   };

   $scope.playqueue = function() {

      $scope.queueService.add(item);
      var parameters = {'queue': $scope.queueService.items};
      var json_data = JSON.stringify(parameters);
      return $http({cache: false, url: '/play', method: 'post', data: json_data});
   };

   $scope.track_select = function(item) {
      $scope.queueService.add(item);
      var parameters = {'id': item.id,
                        'queue': $scope.queueService.items,
                        'position': $scope.queueService.length-1};
      var json_data = JSON.stringify(parameters);
      return $http({cache: false, url: '/play', method: 'post', data: json_data});
   };

   $scope.toggle_queue = function() {
        if($scope.currentView == 'showtracks') {
            $scope.currentView = 'showqueue';
            $scope.changeView('showqueue');
        }
	else {
	    $scope.currentView = 'showtracks';
            $scope.changeView('showtracks');
	}
   };

   $scope.speakers = function() {
        $("#wrapper").toggleClass("toggled");
   };

   // $scope.track_add_to_queue = function(item) {
   // 	$scope.queueService.add(item);
   // };

}]);


app.controller('QueueController', ['$rootScope', '$scope', '$http', '$timeout', '$interval', '$location', 'QueueService',
                                   function($rootScope, $scope, $http, $timeout, $interval, $location, QueueService) {

  $scope.currentPage = 1;
  $scope.queueService = QueueService;

}]);
