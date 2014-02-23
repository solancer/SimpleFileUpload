function Data ($http, $scope) {
  $http.get('/:8080/json').
  success(function(data, status, headers, config) {
    $scope.list = data;
  })
}
